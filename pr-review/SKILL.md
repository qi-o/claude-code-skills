---
name: pr-review
description: Skill PR review workflow — automated validation + manual content review for skill submissions. Trigger when submitting or reviewing new skills.
type: skill
github_url: https://github.com/MiniMax-AI/skills
github_hash: b4c7c3fcd4d8c1f6e2a3d7b9c5e1f4a8d2b7c3e9
version: 1.0.0
---

# PR Review Skill

Two-phase review process for validating skill submissions.

## Phase 1: Automated Validation

Run the validation script against the skill directory:

```bash
python C:/Users/ZDS/.claude/skills/pr-review/scripts/validate_skills.py --dir /path/to/skill
```

### Validation Checks

| Check | Error Level | Description |
|-------|------------|-------------|
| SKILL.md exists | ERROR | Every skill must have a SKILL.md file |
| YAML frontmatter parseable | ERROR | YAML must be valid |
| `name` field present | ERROR | Must have non-empty name |
| `name` matches directory | ERROR | Directory name must match skill name |
| `description` field present | ERROR | Must have non-empty description |
| No hardcoded secrets | ERROR | No `sk-`, `AKIA`, or Bearer tokens |
| `license` field | WARNING | Recommended |
| `metadata` completeness | WARNING | Check completeness |

### Exit Codes

- `0`: All checks passed
- `1`: Validation failed with errors

## Phase 2: Manual Content Review

After automated validation passes, review against quality guidelines:

1. **Scope**: Does the skill have clear, focused scope?
2. **Trigger**: Are trigger conditions specific and unambiguous?
3. **Completeness**: Are all referenced files/scripts present?
4. **Language**: Is documentation in English with consistent terminology?
5. **Credential handling**: Are there clear rules about secrets/API keys?

See `references/quality-guidelines.md` and `references/structure-rules.md` for full checklists.

## Submission Checklist

Before submitting a new skill:
- [ ] `validate_skills.py --dir <skill-dir>` exits 0
- [ ] SKILL.md has valid YAML frontmatter with name + description
- [ ] All referenced scripts exist and have correct paths
- [ ] No hardcoded credentials
- [ ] Trigger conditions clearly described
