# Quality Guidelines for Skill Development

## Scope & Overlap

- Each skill should have a **single, well-defined purpose**
- Avoid overlapping functionality with existing skills
- If overlap is unavoidable, clearly document the differentiation

## Description Quality

A good description:
- Starts with a concrete action verb
- Names the specific technology/domain
- Describes the output or outcome
- Includes trigger conditions

**Bad**: "Handles documents"
**Good**: "Create, edit, and reformat DOCX documents using OpenXML SDK. Trigger when user mentions .docx files."

## File Size Awareness

- SKILL.md should be under 500 lines
- Reference documents should be under 1000 lines
- Long content should be split into multiple reference files

## Credential Handling

- API keys MUST come from environment variables
- Scripts MUST validate that credentials are present before use
- Never log or echo credential values

## Script Quality

- All Python scripts must have `#!/usr/bin/env python3` shebang
- All shell scripts must have proper shebang
- Each script must have a `--help` or `-h` flag
- Scripts should fail fast with clear error messages

## Language

- SKILL.md and references: **English**
- User-facing Chinese notes: acceptable in comments
- Variable/function names: English, snake_case for Python

## README Sync

If the skill has a README.md, ensure it stays in sync with SKILL.md. README is optional — SKILL.md is the source of truth.
