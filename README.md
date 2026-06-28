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

BlueSlide does not jump from raw requirements directly into slide design:

1. **Presentation brief** — audience, goal, context, scope, evidence, format, and constraints.
2. **Narrative spine** — the transformation the audience should experience.
3. **Slide map** — one assertion, evidence set, and visual intent per slide.
4. **Build** — PowerPoint, Google Slides, or another requested deliverable.
5. **Visual QA** — render, inspect, simplify, and correct every slide before delivery.

## Core design rules

- One primary message per slide.
- Approximately 70% quiet background, 25% main color, and 5% accent color.
- Blue as the primary visual language; complementary yellow only for selective emphasis.
- No pure-black body text, text gradients, or text shadows.
- Default sizes: 44 pt title or section header, 36 pt headline, and 24 pt body text.
- No more than two typefaces; keep body text regular weight.
- Prefer direct labels, one hue per chart, chronological or value-based sorting, and zero-baseline bar charts.
- Prefer donut charts to pie charts, and use neither for more than five categories.
- Delete before shrinking: “Great writing is all about the power of the deleted word.”

The canonical palette is stored in [`assets/palette.json`](assets/palette.json).

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
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── README.md
├── SKILL.md
├── agents/openai.yaml
├── assets/palette.json
└── references/
    ├── infographics.md
    ├── intake.md
    ├── method.md
    ├── narrative.md
    └── resource-directory.md
```

## Influences

BlueSlide is an original skill informed by three presentation influences:

- **Nancy Duarte** — audience-centered narrative, the Big Idea, and tension between “what is” and “what could be.”
- **BetterPitch (*พูดด้วยภาพ*)** — decision-oriented investor logic, credible proof, risk, track record, and a precise ask.
- **Chang-Yang Lin** — visual clarity, flat icons, removal of decoration, and content distillation before design.

See [`references/method.md`](references/method.md) for the source links and working blend. BlueSlide is independent and is not affiliated with or endorsed by these creators or organizations.

## License

BlueSlide is released under the [MIT License](LICENSE).
