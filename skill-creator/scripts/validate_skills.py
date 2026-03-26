#!/usr/bin/env python3
"""validate_skills.py - Automated skill validation for SKILL.md files"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path

def validate_skill(dir_path: Path) -> list[str]:
    errors = []
    warnings = []

    skill_md = dir_path / "SKILL.md"

    # Check 1: SKILL.md exists
    if not skill_md.exists():
        errors.append(f"ERROR: SKILL.md not found in {dir_path}")
        return errors, warnings

    # Check 2: YAML frontmatter parseable
    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        errors.append(f"ERROR: SKILL.md must start with YAML frontmatter (---)")
        return errors, warnings

    try:
        frontmatter_end = content.index("---", 3)
        yaml_str = content[3:frontmatter_end].strip()
        frontmatter = yaml.safe_load(yaml_str)
    except Exception as e:
        errors.append(f"ERROR: YAML frontmatter parse error: {e}")
        return errors, warnings

    # Check 3: name field
    if "name" not in frontmatter:
        errors.append("ERROR: 'name' field missing from frontmatter")
    elif not frontmatter["name"]:
        errors.append("ERROR: 'name' field is empty")
    elif frontmatter["name"] != dir_path.name:
        errors.append(f"ERROR: 'name' field '{frontmatter['name']}' does not match directory '{dir_path.name}'")

    # Check 4: description field
    if "description" not in frontmatter:
        errors.append("ERROR: 'description' field missing from frontmatter")
    elif not frontmatter["description"]:
        errors.append("ERROR: 'description' field is empty")

    # Check 5: no hardcoded secrets
    # Only flag Bearer tokens in actual auth header context (not documentation text)
    bearer_pattern = r'(Authorization|Bearer)["\s:]+[a-zA-Z0-9_\-]{20,}'
    for line_num, line in enumerate(content.splitlines(), 1):
        if re.search(bearer_pattern, line, re.IGNORECASE):
            errors.append(f"ERROR: Potential Bearer token found at line {line_num}")

    # Check 6: license (warning)
    if "license" not in frontmatter:
        warnings.append("WARNING: 'license' field missing (recommended)")

    # Check 7: metadata completeness (warning)
    if "type" not in frontmatter:
        warnings.append("WARNING: 'type' field missing (recommended)")

    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Validate skill SKILL.md files")
    parser.add_argument("--dir", required=True, help="Path to skill directory")
    args = parser.parse_args()

    dir_path = Path(args.dir).resolve()
    if not dir_path.is_dir():
        print(f"ERROR: {dir_path} is not a directory")
        sys.exit(1)

    errors, warnings = validate_skill(dir_path)

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    if errors:
        sys.exit(1)
    print("Validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
