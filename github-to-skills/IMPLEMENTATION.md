# Implementation Guide for repo-to-skills v2.0

This document explains the technical implementation of the multi-platform repository to skill converter.

## About This Fusion Skill

This skill is a **fusion** of two open-source projects:

### Primary Source: github-to-skills
- **Repository**: [KKKKhazix/Khazix-Skills](https://github.com/KKKKhazix/Khazix-Skills)
- **Contributions**:
  - Extended metadata schema (github_hash, version, created_at)
  - Lifecycle management integration with skill-manager
  - User preference tracking (evolution.json)

### Secondary Source: repo2skill
- **Repository**: [zhangyanxs/repo2skill](https://github.com/zhangyanxs/repo2skill)
- **Contributions**:
  - Multi-platform support (GitHub, GitLab, Gitee)
  - 10+ mirror rotation with automatic failover
  - AI-powered repository analysis
  - Complete API reference documentation
  - Batch conversion capability

### Update Tracking

The skill metadata includes both sources:

```yaml
---
# Primary source
github_url: https://github.com/KKKKhazix/Khazix-Skills
github_hash: fe15fea6cf7ac216027d11c2c64e87b462cc0427

# Secondary source
secondary_sources:
  - name: repo2skill
    url: https://github.com/zhangyanxs/repo2skill
    hash: 6daa62f40d2a7ffbdc9c3cd54d58a34c908f499b
    contributions: [mirror_rotation, multi_platform, ai_analysis, api_references]
---
```

**For skill-manager**: When checking for updates, compare hashes against **both** repositories to determine if updates are available from either source.

## Architecture

### Skill Structure

```
github-to-skills/
鈹溾攢鈹€ SKILL.md                  # Main skill definition (v2.0 - multi-platform)
鈹溾攢鈹€ IMPLEMENTATION.md         # This document
鈹溾攢鈹€ evolution.json            # Skill evolution tracking
鈹溾攢鈹€ scripts/
鈹?  鈹溾攢鈹€ fetch_repo_info.py    # Multi-platform fetcher with mirror rotation
鈹?  鈹溾攢鈹€ create_skill.py       # Enhanced skill scaffolding
鈹?  鈹溾攢鈹€ mirrors.json          # Mirror configuration
鈹?  鈹溾攢鈹€ fetch_github_info.py  # Legacy: GitHub-only fetcher (deprecated)
鈹?  鈹斺攢鈹€ create_github_skill.py # Legacy: GitHub-only creator (deprecated)
鈹斺攢鈹€ references/               # API reference documents
    鈹溾攢鈹€ github-api.md         # GitHub API v3 quick reference
    鈹溾攢鈹€ gitlab-api.md         # GitLab API v4 quick reference
    鈹斺攢鈹€ gitee-api.md          # Gitee API v5 quick reference
```

## Component Overview

### 1. URL Parsing (RepoParser)

**File**: `scripts/fetch_repo_info.py`

Detects platform and extracts repository information:

```python
from scripts.fetch_repo_info import RepoParser

parsed = RepoParser.parse_url("https://github.com/vercel/next.js")
# Returns: {
#     'platform': 'github',
#     'owner': 'vercel',
#     'repo': 'next.js',
#     'qualified_name': 'vercel/next.js',
#     'original_url': 'https://github.com/vercel/next.js'
# }
```

**Supported patterns**:
- GitHub: `github.com/{owner}/{repo}`
- GitLab: `gitlab.com/{owner}/{repo}`
- Gitee: `gitee.com/{owner}/{repo}`

### 2. Mirror Rotation (MirrorRotator)

**File**: `scripts/fetch_repo_info.py`

Implements intelligent mirror rotation with exponential backoff:

**Retry strategy**:
- 5 retries per mirror
- Backoff delays: 1s, 2s, 4s, 8s
- Switch mirrors after 3 consecutive failures
- 30-second timeout per request

**Usage**:
```python
from scripts.fetch_repo_info import MirrorConfig, MirrorRotator

config = MirrorConfig()  # Loads scripts/mirrors.json
rotator = MirrorRotator(config)

content, mirror = rotator.fetch_with_rotation(
    mirrors=config.get_api_mirrors('github'),
    path_builder=lambda url: f"{url}/repos/{owner}/{repo}"
)
```

### 3. Repository Fetching (RepoFetcher)

**File**: `scripts/fetch_repo_info.py`

Multi-platform repository data fetcher:

**Methods**:
- `fetch_metadata()`: Description, stars, forks, language, default branch
- `fetch_readme()`: README content with fallback branches
- `get_commit_hash()`: Latest commit via git ls-remote

**Usage**:
```python
from scripts.fetch_repo_info import get_repo_info

info = get_repo_info("https://github.com/vercel/next.js")
# Returns: {
#     'name': 'next.js',
#     'platform': 'github',
#     'latest_hash': 'abc123...',
#     'metadata': {...},
#     'readme': '...',
#     'fetched_at': '2026-01-27T...'
# }
```

### 4. Skill Generation (create_skill)

**File**: `scripts/create_skill.py`

Enhanced skill scaffolding with platform-specific metadata:

**Features**:
- Kebab-case name sanitization
- Platform-specific URL fields (github_url, gitlab_url, gitee_url)
- Tag extraction from README
- Comprehensive SKILL.md generation

**Usage**:
```bash
# Fetch repository info
python scripts/fetch_repo_info.py https://github.com/vercel/next.js > repo_info.json

# Create skill
python scripts/create_skill.py repo_info.json ~/.config/opencode/skills
```

## Mirror Configuration

**File**: `scripts/mirrors.json`

JSON configuration for mirror endpoints:

**Structure**:
```json
{
  "mirrors": {
    "github": {
      "api": [...],    // 8 API mirrors
      "raw": [...]     // 3 raw content mirrors
    },
    "gitlab": {
      "api": [...]     // 2 API mirrors
    },
    "gitee": {
      "api": [...]     // 1 API mirror
    }
  },
  "retry_strategy": {
    "max_retries_per_mirror": 5,
    "backoff_delays": [1, 2, 4, 8],
    "timeout_seconds": 30,
    "failover_threshold": 3
  }
}
```

**Adding new mirrors**:
1. Edit `scripts/mirrors.json`
2. Add mirror object with `url`, `name`, and `priority`
3. Lower priority = tried first

## Metadata Schema

### Enhanced Frontmatter

```yaml
---
name: <kebab-case-skill-name>
description: <concise-description>
github_url: <url>  # or gitlab_url/gitee_url
github_hash: <commit-sha>
version: 0.1.0
created_at: <ISO-8601-timestamp>
platform: <github|gitlab|gitee>
source: <repo-url>
stars: <count>
language: <language>
entry_point: scripts/wrapper.py
dependencies: []
tags: []
mirror_used: <mirror-name>
---
```

### Key Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `github_hash` | Commit tracking for updates | `fe15fea6cf7ac216027d11c2c64e87b462cc0427` |
| `platform` | Source platform | `github`, `gitlab`, `gitee` |
| `mirror_used` | Debugging and analytics | `api.github.com`, `kgithub` |
| `stars` | Repository popularity | `12345` |
| `tags` | Skill discoverability | `["javascript", "framework", "web"]` |

## AI Analysis Integration

The skill instructions prompt the AI to:

1. **Parse repository URL** and detect platform
2. **Fetch data** using mirror rotation
3. **Analyze content** using configured LLM
4. **Generate SKILL.md** with comprehensive sections

**Analysis prompts** built into SKILL.md:
```
Analyze this repository and extract:
- Installation instructions (npm/pip/cargo/etc.)
- Usage examples with code snippets
- API endpoints or function signatures
- Configuration options
- Common issues and solutions
```

## Platform-Specific Considerations

### GitHub
- **Default branch**: Often `main`
- **API rate limits**: 60/hour (unauth), 5000/hour (auth)
- **Content encoding**: Base64 for API
- **Mirrors**: 8 API + 3 raw mirrors available

### GitLab
- **Default branch**: Often `main`
- **URL encoding**: Required (owner%2Frepo)
- **Content encoding**: Raw (not base64)
- **Mirrors**: 2 API mirrors available

### Gitee
- **Default branch**: Often `master` (not `main`)
- **Native speed**: Fast in China
- **Content encoding**: Base64 for API
- **Mirrors**: 1 official mirror

## Lifecycle Management

### Update Detection

The `github_hash` field enables automatic update detection. **For fusion skills with dual sources**, check both repositories:

```python
# Check primary source (github-to-skills)
local_hash = skill_metadata['github_hash']
remote_hash = fetch_latest_commit_hash(skill_metadata['github_url'])

primary_update_needed = local_hash != remote_hash

# Check secondary sources (repo2skill)
secondary_updates = []
for source in skill_metadata.get('secondary_sources', []):
    local_secondary_hash = source['hash']
    remote_secondary_hash = fetch_latest_commit_hash(source['url'])
    if local_secondary_hash != remote_secondary_hash:
        secondary_updates.append(source['name'])

# Determine if update is needed
update_needed = primary_update_needed or len(secondary_updates) > 0

if update_needed:
    # Update needed from primary or secondary source
    update_fusion_skill(repo_url)
```

### Dual-Source Update Process

When updating this fusion skill:

1. **Check both sources**:
   ```bash
   # Primary source
   git ls-remote https://github.com/KKKKhazix/Khazix-Skills HEAD

   # Secondary source
   git ls-remote https://github.com/zhangyanxs/repo2skill HEAD
   ```

2. **Compare with local hashes**:
   - Primary: `github_hash` in frontmatter
   - Secondary: `secondary_sources[].hash` in frontmatter

3. **If either has updates**:
   - Review changes from both repositories
   - Merge non-conflicting improvements
   - Resolve conflicts based on feature priorities
   - Update relevant hashes
   - Document changes in version history

4. **Update priority**:
   - **Primary source** (github-to-skills): Metadata tracking, lifecycle management
   - **Secondary source** (repo2skill): Mirror rotation, multi-platform, AI analysis
   - When conflicts arise, preserve core functionality from both sources

## Error Handling

### Repository Not Accessible

```
鉂?Unable to access repository: {url}
Possible reasons:
- Repository doesn't exist
- Repository is private (need token)
- Network issues (all mirrors failed)
- Rate limit exceeded
```

### README Missing

```
鈿狅笍 No README found for {repo}
Falling back to file structure analysis...
鉁?Generated skill based on code structure
```

## Performance

Expected times:

| Repository Size | Files | Time |
|----------------|-------|------|
| Small | < 500 | 30-60s |
| Medium | 500-2k | 1-2min |
| Large | 2k+ | 2-5min |

**Factors**:
- Mirror response times
- Repository size
- README length
- LLM speed
- Network connectivity

## Security

- No user data sent to external services (except public APIs)
- No secrets stored in the skill
- Uses your trusted LLM provider
- HTTPS for all API calls
- Tokens optional (for higher rate limits)

## Extending the Skill

### Add New Platform

1. Add platform pattern to `RepoParser.PLATFORM_PATTERNS`
2. Add mirror configuration to `mirrors.json`
3. Implement fetch methods in `RepoFetcher`
4. Create API reference in `references/`

### Add New Mirror

1. Edit `scripts/mirrors.json`
2. Add mirror with `url`, `name`, `priority`
3. Test with `python scripts/fetch_repo_info.py <url>`

### Customize SKILL.md Template

Edit `generate_skill_content()` in `scripts/create_skill.py`

## Migration from v1.0

### Changes

| v1.0 | v2.0 |
|------|------|
| `fetch_github_info.py` | `fetch_repo_info.py` |
| `create_github_skill.py` | `create_skill.py` |
| GitHub only | Multi-platform |
| No mirrors | 10+ mirrors |
| Basic metadata | Enhanced metadata |

### Migration Steps

1. **Rename skill directory** (optional):
   ```bash
   mv github-to-skills repo-to-skills
   ```

2. **Update SKILL.md**:
   - Name: `github-to-skills` 鈫?`repo-to-skills`
   - Version: `1.0.0` 鈫?`2.0.0`

3. **Use new scripts**:
   ```bash
   # Old (deprecated)
   python scripts/fetch_github_info.py <url>
   python scripts/create_github_skill.py info.json output

   # New
   python scripts/fetch_repo_info.py <url>
   python scripts/create_skill.py info.json output
   ```

4. **Old scripts remain** for backward compatibility

## Debugging

### Enable verbose output

```bash
python scripts/fetch_repo_info.py <url> --verbose
```

### Check mirror status

```bash
# Test GitHub mirrors
for mirror in $(jq '.mirrors.github.api[].url' scripts/mirrors.json); do
    curl -I "$mirror/repos/vercel/next.js"
done
```

### Verify skill structure

```bash
tree ~/.config/opencode/skills/<skill-name>/
```

## License

MIT - Feel free to modify and extend!

## Version History

- **2.0.0** (2026-01-27): Fusion release
  - **Fusion with repo2skill**: Integrated multi-platform support, mirror rotation, and AI analysis
  - **Dual-source tracking**: Now tracks both github-to-skills and repo2skill for updates
  - **New features**: GitLab/Gitee support, 10+ GitHub mirrors, AI-powered analysis
  - **Preserved**: Original metadata tracking and lifecycle management from github-to-skills

- **1.0.0**: Original github-to-skills
  - GitHub-only support
  - Basic metadata tracking (github_hash, version, created_at)
  - skill-manager integration
