#!/usr/bin/env python3
"""Audit a .pptx against the BlueSlide palette, type, and contrast rules.

Usage:
    python scripts/audit_pptx.py deck.pptx

Reports, per slide:
  ERROR  off-palette colors, pure black, text below 12 pt, text that fails
         4.5:1 against its shape fill or slide background, disallowed fonts
  WARN   paragraphs of more than eight words set below 18 pt (message text
         that may be too small), and a theme color scheme that does not match
         pptx_theme in assets/palette.json

Only explicit formatting, paragraph and text-box defaults, and theme values
are resolved. Styles inherited from slide layouts and masters, and colors
modified by lumMod/lumOff/tint/shade, are not; render the deck for visual QA
as well. Exits with status 1 when any ERROR is found.
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


def q(tag):
    prefix, name = tag.split(":")
    return f"{{{NS[prefix]}}}{name}"


class Deck:
    def __init__(self, path):
        self.zip = zipfile.ZipFile(path)
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

    def related(self, part, rel_type):
        folder, file = part.rsplit("/", 1)
        rels = f"{folder}/_rels/{file}.rels"
        if rels not in self.zip.namelist():
            return None
        for rel in self.read(rels).iter(f"{REL_NS}Relationship"):
            if rel.get("Type").endswith("/" + rel_type):
                target = rel.get("Target")
                parts = folder.split("/")
                for piece in target.split("/"):
                    parts = parts[:-1] if piece == ".." else parts + [piece]
                return "/".join(parts)
        return None

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
    """Merge rPr with paragraph and text-box level-1 defaults, nearest first."""
    layers = [
        run.find("a:rPr", NS),
        paragraph.find("a:pPr/a:defRPr", NS),
        body.find("a:lstStyle/a:lvl1pPr/a:defRPr", NS),
    ]
    return [layer for layer in layers if layer is not None]


def first(layers, finder):
    for layer in layers:
        value = finder(layer)
        if value is not None:
            return value
    return None


def audit(path):
    deck = Deck(path)
    findings = []

    expected = {k: v.upper() for k, v in PALETTE["pptx_theme"].items()}
    mismatched = [f"{slot} {deck.theme_colors.get(slot)}≠{value}" for slot, value in expected.items() if deck.theme_colors.get(slot) != value]
    if mismatched:
        findings.append(("theme", "WARN", "theme colors differ from pptx_theme: " + ", ".join(mismatched)))
    for key, font in deck.theme_fonts.items():
        if font not in ALLOWED_FONTS:
            findings.append(("theme", "WARN", f"theme font {key} is {font!r}"))

    for part in deck.slides():
        label = "slide " + re.search(r"(\d+)", part.split("/")[-1]).group(1)
        root = deck.read(part)
        slide_bg = deck.background(part)
        seen = set()

        for node in root.iter(q("a:srgbClr")):
            value = "#" + node.get("val").upper()
            if value in seen:
                continue
            seen.add(value)
            if value == "#000000":
                findings.append((label, "ERROR", "pure black #000000; use charcoal #272729 or deep navy"))
            elif value not in ALLOWED_COLORS:
                findings.append((label, "ERROR", f"off-palette color {value}"))

        for shape in root.iter(q("p:sp")):
            body = shape.find("p:txBody", NS)
            if body is None:
                continue
            shape_fill, _ = deck.color(shape.find("p:spPr/a:solidFill", NS))
            background = shape_fill or slide_bg
            for paragraph in body.findall("a:p", NS):
                runs = paragraph.findall("a:r", NS)
                text = "".join(run.findtext("a:t", "", NS) for run in runs).strip()
                if not text:
                    continue
                snippet = text[:40]
                for run in runs:
                    if not run.findtext("a:t", "", NS).strip():
                        continue
                    layers = run_properties(run, paragraph, body)
                    size = first(layers, lambda layer: layer.get("sz"))
                    if size and int(size) / 100 < LABEL_MIN_PT:
                        findings.append((label, "ERROR", f"{int(size) / 100:g} pt text is below {LABEL_MIN_PT} pt: {snippet!r}"))
                    elif size and int(size) / 100 < MESSAGE_MIN_PT and len(text.split()) > 8:
                        findings.append((label, "WARN", f"{int(size) / 100:g} pt paragraph of {len(text.split())} words; message text needs {MESSAGE_MIN_PT} pt: {snippet!r}"))
                    for tag in ("a:latin", "a:cs", "a:ea"):
                        face = first(layers, lambda layer, t=tag: layer.find(t, NS).get("typeface") if layer.find(t, NS) is not None else None)
                        face = deck.theme_fonts.get(face, face)
                        if face and not face.startswith("+") and face not in ALLOWED_FONTS:
                            findings.append((label, "ERROR", f"font {face!r} is not Calibri, Carlito, or Kanit: {snippet!r}"))
                    color, exact = first(layers, lambda layer: deck.color(layer.find("a:solidFill", NS)) if layer.find("a:solidFill", NS) is not None else None) or (None, True)
                    if color and exact and background:
                        ratio = contrast(color, background)
                        if ratio < TEXT_MIN:
                            findings.append((label, "ERROR", f"text {color} on {background} is {ratio:.2f}:1 (needs {TEXT_MIN}:1): {snippet!r}"))

    grouped = {}
    for where, level, message in findings:
        rule, _, sample = message.partition(": '")
        entry = grouped.setdefault((where, level, rule), [])
        if sample and sample not in entry:
            entry.append(sample)
    unique = list(grouped)
    for (where, level, rule), samples in grouped.items():
        detail = f": '{samples[0]}" + (f" (+{len(samples) - 1} more)" if len(samples) > 1 else "") if samples else ""
        print(f"{where:>9}  {level:5}  {rule}{detail}")
    errors = sum(level == "ERROR" for _, level, _ in unique)
    warnings = sum(level == "WARN" for _, level, _ in unique)
    print(f"\n{errors} error(s), {warnings} warning(s) in {len(deck.slides())} slide(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip())
        sys.exit(2)
    sys.exit(audit(sys.argv[1]))
