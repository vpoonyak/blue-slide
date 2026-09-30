# BlueSlide

**Less noise. Clearer message.**

BlueSlide is an original Codex skill for creating concise, blue-first presentations, infographics, and decision-ready pitch decks. It gives every slide one unmistakable message, uses visual contrast with restraint, and turns information into an audience-centered story.

## What BlueSlide does

- Defines the audience decision before designing slides.
- Interviews the user for unresolved audience, goal, delivery, content, and production requirements.
- Deletes repetition and splits overcrowded slides.
- Builds a persuasive journey from the present state to a better future.
- Uses a restrained 70:25:5 background, main, and accent color system.
- Applies flat visual communication, intentional eye flow, and honest chart design.
- Supports English and Thai presentations with Calibri and Kanit as the preferred typefaces.

## Narrative framework

BlueSlide structures persuasive content in four stages:

1. **Goal** — What should the audience do, decide, believe, or change?
2. **What Is** — What is the audience experiencing now?
3. **Build the Opponent** — What hidden cost, constraint, behavior, belief, or system resists change?
4. **What Could Be** — How could the audience's life, work, organization, or society become better?

Then answer the bridge question: **How do we get from here to there?**

## Output workflow

BlueSlide does not jump from raw requirements directly into slide design. It sizes the task first — a new deck gets the full sequence, while a single-slide or chart fix compresses the stages without skipping the thinking:

1. **Presentation brief** — audience, goal, context, scope, evidence, format, and constraints.
2. **Narrative spine** — the transformation the audience should experience.
3. **Slide map** — one assertion, evidence set, and visual intent per slide.
4. **Build** — PowerPoint, Google Slides, or another requested deliverable.
5. **Visual QA** — render, inspect, simplify, and correct every slide before delivery.

## Core design rules

- One primary message per slide.
- Approximately 70% quiet background, 25% main color, and 5% accent color.
- Blue as the primary visual language; complementary Gold Accent (`#FFB300`) only for the single focal element on a slide, never as text on a light background.
- Every text color meets 4.5:1 contrast against its background; color is never the only carrier of meaning.
- No pure-black text or icons, text gradients, or text shadows; one gold accent only.
- Type sized by role: 44–54 pt title and section slides, 36–40 pt assertion titles (at most two lines), 24–28 pt key text, never below 18 pt for message text and never below 12 pt for anything.
- Density follows delivery mode: a live-talk slide carries far fewer words than a standalone reading deck.
- No more than two typefaces; keep body text regular weight.
- Prefer direct labels, one hue per chart, chronological or value-based sorting, and zero-baseline bar charts.
- Prefer donut charts to pie charts, and use neither for more than five categories.
- Delete before shrinking: “Great writing is all about the power of the deleted word.”

The canonical palette, including which colors may be used as text on which backgrounds, is stored in [`assets/palette.json`](assets/palette.json). Check any custom color pair with:

```bash
python scripts/check_contrast.py '#071560' '#F5F5F5'
python scripts/check_contrast.py --palette   # verify every palette text role
```

Audit a built PowerPoint file for off-palette colors, undersized text, disallowed fonts, failing contrast, and default Office theme colors:

```bash
python scripts/audit_pptx.py deck.pptx
```

Both scripts need Python 3.8 or later and use only the standard library; installing the skill does not require them, but agents run them during QA.

## Install

BlueSlide ships a single root `SKILL.md` in the portable Agent Skills format,
so it installs identically across Claude, Antigravity, Codex, and any other
agent that adopts the standard.

### Skills CLI — recommended

The cross-agent [`skills`](https://github.com/vercel-labs/skills) CLI detects
your installed agents and installs BlueSlide for each of them:

```bash
# Install for every detected agent
npx skills add vpoonyak/blue-slide

# Or target specific agents
npx skills add vpoonyak/blue-slide -a claude-code
npx skills add vpoonyak/blue-slide -a codex

# Inspect what the repository exposes first
npx skills add vpoonyak/blue-slide --list
```

The CLI discovers exactly one root skill named `blue-slide`.

### Manual installation

Clone the repository into the agent's skills directory. Use the global path to
make BlueSlide available everywhere, or a project path to scope it to one repo.

**Claude (Claude Code / Claude apps)**

```bash
# Global
git clone https://github.com/vpoonyak/blue-slide.git ~/.claude/skills/blue-slide
# Project
git clone https://github.com/vpoonyak/blue-slide.git .claude/skills/blue-slide
```

**Google Antigravity**

```bash
# Global
git clone https://github.com/vpoonyak/blue-slide.git ~/.gemini/config/skills/blue-slide
# Project
git clone https://github.com/vpoonyak/blue-slide.git .agents/skills/blue-slide
```

**Codex**

```bash
# Global
git clone https://github.com/vpoonyak/blue-slide.git ~/.codex/skills/blue-slide
# Project
git clone https://github.com/vpoonyak/blue-slide.git .agents/skills/blue-slide
```

Restart or refresh the agent after installation so it can discover the skill.

## Use

Invoke the skill explicitly:

```text
Use $blue-slide to turn this report into a concise 10-slide executive presentation.
```

Other examples:

```text
Use $blue-slide to rewrite this pitch deck so every slide has one clear message.
```

```text
Use $blue-slide to redesign these charts and remove visual noise.
```

## Repository structure

```text
blue-slide/
├── .gitignore
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── assets/palette.json
├── references/
│   ├── examples.md
│   ├── infographics.md
│   ├── intake.md
│   ├── method.md
│   ├── narrative.md
│   ├── production.md
│   └── resource-directory.md
└── scripts/
    ├── audit_pptx.py
    └── check_contrast.py
```

## Influences

BlueSlide is an original skill informed by three presentation influences:

- **Nancy Duarte** — audience-centered narrative, the Big Idea, and tension between “what is” and “what could be.”
- **BetterPitch (*พูดด้วยภาพ*)** — decision-oriented investor logic, credible proof, risk, track record, and a precise ask.
- **Chang-Yang Lin** — visual clarity, flat icons, removal of decoration, and content distillation before design.

See [`references/method.md`](references/method.md) for the source links and working blend. BlueSlide is independent and is not affiliated with or endorsed by these creators or organizations.

## License

BlueSlide is released under the [MIT License](LICENSE).
