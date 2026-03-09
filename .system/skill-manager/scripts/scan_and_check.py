import os
import sys
import yaml
import json
import subprocess
import concurrent.futures
import time
import hashlib
from typing import Dict, List, Optional, Tuple

# Cache file for remote hashes (TTL: 1 hour)
_CACHE_FILE = os.path.join(os.path.expanduser("~"), ".claude", "skills", ".system", "hash_cache.json")
_CACHE_TTL = 3600  # seconds

def _load_cache() -> Dict:
    try:
        if os.path.exists(_CACHE_FILE):
            with open(_CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _save_cache(cache: Dict) -> None:
    try:
        os.makedirs(os.path.dirname(_CACHE_FILE), exist_ok=True)
        with open(_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass

def _cache_key(url: str, branch: Optional[str]) -> str:
    return hashlib.md5(f"{url}#{branch or ''}".encode()).hexdigest()

def get_remote_hash(url: str, branch: str = None) -> Optional[str]:
    """
    Fetch the latest commit hash from the remote repository.
    Uses local cache (TTL 1h) and GITHUB_TOKEN if available to avoid rate limits.

    Priority order (unless branch is specified):
    1. refs/heads/master (stable branch)
    2. refs/heads/main (common default)
    3. HEAD (fallback to default branch)
    """
    # Check cache first
    cache = _load_cache()
    key = _cache_key(url, branch)
    if key in cache:
        entry = cache[key]
        if time.time() - entry.get('ts', 0) < _CACHE_TTL:
            return entry.get('hash')

    try:
        if branch:
            refs_to_try = [f'refs/heads/{branch}']
        else:
            refs_to_try = ['refs/heads/master', 'refs/heads/main', 'HEAD']

        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'
        env['GCM_INTERACTIVE'] = 'never'
        env['GIT_ASKPASS'] = 'echo'
        env['SSH_ASKPASS'] = 'echo'

        # Inject GITHUB_TOKEN as Basic auth for github.com URLs
        token = os.environ.get('GITHUB_TOKEN', '')
        authed_url = url
        if token and 'github.com' in url and url.startswith('https://'):
            authed_url = url.replace('https://', f'https://x-access-token:{token}@', 1)

        for ref in refs_to_try:
            result = subprocess.run(
                ['git', 'ls-remote', authed_url, ref],
                capture_output=True,
                text=True,
                timeout=15,
                env=env
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.split()
                if parts:
                    remote_hash = parts[0]
                    # Save to cache
                    cache[key] = {'hash': remote_hash, 'ts': time.time(), 'url': url}
                    _save_cache(cache)
                    return remote_hash

        return None
    except Exception:
        return None


def check_source_updates(local_hash: str, remote_url: str, branch: str = None) -> Tuple[str, str]:
    """
    Check if a source has updates.

    Args:
        local_hash: Local commit hash
        remote_url: Remote repository URL
        branch: Specific branch to check (optional)

    Returns:
        Tuple of (remote_hash, status)
        - remote_hash: Latest remote hash or None
        - status: 'current', 'outdated', or 'error'
    """
    remote_hash = get_remote_hash(remote_url, branch)

    if not remote_hash:
        return None, 'error'

    if remote_hash != local_hash:
        return remote_hash, 'outdated'

    return remote_hash, 'current'


def scan_skills(skills_root: str) -> List[Dict]:
    """
    Scan all subdirectories for SKILL.md and extract metadata.

    Supports dual-source tracking (primary + secondary_sources).
    Recursively scans subdirectories (e.g., .curated/, .experimental/).

    Args:
        skills_root: Root directory containing skills

    Returns:
        List of skill dictionaries with metadata
    """
    skill_list = []

    if not os.path.exists(skills_root):
        print(f"Skills root not found: {skills_root}", file=sys.stderr)
        return []

    def scan_directory(directory: str) -> None:
        """Recursively scan directory for skills."""
        for item in os.listdir(directory):
            skill_dir = os.path.join(directory, item)

            # Skip hidden directories and non-directories
            if item.startswith('.') or not os.path.isdir(skill_dir):
                continue

            skill_md = os.path.join(skill_dir, "SKILL.md")
            if not os.path.exists(skill_md):
                # Recursively scan subdirectories
                scan_directory(skill_dir)
                continue

            # Parse Frontmatter
            try:
                with open(skill_md, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract YAML between first two ---
                parts = content.split('---')
                if len(parts) < 3:
                    continue  # Invalid format

                frontmatter = yaml.safe_load(parts[1])

                # Check if managed by github-to-skills (has github_url)
                if 'github_url' not in frontmatter:
                    continue

                # Skip local-only skills (no remote to check)
                github_url = frontmatter.get('github_url', '')
                if frontmatter.get('local_only') or not github_url:
                    skill_list.append({
                        "name": frontmatter.get('name', item),
                        "dir": skill_dir,
                        "github_url": "",
                        "local_hash": "local",
                        "local_version": frontmatter.get('version', '0.0.0'),
                        "type": "local-only",
                        "status": "current",
                        "message": "Local-only skill (no remote)"
                    })
                    continue

                skill_info = {
                    "name": frontmatter.get('name', item),
                    "dir": skill_dir,
                    "github_url": github_url,
                    "local_hash": frontmatter.get('github_hash', 'unknown'),
                    "local_version": frontmatter.get('version', '0.0.0'),
                    "type": "single-source"
                }

                # Check for secondary sources (fusion skills)
                secondary_sources = frontmatter.get('secondary_sources', [])
                if secondary_sources:
                    skill_info["type"] = "fusion"
                    skill_info["secondary_sources"] = []
                    for source in secondary_sources:
                        skill_info["secondary_sources"].append({
                            "name": source.get('name', 'unknown'),
                            "url": source['url'],
                            "local_hash": source['hash'],
                            "contributions": source.get('contributions', [])
                        })

                skill_list.append(skill_info)

            except Exception as e:
                # print(f"Skipping {item}: {e}", file=sys.stderr)
                pass

    # Start scanning from root and also scan subdirectories
    scan_directory(skills_root)

    # Also scan .curated and .experimental subdirectories
    for subdir in ['.curated', '.experimental']:
        subdir_path = os.path.join(skills_root, subdir)
        if os.path.isdir(subdir_path):
            scan_directory(subdir_path)

    return skill_list


def check_updates(skills: List[Dict]) -> List[Dict]:
    """
    Check for updates concurrently for all skills and their sources.

    For fusion skills with secondary sources, checks all sources
    and reports update status for each.

    Args:
        skills: List of skill dictionaries from scan_skills()

    Returns:
        List of skill dictionaries with update status
    """
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Collect all sources to check (primary + secondary)
        checks = []

        for skill in skills:
            # Skip local-only skills (already have status set)
            if skill.get('type') == 'local-only':
                results.append(skill)
                continue

            # Primary source check
            future = executor.submit(
                check_source_updates,
                skill['local_hash'],
                skill['github_url']
            )
            checks.append((future, skill, 'primary'))

            # Secondary sources checks (for fusion skills)
            if skill.get('type') == 'fusion':
                for idx, source in enumerate(skill.get('secondary_sources', [])):
                    future = executor.submit(
                        check_source_updates,
                        source['local_hash'],
                        source['url']
                    )
                    checks.append((future, skill, ('secondary', idx)))

        # Process results
        for future, skill, source_type in checks:
            try:
                remote_hash, status = future.result()

                if source_type == 'primary':
                    skill['primary_remote_hash'] = remote_hash
                    skill['primary_status'] = status
                else:
                    source_idx = source_type[1]
                    if 'secondary_status' not in skill:
                        skill['secondary_status'] = {}
                    skill['secondary_status'][source_idx] = {
                        'remote_hash': remote_hash,
                        'status': status
                    }

            except Exception as e:
                if source_type == 'primary':
                    skill['primary_status'] = 'error'
                    skill['primary_error'] = str(e)
                else:
                    source_idx = source_type[1]
                    if 'secondary_status' not in skill:
                        skill['secondary_status'] = {}
                    skill['secondary_status'][source_idx] = {
                        'status': 'error',
                        'error': str(e)
                    }

    # Determine overall status for each skill
    for skill in skills:
        # Skip local-only skills (already processed and added to results)
        if skill.get('type') == 'local-only':
            continue

        primary_status = skill.get('primary_status', 'error')

        if skill.get('type') == 'fusion':
            # For fusion skills, check all sources
            secondary_statuses = skill.get('secondary_status', {})

            # Overall status is outdated if ANY source is outdated
            any_outdated = primary_status == 'outdated'
            any_error = primary_status == 'error'

            for idx, status_info in secondary_statuses.items():
                if status_info['status'] == 'outdated':
                    any_outdated = True
                elif status_info['status'] == 'error':
                    any_error = True

            if any_outdated:
                skill['status'] = 'outdated'
                skill['message'] = 'Updates available from one or more sources'
            elif any_error:
                skill['status'] = 'error'
                skill['message'] = 'Could not check one or more sources'
            else:
                skill['status'] = 'current'
                skill['message'] = 'All sources up to date'
        else:
            # Single-source skills
            skill['status'] = primary_status
            skill['remote_hash'] = skill.get('primary_remote_hash')

            if primary_status == 'outdated':
                skill['message'] = 'New commits available'
            elif primary_status == 'error':
                skill['message'] = 'Could not reach remote'
            else:
                skill['message'] = 'Up to date'

        results.append(skill)

    return results


def format_report(results: List[Dict], format_type: str = 'table') -> str:
    """
    Format the update check results.

    Args:
        results: List of skill dictionaries with status
        format_type: 'table', 'json', or 'summary'

    Returns:
        Formatted report string
    """
    if format_type == 'json':
        return json.dumps(results, indent=2, ensure_ascii=False)

    elif format_type == 'summary':
        current = [s for s in results if s['status'] == 'current']
        outdated = [s for s in results if s['status'] == 'outdated']
        errors = [s for s in results if s['status'] == 'error']

        summary = []
        summary.append(f"📊 Update Check Summary")
        summary.append(f"")
        summary.append(f"Total skills: {len(results)}")
        summary.append(f"✅ Current: {len(current)}")
        summary.append(f"⚠️  Outdated: {len(outdated)}")
        summary.append(f"❌ Errors: {len(errors)}")
        summary.append(f"")

        if outdated:
            summary.append(f"📦 Outdated Skills:")
            for skill in outdated:
                summary.append(f"  - {skill['name']}")

                # Show which sources are outdated
                if skill.get('type') == 'fusion':
                    outdated_sources = []
                    if skill.get('primary_status') == 'outdated':
                        outdated_sources.append('primary')
                    for idx, status in skill.get('secondary_status', {}).items():
                        if status['status'] == 'outdated':
                            source_name = skill['secondary_sources'][idx]['name']
                            outdated_sources.append(source_name)
                    if outdated_sources:
                        summary.append(f"    Sources needing update: {', '.join(outdated_sources)}")

        if errors:
            summary.append(f"")
            summary.append(f"❌ Errors:")
            for skill in errors:
                summary.append(f"  - {skill['name']}: {skill.get('message', 'Unknown error')}")

        return '\n'.join(summary)

    else:  # table format
        lines = []
        lines.append(f"{'Name':<30} {'Type':<15} {'Status':<10} {'Message'}")
        lines.append("-" * 100)

        for skill in results:
            type_label = skill.get('type', 'single-source')
            if type_label == 'fusion':
                type_label = 'fusion 🔗'

            status_icon = {
                'current': '✅',
                'outdated': '⚠️ ',
                'error': '❌'
            }.get(skill['status'], '❓')

            lines.append(f"{skill['name']:<30} {type_label:<15} {status_icon} {skill['message']}")

        return '\n'.join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Scan skills and check for updates')
    parser.add_argument('skills_dir', nargs='?',
                        help='Path to skills directory')
    parser.add_argument('--format', choices=['table', 'json', 'summary'],
                        default='table',
                        help='Output format (default: table)')
    parser.add_argument('--output', '-o',
                        help='Write output to file')

    args = parser.parse_args()

    # Determine skills directory
    if args.skills_dir:
        target_dir = args.skills_dir
    else:
        # Try default paths
        default_paths = [
            os.path.expanduser("~/.claude/skills"),
            os.path.expanduser("~/.config/opencode/skills"),
            r"C:\Users\ZDS\.claude\skills"
        ]
        target_dir = None
        for path in default_paths:
            if os.path.exists(path):
                target_dir = path
                break

        if not target_dir:
            print("Error: Could not find skills directory", file=sys.stderr)
            print("Please specify skills_dir explicitly", file=sys.stderr)
            sys.exit(1)

    # Scan and check
    skills = scan_skills(target_dir)
    if not skills:
        print("No skills found with github_url metadata", file=sys.stderr)
        sys.exit(0)

    updates = check_updates(skills)

    # Format and output
    report = format_report(updates, args.format)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)
