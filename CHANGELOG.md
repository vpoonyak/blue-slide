# Changelog

All notable changes to this project are documented in this file.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `CHANGELOG.md` to track notable changes across versions.
- Multi-agent installation guidance in `README.md` for Claude Code, Google
  Antigravity, and Codex, alongside the cross-agent `npx skills` CLI.

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
