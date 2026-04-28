#!/usr/bin/env python3
"""
Skill Search - Keyword search via `npx skills find`
Wraps the skills CLI to provide structured JSON output for agent consumption.
"""

import os
import sys
import io
import re
import json
import shutil
import argparse
import subprocess
from dataclasses import dataclass, asdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


@dataclass
class SearchResult:
    source: str       # owner/repo
    skill_id: str     # skill name within repo
    installs: int     # install count
    url: str          # skills.sh URL
    is_installed: bool = False


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from string."""
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def get_installed_skills(skills_root: str) -> set:
    """Get set of installed skill names from local skills directory."""
    installed = set()
    if not os.path.exists(skills_root):
        return installed
    for item in os.listdir(skills_root):
        skill_dir = os.path.join(skills_root, item)
        if os.path.isdir(skill_dir):
            skill_md = os.path.join(skill_dir, "SKILL.md")
            if os.path.exists(skill_md):
                installed.add(item.lower())
    return installed


def _resolve_npx() -> str:
    """Resolve npx path, handling Windows Python subprocess PATH issues."""
    npx = shutil.which("npx")
    if npx:
        return npx
    for candidate in [
        os.path.join(os.environ.get("NVM_HOME", ""), "nodejs", "npx"),
        os.path.join(os.environ.get("PROGRAMFILES", ""), "nodejs", "npx.cmd"),
    ]:
        if os.path.exists(candidate):
            return candidate
    return "npx"


def search_skills(query: str, skills_root: str = None) -> list:
    """Search skills via `npx skills find` and parse results."""
    npx_path = _resolve_npx()
    try:
        result = subprocess.run(
            [npx_path, "skills", "find", query],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )
    except FileNotFoundError:
        print(f"Error: npx not found at {npx_path}. Install Node.js first.", file=sys.stderr)
        return []
    except subprocess.TimeoutExpired:
        print("Error: npx skills find timed out", file=sys.stderr)
        return []

    output = strip_ansi(result.stdout)

    installed = get_installed_skills(skills_root) if skills_root else set()

    results = []
    pattern = r'([^\s/]+/[^\s]+)@([^\s]+)\s+([\d.]+[KkMm]?)\s+installs'
    for match in re.finditer(pattern, output):
        source, skill_id, installs_str = match.groups()
        installs = parse_installs(installs_str)
        url = f"https://skills.sh/{source}/{skill_id}"
        is_installed = skill_id.lower() in installed
        results.append(SearchResult(
            source=source,
            skill_id=skill_id,
            installs=installs,
            url=url,
            is_installed=is_installed
        ))

    return results


def parse_installs(text: str) -> int:
    """Parse install count like '8.7K' or '500' to integer."""
    text = text.strip().lower()
    try:
        if 'k' in text:
            return int(float(text.replace('k', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '')) * 1000000)
        else:
            return int(text.replace(',', ''))
    except (ValueError, TypeError):
        return 0


def format_table(results: list) -> str:
    """Format search results as a readable table."""
    if not results:
        return "No skills found for this query."
    lines = []
    for i, r in enumerate(results, 1):
        status = " [Installed]" if r.is_installed else ""
        lines.append(f"{i}. {r.source}@{r.skill_id} ({r.installs:,} installs){status}")
        lines.append(f"   {r.url}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search skills via npx skills find")
    parser.add_argument("query", nargs="+", help="Search keywords")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    parser.add_argument("--skills-root", type=str, default=None, help="Path to skills directory")

    args = parser.parse_args()

    if args.skills_root is None:
        args.skills_root = os.path.expanduser(r"~\.claude\skills")

    query = " ".join(args.query)
    results = search_skills(query, args.skills_root)

    if args.format == "json":
        print(json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False))
    else:
        print(f"Search: \"{query}\" ({len(results)} results)\n")
        print(format_table(results))


if __name__ == "__main__":
    main()
