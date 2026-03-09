#!/usr/bin/env python3
"""
fetch_repo_info.py - Enhanced repository information fetcher with multi-platform and mirror support.

Supports:
- GitHub (with 8+ API mirrors and 3 raw content mirrors)
- GitLab (with API mirrors)
- Gitee (native support)

Usage:
    python fetch_repo_info.py <repository_url>
    python fetch_repo_info.py https://github.com/owner/repo
    python fetch_repo_info.py https://gitlab.com/owner/repo
    python fetch_repo_info.py https://gitee.com/owner/repo
"""

import sys
import json
import subprocess
import re
import urllib.request
import urllib.error
import os
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class MirrorConfig:
    """Mirror configuration loader."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "mirrors.json")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        self.mirrors = config['mirrors']
        self.retry_config = config['retry_strategy']
        self.version = config['version']

    def get_api_mirrors(self, platform: str) -> List[Dict]:
        """Get API mirrors for a platform, sorted by priority."""
        mirrors = self.mirrors.get(platform, {}).get('api', [])
        return sorted(mirrors, key=lambda x: x['priority'])

    def get_raw_mirrors(self, platform: str) -> List[Dict]:
        """Get raw content mirrors for a platform."""
        mirrors = self.mirrors.get(platform, {}).get('raw', [])
        return sorted(mirrors, key=lambda x: x['priority'])

    def get_retry_config(self) -> Dict:
        """Get retry configuration."""
        return self.retry_config


class RepoParser:
    """Parse repository URLs and detect platform."""

    # Platform detection patterns
    PLATFORM_PATTERNS = {
        'github': re.compile(r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)'),
        'gitlab': re.compile(r'(?:https?://)?(?:www\.)?gitlab\.com/([^/]+)/([^/]+)'),
        'gitee': re.compile(r'(?:https?://)?(?:www\.)?gitee\.com/([^/]+)/([^/]+)')
    }

    @classmethod
    def parse_url(cls, url: str) -> Optional[Dict]:
        """
        Parse repository URL and extract platform, owner, repo name.

        Args:
            url: Repository URL

        Returns:
            Dict with platform, owner, repo, and qualified_name, or None if invalid
        """
        url = url.rstrip('/')
        if url.endswith('.git'):
            url = url[:-4]

        for platform, pattern in cls.PLATFORM_PATTERNS.items():
            match = pattern.match(url)
            if match:
                owner, repo = match.groups()
                return {
                    'platform': platform,
                    'owner': owner,
                    'repo': repo,
                    'qualified_name': f"{owner}/{repo}",
                    'original_url': url
                }

        return None


class MirrorRotator:
    """Handle mirror rotation with retry logic."""

    def __init__(self, config: MirrorConfig):
        self.config = config
        self.retry_config = config.get_retry_config()

    def fetch_with_rotation(
        self,
        mirrors: List[Dict],
        path_builder,
        max_failures: int = 3
    ) -> Tuple[Optional[str], Optional[Dict]]:
        """
        Fetch from mirrors with automatic rotation and retry.

        Args:
            mirrors: List of mirror configs
            path_builder: Function that takes mirror_url and returns full URL
            max_failures: Max consecutive failures before switching mirrors

        Returns:
            Tuple of (content, mirror_info) or (None, None) if all failed
        """
        consecutive_failures = 0
        backoff_delays = self.retry_config['backoff_delays']
        max_retries = self.retry_config['max_retries_per_mirror']
        timeout = self.retry_config['timeout_seconds']

        for mirror in mirrors:
            mirror_url = mirror['url']
            mirror_name = mirror.get('name', 'unknown')

            for attempt in range(max_retries):
                try:
                    full_url = path_builder(mirror_url)

                    request = urllib.request.Request(
                        full_url,
                        headers={
                            'Accept': 'application/vnd.github.v3+json',
                            'User-Agent': 'repo2skill/1.0'
                        }
                    )

                    with urllib.request.urlopen(request, timeout=timeout) as response:
                        content = response.read().decode('utf-8')

                        # Reset failure count on success
                        consecutive_failures = 0

                        return content, mirror

                except urllib.error.HTTPError as e:
                    if e.code in (403, 429):
                        # Rate limit - try next mirror
                        consecutive_failures += 1
                        if consecutive_failures >= max_failures:
                            break
                    elif e.code == 404:
                        # Not found - don't retry
                        return None, {'error': f'Not found: {full_url}'}
                    else:
                        consecutive_failures += 1

                except (urllib.error.URLError, TimeoutError) as e:
                    consecutive_failures += 1

                # Apply backoff delay
                if attempt < len(backoff_delays):
                    time.sleep(backoff_delays[attempt])

        return None, None


class RepoFetcher:
    """Fetch repository information from multiple platforms."""

    def __init__(self, config: MirrorConfig = None):
        self.config = config or MirrorConfig()
        self.rotator = MirrorRotator(self.config)

    def fetch_metadata(self, repo_info: Dict) -> Optional[Dict]:
        """Fetch repository metadata (description, stars, forks, etc.)."""

        platform = repo_info['platform']
        owner = repo_info['owner']
        repo = repo_info['repo']

        if platform == 'github':
            return self._fetch_github_metadata(owner, repo)
        elif platform == 'gitlab':
            return self._fetch_gitlab_metadata(owner, repo)
        elif platform == 'gitee':
            return self._fetch_gitee_metadata(owner, repo)

        return None

    def _fetch_github_metadata(self, owner: str, repo: str) -> Optional[Dict]:
        """Fetch GitHub repository metadata."""

        mirrors = self.config.get_api_mirrors('github')

        def path_builder(mirror_url: str) -> str:
            return f"{mirror_url}/repos/{owner}/{repo}"

        content, mirror = self.rotator.fetch_with_rotation(mirrors, path_builder)

        if content:
            data = json.loads(content)
            return {
                'description': data.get('description', ''),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'language': data.get('language', ''),
                'default_branch': data.get('default_branch', 'main'),
                'homepage': data.get('homepage', ''),
                'mirror_used': mirror.get('name', 'unknown') if mirror else 'unknown'
            }

        return None

    def _fetch_gitlab_metadata(self, owner: str, repo: str) -> Optional[Dict]:
        """Fetch GitLab repository metadata."""

        mirrors = self.config.get_api_mirrors('gitlab')

        def path_builder(mirror_url: str) -> str:
            # GitLab API requires URL-encoded project path
            encoded = f"{owner}%2F{repo}"
            return f"{mirror_url}/projects/{encoded}"

        content, mirror = self.rotator.fetch_with_rotation(mirrors, path_builder)

        if content:
            data = json.loads(content)
            return {
                'description': data.get('description', ''),
                'stars': data.get('star_count', 0),
                'forks': data.get('forks_count', 0),
                'language': '',  # GitLab doesn't provide this in metadata
                'default_branch': data.get('default_branch', 'main'),
                'homepage': data.get('web_url', ''),
                'mirror_used': mirror.get('name', 'unknown') if mirror else 'unknown'
            }

        return None

    def _fetch_gitee_metadata(self, owner: str, repo: str) -> Optional[Dict]:
        """Fetch Gitee repository metadata."""

        mirrors = self.config.get_api_mirrors('gitee')

        def path_builder(mirror_url: str) -> str:
            return f"{mirror_url}/repos/{owner}/{repo}"

        content, mirror = self.rotator.fetch_with_rotation(mirrors, path_builder)

        if content:
            data = json.loads(content)
            return {
                'description': data.get('description', ''),
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'language': data.get('language', ''),
                'default_branch': data.get('default_branch', 'master'),
                'homepage': data.get('homepage', ''),
                'mirror_used': mirror.get('name', 'unknown') if mirror else 'unknown'
            }

        return None

    def fetch_readme(self, repo_info: Dict, metadata: Dict) -> str:
        """Fetch README content from repository."""

        platform = repo_info['platform']
        owner = repo_info['owner']
        repo = repo_info['repo']
        default_branch = metadata.get('default_branch', 'main')

        if platform == 'github':
            return self._fetch_github_readme(owner, repo, default_branch)
        elif platform == 'gitlab':
            return self._fetch_gitlab_readme(owner, repo, default_branch)
        elif platform == 'gitee':
            return self._fetch_gitee_readme(owner, repo, default_branch)

        return ""

    def _fetch_github_readme(self, owner: str, repo: str, branch: str) -> str:
        """Fetch README from GitHub."""

        mirrors = self.config.get_api_mirrors('github')

        def path_builder(mirror_url: str) -> str:
            return f"{mirror_url}/repos/{owner}/{repo}/readme"

        content, mirror = self.rotator.fetch_with_rotation(mirrors, path_builder)

        if content:
            data = json.loads(content)
            # GitHub API returns base64-encoded content
            import base64
            encoded = data.get('content', '')
            if encoded:
                try:
                    return base64.b64decode(encoded).decode('utf-8')
                except Exception:
                    pass

        # Fallback to raw mirrors
        raw_mirrors = self.config.get_raw_mirrors('github')

        for raw_mirror in raw_mirrors:
            for try_branch in [branch, 'main', 'master', 'develop']:
                for filename in ['README.md', 'readme.md', 'README.rst', 'README.txt']:
                    try:
                        url = f"{raw_mirror['url']}/{owner}/{repo}/{try_branch}/{filename}"
                        with urllib.request.urlopen(url, timeout=10) as response:
                            return response.read().decode('utf-8')
                    except Exception:
                        continue

        return ""

    def _fetch_gitlab_readme(self, owner: str, repo: str, branch: str) -> str:
        """Fetch README from GitLab."""

        mirrors = self.config.get_api_mirrors('gitlab')

        def path_builder(mirror_url: str) -> str:
            encoded = f"{owner}%2F{repo}"
            return f"{mirror_url}/projects/{encoded}/repository/files/README.md/raw?ref={branch}"

        content, mirror = self.rotator.fetch_with_rotation(mirrors, path_builder)

        if content:
            return content

        # Try alternative branches
        for try_branch in ['main', 'master', 'develop']:
            def alt_path_builder(mirror_url: str) -> str:
                encoded = f"{owner}%2F{repo}"
                return f"{mirror_url}/projects/{encoded}/repository/files/README.md/raw?ref={try_branch}"

            content, _ = self.rotator.fetch_with_rotation(mirrors, alt_path_builder)
            if content:
                return content

        return ""

    def _fetch_gitee_readme(self, owner: str, repo: str, branch: str) -> str:
        """Fetch README from Gitee."""

        mirrors = self.config.get_api_mirrors('gitee')

        def path_builder(mirror_url: str) -> str:
            return f"{mirror_url}/repos/{owner}/{repo}/contents/README.md?ref={branch}"

        content, mirror = self.rotator.fetch_with_rotation(mirrors, path_builder)

        if content:
            data = json.loads(content)
            import base64
            encoded = data.get('content', '')
            if encoded:
                try:
                    return base64.b64decode(encoded).decode('utf-8')
                except Exception:
                    pass

        # Try raw URL
        for try_branch in [branch, 'main', 'master']:
            try:
                url = f"https://gitee.com/{owner}/{repo}/raw/{try_branch}/README.md"
                with urllib.request.urlopen(url, timeout=10) as response:
                    return response.read().decode('utf-8')
            except Exception:
                continue

        return ""

    def get_commit_hash(self, repo_info: Dict) -> str:
        """Get latest commit hash using git ls-remote."""

        url = repo_info['original_url']

        try:
            result = subprocess.run(
                ['git', 'ls-remote', url, 'HEAD'],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            # Output format: <hash>\tHEAD
            return result.stdout.split()[0]
        except Exception as e:
            print(f"Warning: Could not fetch commit hash: {e}", file=sys.stderr)
            return "unknown"


def get_repo_info(url: str) -> Dict:
    """
    Main function to fetch repository information.

    Args:
        url: Repository URL (GitHub, GitLab, or Gitee)

    Returns:
        Dict with repository information
    """
    # Parse URL
    parsed = RepoParser.parse_url(url)
    if not parsed:
        return {
            "error": f"Invalid or unsupported repository URL: {url}",
            "supported_platforms": ["GitHub", "GitLab", "Gitee"]
        }

    # Initialize fetcher
    config = MirrorConfig()
    fetcher = RepoFetcher(config)

    # Fetch metadata
    metadata = fetcher.fetch_metadata(parsed)

    if not metadata:
        return {
            "error": f"Could not fetch metadata for {parsed['qualified_name']}",
            "platform": parsed['platform'],
            "suggestions": [
                "Verify the repository exists and is public",
                "Check your internet connection",
                "Try again later (rate limit may apply)"
            ]
        }

    # Fetch README
    readme = fetcher.fetch_readme(parsed, metadata)

    # Get commit hash
    commit_hash = fetcher.get_commit_hash(parsed)

    # Construct result
    result = {
        "name": parsed['repo'],
        "url": url,
        "platform": parsed['platform'],
        "owner": parsed['owner'],
        "qualified_name": parsed['qualified_name'],
        "latest_hash": commit_hash,
        "metadata": metadata,
        "readme": readme[:10000] if readme else "",  # Truncate if too large
        "mirror_config_version": config.version,
        "fetched_at": datetime.now().isoformat()
    }

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_repo_info.py <repository_url>")
        print("\nSupported platforms:")
        print("  - GitHub:  https://github.com/owner/repo")
        print("  - GitLab:  https://gitlab.com/owner/repo")
        print("  - Gitee:   https://gitee.com/owner/repo")
        sys.exit(1)

    url = sys.argv[1]
    info = get_repo_info(url)

    if 'error' in info:
        print(json.dumps({"error": info['error']}, indent=2), file=sys.stderr)
        if 'suggestions' in info:
            print("\nSuggestions:", file=sys.stderr)
            for s in info['suggestions']:
                print(f"  - {s}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(info, indent=2, ensure_ascii=False))
