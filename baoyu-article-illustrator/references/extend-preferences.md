# EXTEND.md Preferences Loading

This document describes the standard EXTEND.md preference loading mechanism used by baoyu skills.

## Path Detection Priority

EXTEND.md files are searched in the following priority order:

### Shell Detection Commands

```bash
# macOS, Linux, WSL, Git Bash
test -f .baoyu-skills/{skill-name}/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/{skill-name}/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/{skill-name}/EXTEND.md" && echo "user"
```

```powershell
# PowerShell (Windows)
if (Test-Path .baoyu-skills/{skill-name}/EXTEND.md) { "project" }
$xdg = if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { "$HOME/.config" }
if (Test-Path "$xdg/baoyu-skills/{skill-name}/EXTEND.md") { "xdg" }
if (Test-Path "$HOME/.baoyu-skills/{skill-name}/EXTEND.md") { "user" }
```

### Location Priority Table

┌────────────────────────────────────────────────────────┬───────────────────┐
│                          Path                          │     Location      │
├────────────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/{skill-name}/EXTEND.md                   │ Project directory │
├────────────────────────────────────────────────────────┼───────────────────┤
│ $XDG_CONFIG_HOME/baoyu-skills/{skill-name}/EXTEND.md  │ XDG config home   │
├────────────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/{skill-name}/EXTEND.md             │ User home         │
└────────────────────────────────────────────────────────┴───────────────────┘

### Result Handling

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults (or run first-time setup if required)                        │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

## Skill-Specific Options

Each skill documents its own supported EXTEND.md settings. See the individual skill's SKILL.md for details on what configuration options are available.

**Note**: Replace `{skill-name}` in the paths above with the actual skill directory name (e.g., `baoyu-article-illustrator`, `baoyu-compress-image`, `baoyu-format-markdown`).
