# Skill Directory Structure Rules

## Required Structure

```
skills/<skill-name>/
├── SKILL.md              # REQUIRED - entry point with YAML frontmatter
├── scripts/              # OPTIONAL - executable scripts
│   ├── script1.py
│   └── script2.sh
├── references/          # OPTIONAL - detailed reference docs
│   ├── ref1.md
│   └── ref2.md
└── assets/              # OPTIONAL - static assets
    ├── template1.html
    └── image.png
```

## Naming Conventions

- Directory names: lowercase `kebab-case`
- SKILL.md: exactly `SKILL.md` (uppercase)
- Scripts: lowercase `snake_case.py` or `snake_case.sh`
- References: lowercase `kebab-case.md`

## ERROR-Level Rules (Blocking)

| Rule | Description |
|------|-------------|
| SKILL.md exists | Every skill directory must have a SKILL.md |
| YAML frontmatter | Must be valid YAML starting with `---` |
| name field | Must be present and match directory name |
| description field | Must be present and non-empty |
| No secrets | Must not contain `sk-`, `AKIA`, or Bearer tokens |

## WARNING-Level Rules (Recommended)

| Rule | Description |
|------|-------------|
| license field | Recommended in frontmatter |
| type field | Recommended in frontmatter |
| scripts/ directory | Scripts should be in dedicated directory |
| shebang | Python scripts should have `#!/usr/bin/env python3` |
