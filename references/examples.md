# Worked examples

Use these examples to calibrate output quality. They are illustrative; do not reuse their facts or numbers in real work.

## Example 1 — full deck, compressed

**Request:** “Make slides for next week's executive committee about our outpatient no-show problem.”

### Presentation brief (abridged)

```text
Presentation: Outpatient no-show reduction proposal
Primary audience: Hospital executive committee (6 people); CFO holds budget authority
Audience knowledge and stance: Know no-shows are "a problem"; have not seen the cost; skeptical of new IT spend
Goal / desired action: Approve a 3-month SMS-reminder pilot in two clinics
Big Idea: A low-cost reminder pilot can recover lost appointment capacity within one quarter, so we should approve it now.
What Is: About 1 in 5 booked outpatient slots goes unused
Opponent: Invisible cost — empty slots do not appear as a line item, and waitlists keep growing
What Could Be: Recovered slots shorten waits without new staff or rooms
Bridge / recommendation: Pilot in two clinics, measure, then decide on rollout
Delivery mode and presenter: Live, 10 minutes + 5 minutes Q&A, presented by the operations manager
Duration / target slide count / Q&A: 10 minutes / 5 slides + 2 appendix / 5 minutes
Output / aspect ratio / language: PowerPoint, 16:9, English
Assumptions: No-show rate and slot cost come from last quarter's scheduling export (to be verified)
```

### Narrative spine

1. **Goal** — The committee approves a two-clinic pilot today.
2. **What Is** — One in five booked slots goes unused while patients wait weeks.
3. **Opponent** — The loss is invisible: no budget line records an empty slot.
4. **What Could Be** — Recovered capacity shortens waits with the staff and rooms we already have.
5. **Bridge / action** — A 3-month, two-clinic pilot with a pre-agreed success threshold; approve today.

### Slide map

```text
Slide number: 1
Assertion: A low-cost reminder pilot can recover lost clinic capacity this quarter
Narrative purpose: Goal — state the Big Idea and the decision up front
Evidence: None needed; this is the promise the deck will prove
Visual: Deep-navy title slide; assertion in white; meeting date and presenter in light blue
Speaker notes / appendix: "By the end, I will ask you to approve one pilot."

Slide number: 2
Assertion: One in five outpatient slots goes unused
Narrative purpose: What Is — make the problem recognizable
Evidence: Last-quarter no-show rate by clinic
Visual: One large number ("1 in 5") with an icon array of 5 chairs, one highlighted in gold
Speaker notes / appendix: Clinic-level breakdown → appendix A1

Slide number: 3
Assertion: Empty slots are our largest invisible cost
Narrative purpose: Build the Opponent — reveal the hidden cost
Evidence: Unused slots × average slot value, compared with two known budget lines
Visual: Horizontal bar chart, sorted descending, every bar directly labeled; the no-show bar in gold, others in light blue; no gridlines or legend
Speaker notes / appendix: Costing method and assumptions → appendix A2

Slide number: 4
Assertion: Reminders recover capacity without new staff or rooms
Narrative purpose: What Could Be — make the future concrete
Evidence: Published reminder-program results from comparable settings (cite source)
Visual: Before/after comparison of a clinic week: empty chairs vs. filled chairs
Speaker notes / appendix: Study details and limits

Slide number: 5
Assertion: Approve a 3-month pilot in two clinics today
Narrative purpose: Bridge / action — make the decision easy
Evidence: Cost, timeline, owner, success threshold, stop condition
Visual: Deep-navy slide; three-step timeline; the ask in white, the decision date marked in gold
Speaker notes / appendix: Risks and mitigations
```

## Example 2 — rewriting one crowded slide

This is a slide-level edit: confirm the local objective, then rewrite. No full intake is needed.

**Before**

```text
Title: Q3 Results
• Revenue was 12.4M, up from 10.9M in Q2 (+14%)
• New customers: 38 (vs. 31 in Q2)
• Churn decreased from 4.1% to 3.2%
• Enterprise segment grew fastest (+27%)
• SMB flat
• Marketing spend unchanged
• Hiring on track (see appendix)
```

**Diagnosis:** a topic title, seven equal-weight bullets, and no stated message. The audience cannot tell which fact matters.

**After**

```text
Title (assertion): Enterprise drove Q3's 14% revenue growth
Visual: Horizontal bars for segment growth — Enterprise +27% in gold, SMB 0% and others in light blue, direct labels
Supporting line (24 pt, navy): Revenue 12.4M, up from 10.9M
Moved to notes: new-customer count, churn, marketing spend
Moved to appendix: hiring status
```

If churn is itself a message the audience must act on, give it its own slide with its own assertion rather than restoring it to this one.

## Assertion titles — before and after

| Topic title | Assertion title |
| --- | --- |
| Market overview | Mid-size clinics are the fastest-growing, least-served segment |
| Timeline | We can launch in 10 weeks if legal review starts Monday |
| Survey results | Nurses lose 40 minutes a shift to manual charting |
| Risks | Supplier concentration is our only risk that could stop the launch |
| Next steps | Approve the pilot budget today to start in January |

## Reusable slide patterns

These forms repeatedly make one message immediate. Choose by the message, not by variety.

| Message shape | Pattern | BlueSlide treatment |
| --- | --- | --- |
| “This affects 1 in N” | Icon array of N identical figures | One figure in primary blue or gold, the rest in charcoal; the ratio stated in the headline text |
| “We shift effort from X to Y” | Two short verb columns with an arrow | Left column in dark gray labeled TODAY, right in deep navy labeled TO BE; the arrow is the only gold |
| “One number proves it” | Hero number with a one-line caption | 60–120 pt navy number, 24 pt caption; supporting paragraph at 18 pt or moved to notes |
| “Humans stay in control” | Step flow with the human step distinguished | Chevrons in primary blue with white labels (5.13:1); the human step in deep navy with a gold marker. Lighter blues cannot carry white labels |
| “We scale only with proof” | Evidence-gated roadmap | Stages on one line; completed stage marked in gold, later gates in primary blue, each labeled with the evidence required |
| “Here is what we have not proved” | Honest-limits slide | Paired assertion (“Technically feasible. Clinically not yet validated.”), then what exists, what is missing, and the next evidence step |

## Common defects to catch in QA

- Gold text on a light background, used to make a label stand out. Use navy or primary blue text with a gold bar or marker instead.
- A second, paler yellow for arrows or dots next to `#FFB300` text. Use one gold.
- Office-default blue (`#4F81BD`) or other theme defaults in shapes, SmartArt, or charts. Set `pptx_theme` before building.
- Section labels, captions, citations, or chart labels at 8–10 pt. Raise them to 12 pt or delete them.
- Near-black (`#000000`–`#111111`) icons. Recolor them charcoal or deep navy.
- A chart with gridlines, a legend, and a value axis when every bar already carries a direct label. Remove all three.
- Gray text colors that are not in the palette. Map them to dark gray `#4C4C4C` or charcoal.
