#!/usr/bin/env python3
"""Audit a .pptx against the BlueSlide palette, type, and contrast rules.

Usage:
    python scripts/audit_pptx.py deck.pptx

Reports, per slide and per embedded chart:
  ERROR  off-palette colors, pure black, text below 12 pt, text that fails
         4.5:1 against its shape fill or slide background, disallowed fonts,
         and internal links to parts missing from the file (a corrupt deck)
  WARN   long paragraphs set below 18 pt (message text that may be too
         small; Thai is measured in characters), charts that carry direct
         value labels and also gridlines or a legend, and theme colors or
         fonts that differ from pptx_theme in assets/palette.json

Resolved: explicit run, paragraph, and text-box formatting (by list level),
shape fills including theme style fills, slide/layout/master backgrounds,
and theme colors. Not resolved: sizes inherited from layout or master
placeholders (counted and reported), colors modified by lumMod/lumOff/tint/
shade, text over pictures or gradients, and colors inside images. Render the
deck for visual QA as well. Exits with status 1 when any ERROR is found.
"""

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_contrast import contrast  # noqa: E402

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
PALETTE = json.loads((Path(__file__).resolve().parent.parent / "assets" / "palette.json").read_text())
ALLOWED_COLORS = {c.upper() for c in PALETTE["colors"].values()} | {c.upper() for c in PALETTE["pptx_theme"].values()}
ALLOWED_FONTS = {"Calibri", "Carlito", "Kanit"}
SCHEME_ALIASES = {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}
TEXT_MIN, LABEL_MIN_PT, MESSAGE_MIN_PT = 4.5, 12, 18
C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
THAI = re.compile("[\u0E00-\u0E7F]")
THAI_LONG_CHARS = 50


def q(tag):
    prefix, name = tag.split(":")
    return f"{{{NS[prefix]}}}{name}"


class Deck:
    def __init__(self, path):
        self.zip = zipfile.ZipFile(path)
        self.parts = set(self.zip.namelist())
        self.broken = {}
        theme = self.read("ppt/theme/theme1.xml")
        scheme = theme.find(".//a:clrScheme", NS)
        self.theme_colors = {}
        for slot in scheme:
            name = slot.tag.split("}")[1]
            color = slot.find("a:srgbClr", NS)
            system = slot.find("a:sysClr", NS)
            value = color.get("val") if color is not None else system.get("lastClr") if system is not None else None
            if value:
                self.theme_colors[name] = "#" + value.upper()
        fonts = theme.find(".//a:fontScheme", NS)
        self.theme_fonts = {
            "+mj-lt": fonts.find("a:majorFont/a:latin", NS).get("typeface"),
            "+mn-lt": fonts.find("a:minorFont/a:latin", NS).get("typeface"),
        }

    def read(self, name):
        return ET.fromstring(self.zip.read(name))

    def slides(self):
        names = [n for n in self.zip.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
        return sorted(names, key=lambda n: int(re.search(r"(\d+)", n.split("/")[-1]).group(1)))

    def related_all(self, part, rel_type):
        folder, file = part.rsplit("/", 1)
        rels = f"{folder}/_rels/{file}.rels"
        if rels not in self.parts:
            return []
        targets = []
        for rel in self.read(rels).iter(f"{REL_NS}Relationship"):
            if rel.get("Type").endswith("/" + rel_type) and rel.get("TargetMode") != "External":
                target = rel.get("Target")
                # A leading "/" makes the target package-absolute (pptxgenjs writes these)
                parts = [] if target.startswith("/") else folder.split("/")
                for piece in target.lstrip("/").split("/"):
                    if piece in ("", "."):
                        continue
                    parts = parts[:-1] if piece == ".." else parts + [piece]
                resolved = "/".join(parts)
                if resolved in self.parts:
                    targets.append(resolved)
                else:
                    self.broken.setdefault(part, set()).add(resolved)
        return targets

    def related(self, part, rel_type):
        targets = self.related_all(part, rel_type)
        return targets[0] if targets else None

    def color(self, fill):
        """Resolve a fill-like element to (#RRGGBB or None, exact)."""
        if fill is None:
            return None, True
        srgb = fill.find("a:srgbClr", NS)
        scheme = fill.find("a:schemeClr", NS)
        node = srgb if srgb is not None else scheme
        if node is None:
            return None, True
        exact = len(node) == 0 or all(child.tag == q("a:alpha") for child in node)
        if srgb is not None:
            return "#" + srgb.get("val").upper(), exact
        slot = SCHEME_ALIASES.get(scheme.get("val"), scheme.get("val"))
        return self.theme_colors.get(slot), exact

    def background(self, part):
        """Solid background of a slide, falling back to its layout, then master."""
        layout = self.related(part, "slideLayout")
        master = self.related(layout, "slideMaster") if layout else None
        for candidate in (part, layout, master):
            if not candidate:
                continue
            bg = self.read(candidate).find("p:cSld/p:bg", NS)
            if bg is None:
                continue
            fill = bg.find("p:bgPr/a:solidFill", NS)
            return self.color(fill if fill is not None else bg.find("p:bgRef", NS))[0]
        return self.theme_colors.get("lt1", "#FFFFFF")


def run_properties(run, paragraph, body):
    """Run formatting layers, nearest first: run, paragraph, text-box list level."""
    properties = paragraph.find("a:pPr", NS)
    level = int(properties.get("lvl", "0")) + 1 if properties is not None else 1
    layers = [
        run.find("a:rPr", NS),
        paragraph.find("a:pPr/a:defRPr", NS),
        body.find(f"a:lstStyle/a:lvl{level}pPr/a:defRPr", NS),
    ]
    return [layer for layer in layers if layer is not None]


def first(layers, finder):
    for layer in layers:
        value = finder(layer)
        if value is not None:
            return value
    return None


def is_long(text):
    """More than eight words, or about that much Thai (which has no word spaces)."""
    if THAI.search(text):
        return len(re.sub(r"\s", "", text)) > THAI_LONG_CHARS
    return len(text.split()) > 8


def shape_background(deck, shape, slide_bg):
    """Background behind a shape's text: explicit fill, theme style fill, or slide."""
    properties = shape.find("p:spPr", NS)
    if properties is not None:
        if properties.find("a:solidFill", NS) is not None:
            return deck.color(properties.find("a:solidFill", NS))
        if properties.find("a:noFill", NS) is not None:
            return slide_bg, True
        if properties.find("a:gradFill", NS) is not None or properties.find("a:blipFill", NS) is not None:
            return None, False
    style_fill = shape.find("p:style/a:fillRef", NS)
    if style_fill is not None and style_fill.get("idx", "0") != "0":
        return deck.color(style_fill)
    return slide_bg, True


def audit_colors(nodes, where, add):
    for value in sorted({"#" + node.get("val").upper() for node in nodes}):
        if value == "#000000":
            add(where, "ERROR", "pure black #000000; use charcoal #272729 or deep navy")
        elif value not in ALLOWED_COLORS:
            add(where, "ERROR", f"off-palette color {value}")


def audit_chart(deck, part, where, add):
    chart = deck.read(part)
    audit_colors(chart.iter(q("a:srgbClr")), where, add)
    labeled = any(node.get("val") == "1" for node in chart.iter(f"{{{C_NS}}}showVal"))
    if labeled:
        clutter = []
        if any(True for _ in chart.iter(f"{{{C_NS}}}majorGridlines")):
            clutter.append("gridlines")
        if chart.find(f".//{{{C_NS}}}legend") is not None:
            clutter.append("legend")
        if clutter:
            add(where, "WARN", "chart has direct value labels and also " + " and ".join(clutter) + "; remove them")
    for size in chart.iter(q("a:defRPr")):
        if size.get("sz") and int(size.get("sz")) / 100 < LABEL_MIN_PT:
            add(where, "ERROR", f"chart text at {int(size.get('sz')) / 100:g} pt is below {LABEL_MIN_PT} pt")
            break


def audit(path):
    deck = Deck(path)
    findings = {}
    unsized = 0

    def add(where, level, rule, sample=None):
        samples = findings.setdefault((where, level, rule), [])
        if sample and sample not in samples:
            samples.append(sample)

    expected = {k: v.upper() for k, v in PALETTE["pptx_theme"].items()}
    mismatched = [f"{slot} {deck.theme_colors.get(slot)}≠{value}" for slot, value in expected.items() if deck.theme_colors.get(slot) != value]
    if mismatched:
        add("theme", "WARN", "theme colors differ from pptx_theme: " + ", ".join(mismatched))
    for key, font in deck.theme_fonts.items():
        if font not in ALLOWED_FONTS:
            add("theme", "WARN", f"theme font {key} is {font!r}")

    for part in deck.slides():
        label = "slide " + re.search(r"(\d+)", part.split("/")[-1]).group(1)
        root = deck.read(part)
        slide_bg = deck.background(part)
        audit_colors(root.iter(q("a:srgbClr")), label, add)
        for chart_part in deck.related_all(part, "chart"):
            audit_chart(deck, chart_part, label + " chart", add)

        for shape in root.iter(q("p:sp")):
            body = shape.find("p:txBody", NS)
            if body is None:
                continue
            background, background_exact = shape_background(deck, shape, slide_bg)
            for paragraph in body.findall("a:p", NS):
                runs = [run for run in paragraph.findall("a:r", NS) if run.findtext("a:t", "", NS).strip()]
                text = "".join(run.findtext("a:t", "", NS) for run in runs).strip()
                if not text:
                    continue
                snippet = text[:40]
                warned_length = False
                for run in runs:
                    layers = run_properties(run, paragraph, body)
                    size = first(layers, lambda layer: layer.get("sz"))
                    if size is None:
                        unsized += 1
                    elif int(size) / 100 < LABEL_MIN_PT:
                        add(label, "ERROR", f"{int(size) / 100:g} pt text is below {LABEL_MIN_PT} pt", snippet)
                    elif int(size) / 100 < MESSAGE_MIN_PT and is_long(text) and not warned_length:
                        add(label, "WARN", f"{int(size) / 100:g} pt long paragraph; message text needs {MESSAGE_MIN_PT} pt", snippet)
                        warned_length = True
                    for tag in ("a:latin", "a:cs", "a:ea"):
                        face = first(layers, lambda layer, t=tag: layer.find(t, NS).get("typeface") if layer.find(t, NS) is not None else None)
                        face = deck.theme_fonts.get(face, face)
                        if face and not face.startswith("+") and face not in ALLOWED_FONTS:
                            add(label, "ERROR", f"font {face!r} is not Calibri, Carlito, or Kanit", snippet)
                    color, exact = first(layers, lambda layer: deck.color(layer.find("a:solidFill", NS)) if layer.find("a:solidFill", NS) is not None else None) or (None, True)
                    if color and exact and background and background_exact:
                        ratio = contrast(color, background)
                        if ratio < TEXT_MIN:
                            add(label, "ERROR", f"text {color} on {background} is {ratio:.2f}:1 (needs {TEXT_MIN}:1)", snippet)

    for part, targets in deck.broken.items():
        where = re.sub(r"^slide(\d+)$", r"slide \1", Path(part).stem)
        for target in sorted(targets):
            add(where, "ERROR", f"broken link to {target}; the deck may be corrupt")

    for (where, level, rule), samples in findings.items():
        detail = f": {samples[0]!r}" + (f" (+{len(samples) - 1} more)" if len(samples) > 1 else "") if samples else ""
        print(f"{where:>15}  {level:5}  {rule}{detail}")
    errors = sum(level == "ERROR" for _, level, _ in findings)
    warnings = sum(level == "WARN" for _, level, _ in findings)
    print(f"\n{errors} error(s), {warnings} warning(s) in {len(deck.slides())} slide(s)")
    if unsized:
        print(f"{unsized} text run(s) inherit their size from a layout or master and were not size-checked; confirm them in the rendered slides.")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip())
        sys.exit(2)
    sys.exit(audit(sys.argv[1]))
