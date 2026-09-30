# Production and QA reference

Use this reference when building, rendering, or checking an actual slide file.

## Match density to delivery mode

Set the density budget from the brief's delivery mode before writing the slide map.

| Delivery mode | Words per slide (excluding title) | Pace | Detail lives in |
| --- | --- | --- | --- |
| Live talk | 0–15; a number, image, or phrase is often enough | about 1 slide per 1–2 minutes | speaker notes |
| Hybrid (presented, then sent) | up to about 30 | about 1 slide per 2 minutes | notes and appendix |
| Standalone reading deck | up to about 60, in short labeled blocks | reader-paced | appendix |

- Treat these as ceilings, not targets. Delete first; split second; never shrink text to fit.
- A standalone deck still uses assertion titles and one message per slide; it simply carries more of its own evidence.
- When one deck must serve both modes, build the live version and put the reading detail in speaker notes or a clearly marked appendix rather than compromising every slide.

## Use a consistent 16:9 grid

Default to 16:9 at 13.333 × 7.5 in (33.867 × 19.05 cm) unless the brief specifies another size.

- Keep content inside a 1.0 in (2.54 cm) left and right margin and a 0.75 in top and bottom margin.
- Use the outer 0.5 in band only for navigation and provenance: a section label, source citation, logo, or slide number. Full-bleed images and background fills may cross every margin.
- Place the assertion title at the same top-left position on every content slide (about 1.0 in from the left, 0.75 in from the top) so the eye learns where to look. Center only title, section, and single-statement slides.
- Use a 12-column grid inside the margins. Align every text box, chart, and image edge to a column or to another element.
- Leave at least 0.3 in between unrelated elements and group related elements closer than unrelated ones.
- Reserve the lower-left or lower-right corner for source citations in dark gray; keep them out of the reading path.

## Size type by role

| Role | Size | Weight and color |
| --- | --- | --- |
| Title or section slide headline | 44–54 pt | bold; white on deep navy or navy on light |
| Assertion title on a content slide | 36–40 pt, at most two lines | bold; deep navy |
| Hero number or single statement | 60–120 pt | bold; deep navy or primary blue |
| Key text and statements | 24–28 pt | regular; deep navy, charcoal, or dark gray |
| Supporting message text | 18–20 pt minimum | regular; charcoal or dark gray |
| Labels: section label, axis, legend, citation, caption | 12–14 pt minimum | regular or bold caps; dark gray `#4C4C4C` or primary blue |

- Message text never goes below 18 pt in a live presentation. If content only fits smaller, it belongs in notes or the appendix.
- Nothing on a slide goes below 12 pt. A 9 pt label disappears on a projector; if a label is not worth 12 pt, delete it.
- An assertion title that needs three lines is two messages or too many words; rewrite it rather than shrinking it.
- Use mid gray `#858487` only for 18 pt and larger de-emphasized labels (3.41:1 on off-white fails smaller text).

## Fonts and fallbacks

- English: Calibri. Thai: Kanit. Mixed Thai and English slides may use Kanit for both to keep one text rhythm.
- Calibri ships with Microsoft Office but not with Google Slides or every macOS install without Office. In Google Slides, use Carlito (metric-compatible with Calibri) and state the substitution.
- Kanit is a Google Font and is not installed with PowerPoint. For a .pptx that uses Kanit, embed fonts when the host tool supports it, or tell the user the recipient must install Kanit; otherwise PowerPoint will substitute a system font and Thai text will reflow.
- Thai script needs more line height than Latin: set Thai body line spacing to about 1.2–1.3 and check that tone marks and vowels above and below the line are not clipped.

## Apply color by role

Take colors from the roles in [../assets/palette.json](../assets/palette.json), not from arbitrary palette entries.

- Titles and body text: deep navy or charcoal on white or off-white; primary blue is acceptable for large headings.
- Accent: Gold Accent `#FFB300` as a highlight bar, marker, key data series, or fill behind navy text. On light backgrounds, never set text in `#FFB300`; use `#8A5A00` if a word itself must carry the accent color.
- Dark slides (section breaks, the Big Idea, the final ask): deep navy background with white text and gold accent.
- Supporting blues: chart series, icon fills, and shapes, not body text on light backgrounds.
- Use one gold. Do not introduce a second, softer yellow for arrows or markers; `#FFB300` is the only accent.
- Never use pure black, including for icons; use charcoal `#272729` or deep navy.
- Do not use any color outside the palette. Off-palette colors usually enter through tool defaults (PowerPoint's `#4F81BD` blue, default chart styles), so set the theme colors below before building.
- Check any unavoidable non-palette text color with `python scripts/check_contrast.py FOREGROUND BACKGROUND`.

## Set the theme colors first

When building a .pptx or Google Slides deck, replace the default theme colors with the `pptx_theme` mapping in [../assets/palette.json](../assets/palette.json) before adding content. Default shapes, SmartArt, charts, and hyperlinks then inherit BlueSlide colors instead of Office blues. In Google Slides, set the same values under **Theme → Colors**.

## Accessibility

- Never let color be the only carrier of meaning. Pair the accent with position, size, a direct label, or a marker.
- Keep the accent and the main blue distinguishable in grayscale; the gold–navy pair survives common color-vision deficiencies, but two adjacent blues may not.
- Give meaningful images and charts alt text that states the message, not just the chart type.
- Set a logical reading order for text boxes so screen readers follow the intended eye path.
- Avoid flashing or rapid animation; use builds only to reveal a sequence the speaker narrates.

## Audit the file

For a .pptx, run the automated audit before visual QA:

```bash
python scripts/audit_pptx.py deck.pptx
```

It reports errors for off-palette colors, pure black, text below 12 pt, fonts other than Calibri, Carlito, or Kanit, and text that fails 4.5:1 against its shape fill or slide background. It warns about paragraphs of more than eight words set below 18 pt and about theme colors that differ from `pptx_theme`. Fix every error before delivery, or tell the user which ones remain and why. The audit reads explicit formatting and the theme only; it cannot see styles inherited from layouts, rendered overlap, or images, so it complements visual QA rather than replacing it.

## Render for visual QA

Inspect rendered pixels, not only the file's object model.

- If the host tool can export or screenshot slides, use it.
- For a .pptx on a machine with LibreOffice:

  ```bash
  soffice --headless --convert-to pdf deck.pptx
  ```

  Then rasterize the PDF (for example `pdftoppm -png -r 80 deck.pdf slide`) and view each image.
- LibreOffice substitutes missing fonts. When a render shows unexpected wrapping, confirm whether the font was installed before rewriting the slide.
- Review a slide-sorter view (all thumbnails together) for rhythm and consistency, then each slide at full size for clipping, overflow, overlap, contrast, and label legibility.
- If no rendering path is available, say so explicitly in the delivery and list the checks that could not be performed.
