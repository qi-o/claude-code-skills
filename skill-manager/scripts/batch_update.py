#!/usr/bin/env python3
"""
Batch Update - Check and update all GitHub-based skills with dual-source support.

Delegates scanning/checking to scan_and_check.py (which has hash caching,
GITHUB_TOKEN support, master-priority, recursive scanning, local_only support).

When --auto-update is used, performs the actual update:
1. For each outdated skill, fetches upstream content
2. Backs up local SKILL.md
3. Outputs JSON with upstream content + diff metadata for Agent-driven merge
4. Updates github_hash in SKILL.md frontmatter
"""

import os
import sys
import io
import json
import argparse
import subprocess
import shutil
import datetime
import re

# Force UTF-8 encoding for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import scan_and_check as a sibling module
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from scan_and_check import scan_skills, check_updates
except ImportError:
    print("ERROR: Cannot import scan_and_check.py. Ensure it's in the same directory.", file=sys.stderr)
    sys.exit(1)


def _frontmatter_lines(content: str):
    """Split content into (frontmatter_str, body_str)."""
    parts = content.split('---', 2)
    if len(parts) < 3:
        return '', content
    return parts[1].strip(), '---'.join([''] + parts[2:])


def _update_hash_in_frontmatter(content: str, old_hash: str, new_hash: str) -> str:
    """Replace github_hash in SKILL.md frontmatter using regex to handle YAML type coercion."""
    # YAML may parse numeric-looking hashes (e.g., "0" or "1234567") as integers.
    # Use regex to match whatever is after "github_hash:" regardless of format.
    pattern = r'^(github_hash:\s*)\S+'
    return re.sub(pattern, rf'\g<1>{new_hash}', content, count=1, flags=re.MULTILINE)


def _update_secondary_hash(content: str, old_hash: str, new_hash: str, source_idx: int = 0) -> str:
    """Replace a secondary source hash in SKILL.md frontmatter using regex."""
    # Find the nth occurrence of "    hash: <value>" in the secondary_sources block
    matches = list(re.finditer(r'^(\s+hash:\s*)\S+', content, re.MULTILINE))
    if source_idx < len(matches):
        m = matches[source_idx]
        return content[:m.start()] + m.group(1) + new_hash + content[m.end():]
    return content


def fetch_upstream_readme(github_url: str, source_path: str = "") -> dict:
    """
    Fetch the upstream README/SKILL.md content from GitHub.

    Returns dict with keys: url, content, error
    """
    # Parse owner/repo from URL
    match = re.match(r'https://github\.com/([^/]+/[^/]+)', github_url)
    if not match:
        return {"url": github_url, "content": None, "error": f"Cannot parse GitHub URL: {github_url}"}

    repo = match.group(1).rstrip('/')

    # Determine file path to fetch
    file_path = source_path.strip('/') + '/SKILL.md' if source_path else 'README.md'
    # Also try SKILL.md at root
    paths_to_try = []
    if source_path:
        paths_to_try.append(f"{source_path.strip('/')}/SKILL.md")
    paths_to_try.extend(['SKILL.md', 'README.md'])

    token = os.environ.get('GITHUB_TOKEN', '')

    for path in paths_to_try:
        raw_url = f"https://raw.githubusercontent.com/{repo}/main/{path}"
        try:
            headers = []
            if token:
                headers = ['-H', f'Authorization: token {token}']
            cmd = ['curl', '-sL', '-w', '\\n%{http_code}'] + headers + [raw_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, encoding='utf-8')
            lines = result.stdout.rsplit('\n', 1)
            status_code = int(lines[-1].strip()) if lines else 0
            body = lines[0] if len(lines) > 1 else ''

            if status_code == 200 and body.strip():
                return {"url": raw_url, "content": body, "error": None}
        except Exception:
            continue

        # Try master branch
        raw_url = f"https://raw.githubusercontent.com/{repo}/master/{path}"
        try:
            cmd_base = ['curl', '-sL', '-w', '\\n%{http_code}']
            if token:
                cmd_base += ['-H', f'Authorization: token {token}']
            cmd_base.append(raw_url)
            result = subprocess.run(cmd_base, capture_output=True, text=True, timeout=15, encoding='utf-8')
            lines = result.stdout.rsplit('\n', 1)
            status_code = int(lines[-1].strip()) if lines else 0
            body = lines[0] if len(lines) > 1 else ''

            if status_code == 200 and body.strip():
                return {"url": raw_url, "content": body, "error": None}
        except Exception:
            continue

    return {"url": github_url, "content": None, "error": f"Could not fetch upstream content from {github_url}"}


def backup_skill_md(skill_dir: str) -> str:
    """Backup SKILL.md with timestamp. Returns backup path."""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return ""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(skill_dir, f"SKILL.md.bak.{timestamp}")
    shutil.copy2(skill_md, backup_path)
    return backup_path


def auto_update_skill(skill: dict) -> dict:
    """
    Perform auto-update for a single outdated skill.

    Strategy: hash-only update (fetch latest hash, update SKILL.md frontmatter).
    Also fetches upstream README/SKILL.md content and includes it in the JSON output
    so the calling Agent can do a content-level merge if needed.

    Returns dict with update result.
    """
    name = skill.get('name', 'unknown')
    skill_dir = skill.get('dir', '')
    github_url = skill.get('github_url', '')
    local_hash = skill.get('local_hash', '')
    primary_remote_hash = skill.get('primary_remote_hash') or skill.get('remote_hash')
    source_path = ''
    frontmatter_str, _ = _frontmatter_lines(
        open(os.path.join(skill_dir, 'SKILL.md'), 'r', encoding='utf-8').read()
    )
    for line in frontmatter_str.split('\n'):
        if line.strip().startswith('source:'):
            source_path = line.split(':', 1)[1].strip().strip('"').strip("'")

    result = {
        "name": name,
        "dir": skill_dir,
        "status": "skipped",
        "backup_path": "",
        "hash_updated": False,
        "upstream_content": None,
        "error": None
    }

    if not primary_remote_hash:
        result["error"] = "No remote hash available"
        return result

    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md_path):
        result["error"] = "SKILL.md not found"
        return result

    # Backup
    backup = backup_skill_md(skill_dir)
    result["backup_path"] = backup

    # Read current content
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update primary github_hash (always update if remote hash available)
    if primary_remote_hash and str(local_hash) != 'unknown':
        new_content = _update_hash_in_frontmatter(content, str(local_hash), primary_remote_hash)
        if new_content != content:
            content = new_content
            result["hash_updated"] = True

    # Update secondary hashes for fusion skills
    secondary_status = skill.get('secondary_status', {})
    secondary_sources = skill.get('secondary_sources', [])
    for idx_str, status_info in secondary_status.items():
        idx = int(idx_str)
        if idx < len(secondary_sources) and status_info.get('status') == 'outdated':
            old_h = secondary_sources[idx].get('hash', '')
            new_h = status_info.get('remote_hash', '')
            if old_h and new_h:
                content = _update_secondary_hash(content, old_h, new_h)
                result["hash_updated"] = True

    # Write updated content
    if result["hash_updated"]:
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Fetch upstream content for Agent-driven merge
    upstream = fetch_upstream_readme(github_url, source_path)
    result["upstream_content"] = upstream.get("content")
    result["upstream_fetch_error"] = upstream.get("error")

    result["status"] = "updated" if result["hash_updated"] else "no_change"
    return result


def format_report(results: list, update_results: list = None, auto_update: bool = False) -> str:
    """Format the update check report with optional update results."""
    if not results:
        return "No GitHub-based skills found."

    outdated = [s for s in results if s.get('status') == 'outdated']
    current = [s for s in results if s.get('status') == 'current']
    errors = [s for s in results if s.get('status') == 'error']

    lines = ["=" * 70, "Skill Update Report (Dual-Source Support)", "=" * 70, ""]

    lines.append(f"Total skills scanned: {len(results)}")
    lines.append(f"  - Up to date: {len(current)}")
    lines.append(f"  - Outdated: {len(outdated)}")
    lines.append(f"  - Errors: {len(errors)}")
    lines.append("")

    if outdated:
        lines.append("-" * 50)
        lines.append("OUTDATED SKILLS (need update):")
        lines.append("-" * 50)
        for skill in outdated:
            type_icon = "\U0001f517" if skill.get('type') == "fusion" else "\U0001f4e6"
            lines.append(f"  {type_icon} {skill['name']}")

            if skill.get('type') == 'fusion':
                outdated_sources = []
                if skill.get('primary_status') == 'outdated':
                    outdated_sources.append("primary")
                for idx, status in skill.get('secondary_status', {}).items():
                    if status.get('status') == 'outdated':
                        source_name = skill.get('secondary_sources', [{}])[int(idx)].get('name', f'source-{idx}')
                        outdated_sources.append(source_name)
                if outdated_sources:
                    lines.append(f"      Sources needing update: {', '.join(outdated_sources)}")

            lines.append(f"      URL: {skill.get('github_url', '')}")
            local_h = skill.get('local_hash', 'unknown')
            lines.append(f"      Local:  {local_h[:8]}...")
            remote_h = skill.get('primary_remote_hash') or skill.get('remote_hash', '')
            if remote_h:
                lines.append(f"      Remote: {remote_h[:8]}...")
            lines.append("")

    if update_results:
        lines.append("-" * 50)
        lines.append("UPDATE RESULTS:")
        lines.append("-" * 50)
        for r in update_results:
            status_icon = "\u2705" if r['status'] == 'updated' else "\u26a0\ufe0f" if r['status'] == 'no_change' else "\u274c"
            lines.append(f"  {status_icon} {r['name']}: {r['status']}")
            if r.get('hash_updated'):
                lines.append(f"      hash updated")
            if r.get('backup_path'):
                lines.append(f"      backup: {r['backup_path']}")
            if r.get('upstream_fetch_error'):
                lines.append(f"      upstream fetch: {r['upstream_fetch_error']}")
            if r.get('error'):
                lines.append(f"      error: {r['error']}")
        lines.append("")

    if errors:
        lines.append("-" * 50)
        lines.append("ERRORS:")
        lines.append("-" * 50)
        for skill in errors:
            lines.append(f"  * {skill.get('name', 'unknown')}: {skill.get('message', 'unknown error')}")
        lines.append("")

    if not auto_update and outdated:
        lines.append("-" * 50)
        lines.append("To update these skills:")
        lines.append("  - Use: /skill-manager batch-update")
        lines.append("  - Or: python batch_update.py --auto-update")
        lines.append("")

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
        args.skills_root = os.path.expanduser("~/.claude/skills")
        if os.name == 'nt' and not os.path.exists(args.skills_root):
            args.skills_root = os.path.expanduser(r"~\.claude\skills")

    # Delegate scanning/checking to scan_and_check.py
    skills = scan_skills(args.skills_root)
    results = check_updates(skills)

    update_results = []

    # Perform auto-update if requested
    if args.auto_update:
        outdated = [s for s in results if s.get('status') == 'outdated']
        if outdated:
            for skill in outdated:
                upd = auto_update_skill(skill)
                update_results.append(upd)

    # Output
    if args.format == "json":
        output = {
            "total": len(results),
            "outdated": [s for s in results if s.get('status') == 'outdated'],
            "current": [s for s in results if s.get('status') == 'current'],
            "errors": [s for s in results if s.get('status') == 'error']
        }
        if update_results:
            output["update_results"] = update_results
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_report(results, update_results, auto_update=args.auto_update))

    # Return exit code based on outdated count (0 if all updated)
    if args.auto_update:
        failed = len([r for r in update_results if r['status'] not in ('updated', 'no_change')])
        return failed
    else:
        outdated_count = len([s for s in results if s.get('status') == 'outdated'])
        return outdated_count


if __name__ == "__main__":
    sys.exit(main())
