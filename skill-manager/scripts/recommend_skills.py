#!/usr/bin/env python3
"""
Skill Recommender - Discover popular skills from skills.sh
"""

import os
import sys
import io
import re
import json
import argparse
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Force UTF-8 encoding for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILLS_SH_URL = "https://skills.sh"

@dataclass
class RecommendedSkill:
    rank: int
    name: str
    source: str  # owner/repo
    installs: int
    github_url: str
    is_installed: bool = False


class SkillsShParser(HTMLParser):
    """Parse skills.sh HTML to extract skill information.

    skills.sh uses Next.js with data embedded in __next_f scripts.
    We extract JSON data containing skill objects with:
    - source: "owner/repo"
    - skillId: "skill-name"
    - name: "skill-name"
    - installs: 38271
    """

    def __init__(self):
        super().__init__()
        self.skills = []
        self.in_script = False
        self.script_content = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.in_script = True
            self.script_content = ""

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_script:
            self.in_script = False
            # Try to extract skill data from Next.js payload
            self._extract_skills_from_script(self.script_content)

    def handle_data(self, data):
        if self.in_script:
            self.script_content += data

    def _extract_skills_from_script(self, content):
        """Extract skill objects from Next.js script content."""
        # The data is escaped JSON like: \"source\":\"owner/repo\",\"skillId\":\"name\",\"installs\":123
        # Pattern for escaped JSON format
        pattern = r'\\"source\\":\\"([^"\\]+)\\",\\"skillId\\":\\"([^"\\]+)\\",\\"name\\":\\"([^"\\]+)\\",\\"installs\\":(\d+)'
        matches = re.findall(pattern, content)

        for match in matches:
            source, skill_id, name, installs = match
            # Avoid duplicates
            if not any(s.get('name') == name for s in self.skills):
                self.skills.append({
                    'source': source,
                    'name': name,
                    'installs': int(installs),
                    'github_url': f"https://github.com/{source}"
                })

        # Sort by installs descending and assign ranks
        self.skills.sort(key=lambda x: x.get('installs', 0), reverse=True)
        for i, skill in enumerate(self.skills, 1):
            skill['rank'] = i


def parse_install_count(text: str) -> int:
    """Parse install count string like '1.2k' or '500' to integer."""
    text = text.strip().lower()
    if not text:
        return 0
    try:
        if 'k' in text:
            return int(float(text.replace('k', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '')) * 1000000)
        else:
            return int(text.replace(',', ''))
    except ValueError:
        return 0


def fetch_skills_sh() -> str:
    """Fetch HTML content from skills.sh."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Claude-Code-Skill-Manager/1.0'
    }
    req = Request(SKILLS_SH_URL, headers=headers)
    try:
        with urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except (URLError, HTTPError) as e:
        print(f"Error fetching skills.sh: {e}", file=sys.stderr)
        return ""


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


def recommend_skills(limit: int = 20, skills_root: str = None, include_installed: bool = False) -> list:
    """Fetch and parse popular skills from skills.sh."""
    html = fetch_skills_sh()
    if not html:
        return []

    parser = SkillsShParser()
    parser.feed(html)

    # Get installed skills for marking
    if skills_root:
        installed = get_installed_skills(skills_root)
    else:
        installed = set()

    results = []
    for skill_data in parser.skills[:limit]:
        skill = RecommendedSkill(
            rank=skill_data.get('rank', 0),
            name=skill_data.get('name', ''),
            source=skill_data.get('source', ''),
            installs=skill_data.get('installs', 0),
            github_url=skill_data.get('github_url', ''),
            is_installed=skill_data.get('name', '').lower() in installed
        )
        if include_installed or not skill.is_installed:
            results.append(skill)

    return results


def format_table(skills: list) -> str:
    """Format skills as a table."""
    if not skills:
        return "No skills found."

    header = f"{'Rank':<6} | {'Name':<25} | {'Source':<30} | {'Installs':<10} | {'Status':<10}"
    lines = [header, "-" * len(header)]

    for skill in skills:
        status = "[Installed]" if skill.is_installed else ""
        lines.append(
            f"{skill.rank:<6} | {skill.name:<25} | {skill.source:<30} | {skill.installs:<10} | {status:<10}"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Discover popular skills from skills.sh")
    parser.add_argument("--limit", type=int, default=20, help="Number of skills to show (default: 20)")
    parser.add_argument("--format", choices=["table", "json"], default="table", help="Output format")
    parser.add_argument("--include-installed", action="store_true", help="Include already installed skills")
    parser.add_argument("--skills-root", type=str, default=None, help="Path to skills directory")

    args = parser.parse_args()

    # Default skills root
    if args.skills_root is None:
        args.skills_root = os.path.expanduser(r"~\.claude\skills")

    skills = recommend_skills(
        limit=args.limit,
        skills_root=args.skills_root,
        include_installed=args.include_installed
    )

    if args.format == "json":
        print(json.dumps([asdict(s) for s in skills], indent=2, ensure_ascii=False))
    else:
        print(format_table(skills))


if __name__ == "__main__":
    main()
