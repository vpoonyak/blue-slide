# Changelog

All notable changes to this project are documented in this file.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `CHANGELOG.md` to track notable changes across versions.
- Multi-agent installation guidance in `README.md` for Claude Code, Google
  Antigravity, and Codex, alongside the cross-agent `npx skills` CLI.
- Canonical Gold Accent `#FFB300` from the BlueSlide house palette, and a
  derived text-safe amber `#8A5A00` in `assets/palette.json`, plus explicit color roles (`text_on_light`,
  `text_on_panel`, `text_on_dark`, `fill_only_on_light`) and measured
  contrast ratios.
- `scripts/check_contrast.py` to verify WCAG contrast for custom color pairs
  and for every palette text role.
- `references/production.md`: density budgets by delivery mode, 16:9 grid and
  margins, Calibri/Kanit fallbacks and Thai line spacing, color-by-role rules,
  accessibility checks, and a LibreOffice rendering path for visual QA.
- `references/examples.md`: a worked brief → spine → slide map, a single-slide
  rewrite, and assertion-title examples.
- Task-scope table in `SKILL.md` so slide-level edits and chart fixes compress
  the workflow instead of producing a full brief and slide map, with an
  explicit approval-gate column.
- `scripts/audit_pptx.py`: a standard-library .pptx audit of slides and
  embedded charts for off-palette colors, pure black, text below 12 pt,
  undersized message text (Thai-aware), disallowed fonts, failing text
  contrast on explicit and theme-styled fills, cluttered labeled charts, and
  theme colors that differ from the palette.
- `.gitignore` for Python bytecode caches.
- `pptx_theme` in `assets/palette.json`, mapping BlueSlide colors onto
  PowerPoint and Google Slides theme slots so tool defaults such as Office blue
  `#4F81BD` never appear.
- Role-based type scale, reusable slide patterns, and a common-defects QA list
  drawn from reviewing a real BlueSlide deck.

### Changed

- Titles and body text now use deep navy or charcoal; the accent is reserved
  for one focal element per slide. The previous rule set titles in the accent
  color, which fails contrast for gold on light backgrounds (1.79:1 on white).
- Cool light grays (`#D1D5D8`, `#CBCDCF`) are now panel colors rather than
  slide backgrounds, because primary blue text falls below 4.5:1 on them.
- Visual QA requires rendered slide images, or an explicit statement of which
  checks could not be performed.
- Type sizing is now by role: assertion titles 36–40 pt (at most two lines),
  title and section slides 44–54 pt, message text at least 18 pt, and nothing
  below 12 pt, replacing the single 44 / 36 / 24 pt scale.
- Content margins are 1.0 in left and right, with an outer 0.5 in band reserved
  for section labels, citations, logos, and slide numbers.
- Only one gold accent is allowed, pure black is banned for icons as well as
  text, and low-contrast chart marks are allowed only when directly labeled.
- Mid gray `#858487` is a fill, divider, and chart color only, not text.

### Removed

- `roles.preferred_complementary_accent_hue` and
  `roles.preferred_complementary_accent_hex` from `assets/palette.json`,
  superseded by `roles.accent` and `colors.gold_accent`.

### Fixed

- `scripts/audit_pptx.py` no longer crashes on decks whose relationship
  targets are package-absolute (for example `/ppt/charts/chart1.xml`, as
  written by pptxgenjs) or contain `.` segments.
- `scripts/audit_pptx.py` reports a link to a part missing from the file as
  an error and keeps auditing, instead of crashing.

## [0.1.0] - 2026-06-28

### Added

- Root `SKILL.md` BlueSlide skill: a blue-first, one-message-per-slide
  presentation method with `name` and `description` frontmatter.
- Required output sequence — presentation brief → narrative spine → slide map
  → build → visual QA — so an agent never jumps from requirements straight to
  slides.
- Four-stage narrative framework: Goal → What Is → Build the Opponent →
  What Could Be, plus the "how do we get there" bridge.
- Grill Me intake interview, loaded conditionally for new decks, conflicting
  or incomplete briefs, and high-stakes presentations (not for small edits).
- Reference library under `references/`: `method.md`, `intake.md`,
  `narrative.md`, `infographics.md`, and `resource-directory.md`.
- Canonical 70:25:5 palette in `assets/palette.json`.
- Codex interface metadata in `agents/openai.yaml`.
- `AGENTS.md` maintenance invariants: single-skill scope, intact execution
  order, three conceptual influences, validation steps, README synchronization,
  and a prohibition on committing copyrighted reference pages.
- "Grill Me" and presentation-intake triggers in the skill description.
- `LICENSE` (MIT) granting reuse rights for the public repository.
- `README.md` documenting the method, narrative framework, output workflow,
  design rules, and installation.

[Unreleased]: https://github.com/vpoonyak/blue-slide/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/vpoonyak/blue-slide/releases/tag/v0.1.0
