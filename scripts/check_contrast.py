#!/usr/bin/env python3
"""Check WCAG contrast between slide colors.

Usage:
    python scripts/check_contrast.py FOREGROUND BACKGROUND [...]
    python scripts/check_contrast.py --palette

Pass colors as pairs of RRGGBB hex values, with or without a leading #
(quote values that start with #, because shells treat # as a comment). With --palette, report every text role in
assets/palette.json against the backgrounds, panels, and deep navy that it may sit on.
Exits with status 1 when any pair falls below the 4.5:1 BlueSlide text rule.
"""

import json
import re
import sys
from pathlib import Path

TEXT_MIN = 4.5
PALETTE = Path(__file__).resolve().parent.parent / "assets" / "palette.json"


def luminance(hex_color):
    value = hex_color.lstrip("#")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
        raise ValueError(f"expected RRGGBB hex color, got {hex_color!r}")
    channels = [int(value[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(foreground, background):
    high, low = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def palette_pairs():
    roles = json.loads(PALETTE.read_text())["roles"]
    for background in roles["background"]:
        for foreground in roles["text_on_light"] + [roles["accent_text_on_light"]]:
            yield foreground, background
    for background in roles["panel"]:
        for foreground in roles["text_on_panel"]:
            yield foreground, background
    for foreground in roles["text_on_dark"]:
        yield foreground, "#071560"


def main(args):
    if args == ["--palette"]:
        pairs = list(palette_pairs())
    elif args and len(args) % 2 == 0:
        pairs = list(zip(args[::2], args[1::2]))
    else:
        print(__doc__.strip())
        return 2

    failed = False
    for foreground, background in pairs:
        try:
            ratio = contrast(foreground, background)
        except ValueError as error:
            print(error)
            return 2
        verdict = "ok" if ratio >= TEXT_MIN else "FAIL (fill or large mark only)" if ratio >= 3 else "FAIL"
        failed |= ratio < TEXT_MIN
        print(f"{foreground} on {background}: {ratio:5.2f}:1  {verdict}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
