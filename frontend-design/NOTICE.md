frontend-design skill
Copyright 2025 Anthropic, PBC
Licensed under the Apache License, Version 2.0 (see LICENSE.txt).

## Modifications (by end-user, 2026-04-19)

This local installation has been modified from the upstream Anthropic source:

- Absorbed the prior `design-artifact` skill (user-authored) including:
  - HTML artifact 6-step workflow (Understand → Explore → Plan → Build → Verify → Summarize)
  - `questions_v2` clarification checklist (5 mandatory dimensions, 10 questions template)
  - Starter components: `deck_stage.js`, `design_canvas.jsx`, `animations.jsx`,
    and 4 device-frame JSX components (iOS, Android, macOS, browser)
  - `react-babel-guide.md` for inline JSX with pinned React 18.3.1 + Babel 7.29.0 + integrity hashes
  - Tweaks Protocol (postMessage + EDITMODE-BEGIN/END markers)
  - Supplementary anti-AI-slop rules
  - Design tokens reference with oklch color strategy (scoped as artifact fallback)
- Added `secondary_sources` entry for `react-best-practices` (vercel-labs/agent-skills)
- Added `triggers:` YAML list merging 12 HTML artifact keywords (English + Chinese)
- Added supplementary `reference/` files: `anti-slop.md`, `design-tokens.md`,
  `react-babel-guide.md`, `starter-patterns.md`, `workflow.md`
- Added `starters/` directory with scaffold components
- Demoted `design-tokens.md` font defaults (Geist-only, ban Fraunces etc.) to
  "artifact fallback" — `reference/typography.md` on distinctive font pairing
  remains PRIMARY authority
- Added Precedence Rule so `questions_v2` yields to existing DESIGN.md when present
- Version bump: 0.0.1 → 0.1.0 (minor, additive merge)

These modifications are local-only and not redistributed. If redistributed,
this NOTICE must accompany the skill per Apache 2.0 Section 4(b).

The provenance of the absorbed content (reverse-engineered Claude Artifacts
design system prompt via .zread project research) is recorded in
`evolution.json` fusion entry dated 2026-04-19.
