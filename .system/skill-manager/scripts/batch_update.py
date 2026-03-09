#!/usr/bin/env python3
"""
Batch Update - Check and update all GitHub-based skills with dual-source support
"""

import os
import sys
import io
import json
import argparse
import subprocess
import concurrent.futures
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

# Force UTF-8 encoding for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


@dataclass
class SourceInfo:
    """Information about a source repository."""
    name: str
    url: str
    local_hash: str
    remote_hash: Optional[str] = None
    status: str = "unknown"  # current, outdated, error


@dataclass
class SkillStatus:
    """Status of a skill with all its sources."""
    name: str
    dir: str
    github_url: str
    local_hash: str
    type: str = "single-source"  # single-source or fusion
    primary_status: str = "unknown"
    primary_remote_hash: Optional[str] = None
    secondary_sources: List[SourceInfo] = field(default_factory=list)
    secondary_status: Dict[int, Dict] = field(default_factory=dict)
    status: str = "unknown"  # current, outdated, error
    message: str = ""


def parse_yaml_frontmatter(content: str) -> dict:
    """Simple YAML frontmatter parser without external dependencies."""
    parts = content.split('---')
    if len(parts) < 3:
        return {}

    yaml_content = parts[1].strip()
    result = {}

    for line in yaml_content.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value

    return result


def parse_list_value(value: str) -> list:
    """Parse a YAML list value."""
    value = value.strip()
    if value.startswith('[') and value.endswith(']'):
        # Remove brackets and split
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = [item.strip().strip('"').strip("'") for item in inner.split(',')]
        return items
    return []


def get_remote_hash(url: str) -> Optional[str]:
    """Fetch the latest commit hash from the remote repository."""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', url, 'HEAD'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return None
        parts = result.stdout.split()
        if parts:
            return parts[0]
        return None
    except Exception:
        return None


def scan_github_skills(skills_root: str) -> List[SkillStatus]:
    """Scan all subdirectories for GitHub-based skills with dual-source support."""
    skill_list = []

    if not os.path.exists(skills_root):
        print(f"Skills root not found: {skills_root}", file=sys.stderr)
        return []

    for item in os.listdir(skills_root):
        skill_dir = os.path.join(skills_root, item)
        if not os.path.isdir(skill_dir):
            continue

        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_md):
            continue

        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()

            frontmatter = parse_yaml_frontmatter(content)

            if 'github_url' not in frontmatter:
                continue

            # Check for secondary sources (fusion skills)
            has_secondary = 'secondary_sources' in content

            skill = SkillStatus(
                name=frontmatter.get('name', item),
                dir=skill_dir,
                github_url=frontmatter['github_url'],
                local_hash=frontmatter.get('github_hash', 'unknown'),
                type="fusion" if has_secondary else "single-source"
            )

            # Parse secondary sources if present
            if has_secondary:
                # Find secondary_sources block in content
                lines = content.split('\n')
                in_secondary = False
                current_source = None
                idx = 0

                for line in lines:
                    line = line.strip()
                    if line.startswith('secondary_sources:'):
                        in_secondary = True
                        continue
                    elif in_secondary:
                        if line.startswith('- name:'):
                            current_source = SourceInfo(
                                name=line.split(':', 1)[1].strip(),
                                url="",
                                local_hash=""
                            )
                        elif current_source and line.startswith('url:'):
                            current_source.url = line.split(':', 1)[1].strip().strip('"').strip("'")
                        elif current_source and line.startswith('hash:'):
                            current_source.local_hash = line.split(':', 1)[1].strip().strip('"').strip("'")
                        elif current_source and line.startswith('contributions:'):
                            # Parse contributions list
                            current_source.contributions = parse_list_value(line.split(':', 1)[1].strip())
                        elif current_source and line.startswith('-'):
                            # Next source starts
                            skill.secondary_sources.append(current_source)
                            idx += 1
                        elif not line.startswith(' ') and not line.startswith('\t'):
                            # End of block
                            if current_source:
                                skill.secondary_sources.append(current_source)
                            break

            skill_list.append(skill)

        except Exception as e:
            print(f"Skipping {item}: {e}", file=sys.stderr)
            pass

    return skill_list


def check_updates(skills: List[SkillStatus]) -> List[SkillStatus]:
    """Check for updates concurrently for all sources."""
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Collect all checks to perform
        checks = []

        for skill in skills:
            # Primary source check
            future = executor.submit(get_remote_hash, skill.github_url)
            checks.append((future, skill, 'primary'))

            # Secondary sources checks (for fusion skills)
            for idx, source in enumerate(skill.secondary_sources):
                future = executor.submit(get_remote_hash, source.url)
                checks.append((future, skill, ('secondary', idx)))

        # Process results
        for future, skill, source_type in checks:
            try:
                remote_hash = future.result()

                if source_type == 'primary':
                    skill.primary_remote_hash = remote_hash
                    if not remote_hash:
                        skill.primary_status = 'error'
                    elif remote_hash != skill.local_hash:
                        skill.primary_status = 'outdated'
                    else:
                        skill.primary_status = 'current'
                else:
                    source_idx = source_type[1]
                    source = skill.secondary_sources[source_idx]
                    source.remote_hash = remote_hash

                    status = 'error'
                    if remote_hash:
                        status = 'outdated' if remote_hash != source.local_hash else 'current'

                    skill.secondary_status[source_idx] = {
                        'remote_hash': remote_hash,
                        'status': status
                    }

            except Exception as e:
                if source_type == 'primary':
                    skill.primary_status = 'error'
                else:
                    source_idx = source_type[1]
                    skill.secondary_status[source_idx] = {
                        'remote_hash': None,
                        'status': 'error',
                        'error': str(e)
                    }

    # Determine overall status
    for skill in skills:
        if skill.type == 'fusion':
            # For fusion skills, check all sources
            any_outdated = skill.primary_status == 'outdated'
            any_error = skill.primary_status == 'error'

            for idx, status_info in skill.secondary_status.items():
                if status_info['status'] == 'outdated':
                    any_outdated = True
                elif status_info['status'] == 'error':
                    any_error = True

            if any_outdated:
                skill.status = 'outdated'
                skill.message = 'Updates available from one or more sources'
            elif any_error:
                skill.status = 'error'
                skill.message = 'Could not check one or more sources'
            else:
                skill.status = 'current'
                skill.message = 'All sources up to date'
        else:
            # Single-source skills
            skill.status = skill.primary_status
            skill.remote_hash = skill.primary_remote_hash

            if skill.primary_status == 'outdated':
                skill.message = 'New commits available'
            elif skill.primary_status == 'error':
                skill.message = 'Could not reach remote'
            else:
                skill.message = 'Up to date'

        results.append(skill)

    return results


def format_report(skills: List[SkillStatus], check_only: bool = True) -> str:
    """Format the update check report with dual-source information."""
    if not skills:
        return "No GitHub-based skills found."

    outdated = [s for s in skills if s.status == 'outdated']
    current = [s for s in skills if s.status == 'current']
    errors = [s for s in skills if s.status == 'error']

    lines = ["=" * 70, "Skill Update Report (Dual-Source Support)", "=" * 70, ""]

    lines.append(f"Total skills scanned: {len(skills)}")
    lines.append(f"  - Up to date: {len(current)}")
    lines.append(f"  - Outdated: {len(outdated)}")
    lines.append(f"  - Errors: {len(errors)}")
    lines.append("")

    if outdated:
        lines.append("-" * 50)
        lines.append("OUTDATED SKILLS (need update):")
        lines.append("-" * 50)
        for skill in outdated:
            type_icon = "🔗" if skill.type == "fusion" else "📦"
            lines.append(f"  {type_icon} {skill.name}")

            if skill.type == "fusion":
                # Show which sources are outdated
                outdated_sources = []
                if skill.primary_status == 'outdated':
                    outdated_sources.append("primary")
                for idx, status in skill.secondary_status.items():
                    if status['status'] == 'outdated':
                        source_name = skill.secondary_sources[idx].name
                        outdated_sources.append(source_name)
                if outdated_sources:
                    lines.append(f"      Sources needing update: {', '.join(outdated_sources)}")

            lines.append(f"      URL: {skill.github_url}")
            lines.append(f"      Local:  {skill.local_hash[:8]}...")
            if skill.primary_remote_hash:
                lines.append(f"      Remote: {skill.primary_remote_hash[:8]}...")
            lines.append("")

    if errors:
        lines.append("-" * 50)
        lines.append("ERRORS:")
        lines.append("-" * 50)
        for skill in errors:
            lines.append(f"  * {skill.name}: {skill.message}")
        lines.append("")

    if check_only and outdated:
        lines.append("-" * 50)
        lines.append("To update these skills:")
        lines.append("  - Use: /skill-manager batch-update")
        lines.append("  - Or: python batch_update.py --auto-update")
        lines.append("")
        lines.append("For fusion skills, review changes from all sources before updating.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Batch check and update GitHub-based skills")
    parser.add_argument("skills_root", nargs="?", default=None, help="Path to skills directory")
    parser.add_argument("--check-only", action="store_true", help="Only check for updates, don't update")
    parser.add_argument("--auto-update", action="store_true", help="Automatically update outdated skills")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Default skills root
    if args.skills_root is None:
        args.skills_root = os.path.expanduser(r"~\.claude\skills")

    # Scan and check
    skills = scan_github_skills(args.skills_root)
    results = check_updates(skills)

    if args.format == "json":
        output = {
            "total": len(results),
            "outdated": [asdict(s) for s in results if s.status == 'outdated'],
            "current": [asdict(s) for s in results if s.status == 'current'],
            "errors": [asdict(s) for s in results if s.status == 'error']
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_report(results, check_only=not args.auto_update))

    # Return exit code based on outdated count
    outdated_count = len([s for s in results if s.status == 'outdated'])
    return outdated_count


if __name__ == "__main__":
    sys.exit(main())
