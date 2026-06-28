# BlueSlide repository instructions

Maintain BlueSlide as one focused skill. Do not convert this repository into a multi-skill collection unless the project scope explicitly changes.

## Invariants

- Keep `SKILL.md` as the root skill entry point with only `name` and `description` in YAML frontmatter.
- Keep the execution order intact: presentation brief → narrative spine → slide map → build → visual QA.
- Load the full Grill Me intake only for new decks, incomplete or conflicting briefs, high-stakes presentations, or explicit Grill Me requests.
- Keep conceptual presentation attribution limited to BetterPitch (*พูดด้วยภาพ*), Nancy Duarte, and Chang-Yang Lin. Operational color, icon, and template sites may remain in `references/resource-directory.md`.
- Never commit photographed book pages, copyrighted reference decks, or third-party assets without explicit permission and a compatible license.
- Treat `assets/palette.json` as the canonical palette. Synchronize any palette change across `SKILL.md`, `README.md`, and `agents/openai.yaml` when applicable.
- Keep detailed frameworks in `references/`; keep the root skill concise and procedural.
- Update the repository tree and installation guidance in `README.md` whenever public files or installation behavior changes.
- Record every notable change in `CHANGELOG.md` under `[Unreleased]`, following [Keep a Changelog](https://keepachangelog.com/) and Semantic Versioning; promote `[Unreleased]` to a dated version when tagging a release.
- Keep installation paths consistent across agents: `~/.claude/skills/` (Claude), `~/.gemini/config/skills/` (Antigravity global) or `.agents/skills/` (project), and `~/.codex/skills/` (Codex). The root `SKILL.md` must remain the single portable entry point.
- Preserve external licensing and attribution requirements for every icon, image, template, and visual asset.

## Validation

Before committing:

```bash
python "$SKILL_CREATOR/scripts/quick_validate.py" .
npx skills add . --list
git diff --check
```

Set `SKILL_CREATOR` to the local skill-creator directory. If the official validator requires an unavailable dependency, run it in an isolated environment rather than adding that dependency to this repository.

Confirm that the Skills CLI discovers exactly one skill named `blue-slide` and that all relative links in `README.md` and `SKILL.md` resolve.
