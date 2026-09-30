---
name: blue-slide
description: Create, rewrite, review, or simplify presentations and pitch decks using requirements discovery, a restrained blue visual system, one-message-per-slide editing, audience-centered narrative, flat visual communication, and honest chart design. Use for PowerPoint, Google Slides, keynote-style talks, investor decks, slide outlines, infographics, chart redesign, presentation intake, or requests to be interviewed or “grilled” before making slides clearer, less crowded, more visual, or more decision-oriented.
---

# BlueSlide

Create concise presentations in which every slide has one unmistakable message. Use blue as the primary visual language, quiet backgrounds for space, and a small contrasting accent only where attention is required.

## Load the references

- Read [references/method.md](references/method.md) for every task.
- Read [references/intake.md](references/intake.md) for a new deck, an incomplete or conflicting brief, a high-stakes presentation, or an explicit Grill Me request. Do not load the full intake for a small, well-scoped edit.
- Read [references/narrative.md](references/narrative.md) for every task that needs a persuasive story, talk, pitch, recommendation, or call to action.
- Read [references/infographics.md](references/infographics.md) when the task includes data, charts, diagrams, comparisons, timelines, maps, frameworks, or infographics.
- Read [references/production.md](references/production.md) when building, rendering, or reviewing an actual slide file, and for density budgets, grid, fonts, color roles, and accessibility.
- Read [references/examples.md](references/examples.md) to calibrate the brief, slide map, and assertion titles before producing them for the first time in a session.
- Read [references/resource-directory.md](references/resource-directory.md) only when external colors, icons, or templates are needed.
- Use [assets/palette.json](assets/palette.json) as the canonical BlueSlide palette and its `roles` to decide where each color may appear.
- Run [scripts/check_contrast.py](scripts/check_contrast.py) to verify any text color that is not already a palette text role, and [scripts/audit_pptx.py](scripts/audit_pptx.py) on every built .pptx.

## Size the task first

Classify the request before starting, then run the workflow at that depth. Compress stages for small tasks; never reorder them.

| Scope | Examples | Brief | Narrative spine | Slide map | Approval gates | Build and QA |
| --- | --- | --- | --- | --- | --- | --- |
| New or rebuilt deck | talk, pitch, report-to-deck | full brief; Grill Me when warranted | required | required | brief and slide map | full |
| Section or several slides | add a results section, rework the ending | confirm how it fits the existing argument | one line on its role in the spine | entries for the affected slides | slide map only if the argument changes | affected slides plus neighbors |
| Single slide or chart | rewrite a crowded slide, redesign a chart | one-sentence local objective | skip | one entry, stated inline | none; proceed | that slide |
| Review only | critique a deck without editing | infer from the deck; state assumptions | reconstruct and critique | critique against the map | none | findings ranked by impact, with audit results for a .pptx |

The approval steps in the workflow below apply only where this table lists a gate, or when the user asks to approve before building.

## Follow the workflow

### 0. Establish or confirm the brief

- Inspect every supplied file, note, source, and reference before asking questions.
- Ask only questions whose answers are not already available.
- For a new deck, establish at least the audience, desired action, delivery context, duration or slide count, content sources, output format, language, deadline, and constraints before authoring.
- Use full **Grill Me mode** for ambiguous, high-stakes, investor, executive, sales, conference, defense, or public-facing presentations.
- For a small edit with a clear request, confirm the local objective and proceed without the full interview.
- Ask questions in short rounds rather than one overwhelming list.
- Summarize the answers as a presentation brief and surface assumptions, conflicts, and missing evidence.
- Obtain approval of the brief before planning the deck unless the user explicitly delegates full autonomy or asks to proceed with stated assumptions.

### 1. Define the decision

- Identify the audience, the change they should experience, and the action or decision required.
- Set the delivery mode (live, hybrid, or standalone reading) because it fixes the density budget in [references/production.md](references/production.md).
- Write one Big Idea that states a complete point of view, not merely a topic.
- For investor material, define the opportunity, proof, assumptions, risk, track record, and precise ask.

### 2. Delete before designing

- Give each slide one primary message.
- Write the slide title as an assertion whenever possible.
- Remove repeated claims, throat-clearing, decorative labels, and evidence that does not change the decision.
- Split a crowded slide instead of shrinking text.
- Move technical detail to notes or an appendix when it is needed for diligence but not for the live argument.
- Apply the rule: “Great writing is all about the power of the deleted word.”

### 3. Build the narrative

- Use the four-stage BlueSlide sequence: Goal → What Is → Build the Opponent → What Could Be.
- Treat the audience as the hero and the presenter as the guide.
- Alternate between “what is” and “what could be” to create tension.
- Progress toward a clear transformation and finish with action.
- Vary evidence, story, image, and data without weakening the narrative thread.
- Make the deck retellable: a reader should be able to repeat the argument after a quick review.

### 4. Choose the visual form

- Prefer one confident composition over a grid of panels.
- Use a photograph, icon, number, chart, or short phrase only when it communicates faster than prose.
- Remove decoration and expose the essence.
- Use simple flat icons as a universal visual language.
- Use the Gutenberg diagram, F-pattern, or Z-pattern to create an intentional reading path.
- Place emphasis through size, color, spacing, position, or selective header weight—not bullets alone.
- Replace bullets with step labels, icons, a sequence, or a comparison when those devices clarify meaning.

### 5. Produce the slide map

- Map the narrative before building slides.
- Give every slide one assertion that can stand as its title.
- Keep each slide within the density budget for the delivery mode.
- Record each slide's narrative purpose, minimum necessary evidence, intended visual form, and material that belongs in speaker notes or the appendix.
- Use this schema:

```text
Slide number:
Assertion:
Narrative purpose:
Evidence:
Visual:
Speaker notes / appendix:
```

- Review the slide map for repetition, missing transitions, weak proof, and information overload.
- Obtain approval of the slide map before building unless the user explicitly delegates full autonomy.

### 6. Apply the BlueSlide system

- Use approximately 70% quiet background, 25% main color, and 5% accent color.
- Use a low-saturation background.
- Choose a main color strong enough to work as text or as a background.
- Use the canonical Gold Accent `#FFB300` sparingly and only for the one focal element per slide: a key number, series, marker, or highlight bar. Use one gold only; never introduce a second, softer yellow.
- Never set text in the gold accent on a light background (1.79:1 on white). On light slides, place navy text on a gold fill, or use `#8A5A00` when a word itself must carry the accent. On deep-navy slides, gold text is safe.
- Use monochromatic, analogous, complementary, or triadic color relationships only when comparison requires them.
- Never use pure black for text or icons; use charcoal or deep navy.
- Use no color outside [assets/palette.json](assets/palette.json). Before adding content to a .pptx or Google Slides deck, set its theme colors to the palette's `pptx_theme` so default shapes and charts do not fall back to Office blues.
- Never apply gradients or shadows to text.
- Prefer Calibri for English and Kanit for Thai; apply the font fallbacks and Thai line-spacing rules in [references/production.md](references/production.md).
- Use no more than two typefaces in one presentation.
- Size type by role (full scale in [references/production.md](references/production.md)): 44–54 pt on title and section slides, 36–40 pt bold for a content slide's assertion title (at most two lines), 24–28 pt for key text, never below 18 pt for message text, and never below 12 pt for anything—including section labels, axis labels, and citations.
- Set titles, headlines, and body text in deep navy or charcoal; primary blue may be used for large headings. Keep supporting blues for fills and chart series, not light-background text.
- Hold all text to 4.5:1 contrast or better; projectors wash out marginal contrast.
- Never let color be the only carrier of meaning; pair the accent with position, size, or a direct label.
- Keep body text regular weight. Never bold body paragraphs.
- Stress a header by increasing size, changing color, adding space, or using a bold weight.

### 7. Build with the available presentation tool

- Use the host's available PowerPoint, Google Slides, or presentation-production tool when the user requests a file.
- Treat BlueSlide's narrative, density, palette, typography, chart, and visual rules as constraints that override generic tool defaults.
- If no presentation-production tool is available, deliver the approved brief and slide map; do not claim that a deck file was created.

### 8. Perform visual QA

- For a .pptx, run `python scripts/audit_pptx.py deck.pptx` and fix every error.
- Render every final slide to images and inspect them, using the host tool or the LibreOffice path in [references/production.md](references/production.md). If rendering is impossible, say so in the delivery and list the checks that were not performed.
- Fix clipping, overflow, unintended overlap, weak contrast, awkward wrapping, inconsistent spacing, illegible labels, and crowded compositions.
- Confirm that the sequence still reads as one coherent argument in both slide-sorter view and full-screen view.
- Confirm that data, citations, and visual emphasis match the approved slide map.

### 9. Validate the result

- Confirm that the key message is understandable within a few seconds.
- Confirm that every element earns its place.
- Confirm that the accent color marks only the intended focal point.
- Confirm that text is readable, message text is at least 18 pt, nothing is below 12 pt, and every text color meets 4.5:1 against its actual background.
- Confirm that every color comes from the palette and that the theme colors match `pptx_theme`.
- Confirm that the reading path is intentional.
- Confirm that charts are honest, correctly ordered, directly labeled when possible, and free of unnecessary decoration.
- Confirm that no slide was made to fit by shrinking its content.

## Required output sequence

Do not skip directly from raw requirements to slide design. Produce work in this order, at the depth set by the task scope:

1. **Presentation brief** — approved by the user or accompanied by explicit assumptions.
2. **Narrative spine** — Goal → What Is → Build the Opponent → What Could Be → bridge/action.
3. **Slide map** — one assertion, evidence set, and visual intent per slide.
4. **Built deck** — only after the brief and slide map are approved or autonomy is delegated.
5. **Visual QA** — rendered inspection and correction before delivery.

## Respect external resources

- Treat external templates as structural inspiration unless their license explicitly permits reuse.
- Check icon and asset licenses before use, preserve required attribution, and avoid copying a creator's distinctive deck wholesale.
- Use only the three conceptual influences named in [references/method.md](references/method.md) when describing BlueSlide's presentation lineage.
