---
name: github-to-skills
description: Multi-platform repository to skill converter with AI-powered analysis, mirror rotation, and enhanced metadata tracking. Supports GitHub, GitLab, and Gitee. Use when user wants to convert a repository into an AI skill. Triggers: "仓库转Skill", "GitHub转技能", "convert repo", "repo to skill", "把仓库转成skill", "从GitHub安装skill". Do NOT use for creating skills from scratch (use skill-creator instead).
license: MIT
# Primary source (original github-to-skills)
github_url: https://github.com/KKKKhazix/Khazix-Skills
github_hash: 08996c956ea70b1529a9b1bff308296c4076c3ad
# Secondary source (repo2skill - mirror rotation, multi-platform, AI analysis)
secondary_sources:
  - name: repo2skill
    url: https://github.com/zhangyanxs/repo2skill
    hash: c8a4ddc1bc6bacfa3f8eb24643b2d37ba3522af7
    contributions: [mirror_rotation, multi_platform, ai_analysis, api_references, local_repo_support]
version: 2.1.0
platforms: [github, gitlab, gitee]
metadata:
  category: workflow-automation
---

# Repo to Skills Factory

This skill automates the conversion of open-source repositories (GitHub, GitLab, Gitee) into fully functional AI skills with intelligent mirror rotation, AI-powered analysis, and comprehensive metadata tracking.

## About This Skill

This is a **fusion skill** that combines the best features from two projects:

| Feature | github-to-skills (KKHKhazix) | repo2skill (zhangyanxs) | **Fusion Result** |
|---------|------------------------------|------------------------|------------------|
| **Metadata Tracking** | 鉁?github_hash, version | 鉂?| 鉁?**Preserved** |
| **Lifecycle Management** | 鉁?skill-manager integration | 鉂?| 鉁?**Preserved** |
| **Multi-Platform** | 鉂?GitHub only | 鉁?GH+GL+Gitee | 鉁?**Added** |
| **Mirror Rotation** | 鉂?| 鉁?10+ mirrors | 鉁?**Added** |
| **AI Analysis** | 鉂?Manual | 鉁?Auto | 鉁?**Added** |
| **API References** | 鉂?| 鉁?Complete docs | 鉁?**Added** |
| **Batch Conversion** | 鉂?| 鉁?| 鉁?**Added** |
| **Local Repo Support** | 鉂?| 鉁?| 鉁?**Added** |

**Source Repositories:**
- Primary: [KKKKhazix/Khazix-Skills](https://github.com/KKKKhazix/Khazix-Skills) - Metadata tracking and lifecycle management
- Secondary: [zhangyanxs/repo2skill](https://github.com/zhangyanxs/repo2skill) - Mirror rotation, multi-platform, AI analysis

When `skill-manager` checks for updates, it will monitor **both** repositories for new changes.

## Core Functionality

1. **Multi-Platform Support**: GitHub, GitLab, and Gitee repositories
2. **Local Repository Support**: Direct analysis of local project directories - no network required
3. **Intelligent Mirror Rotation**: 10+ GitHub mirrors with automatic failover
4. **AI-Powered Analysis**: Uses configured LLM to analyze repository structure and documentation
5. **Enhanced Metadata**: Tracks source URL, commit hash, version, and timestamps for lifecycle management
6. **Batch Processing**: Convert multiple repositories simultaneously
7. **Scaffolding**: Creates standardized skill directory structure with wrapper scripts

## Usage

**Triggers:**

- `/repo-to-skills <repository_url>`
- "Convert this repo to a skill: <url>"
- "帮我把这个仓库转成技能：<url>"
- "帮我把当前项目转成技能"
- "帮我把这个本地项目转成技能：<path>"

**Supported URL formats:**

```
GitHub:  https://github.com/owner/repo
GitLab:  https://gitlab.com/owner/repo
Gitee:   https://gitee.com/owner/repo
Local:   ./my-project  |  /absolute/path  |  ~/workspace/project
```

**Batch conversion:**

```
Convert these repos:
- https://github.com/vercel/next.js
- https://gitlab.com/gitlab-org/gitlab
- https://gitee.com/mindspore/docs
```

## Workflow

### Step 1: Parse Repository URL

Detect platform and extract repository information:

- Platform (github/gitlab/gitee)
- Owner (user/org name)
- Repository name
- Full qualified name (owner/repo)

**Input Detection (Remote vs Local):**

```
Input
  鈹溾攢 Remote URL (github/gitlab/gitee.com) 鈫?Remote Flow (Steps 2+)
  鈹斺攢 Local Path (./, /, ~, or directory)  鈫?Local Flow (Step 1b)
```

**Step 1b: Local Repository Flow**

When input is a local path:

- Validate path exists
- Extract README, config files, docs directly from filesystem
- Infer metadata: language, type, dependencies from config files
- Detect git remote URL (if git repository)
- 2-3x faster than remote repositories - no network required

**Supported local path formats:**

```
./my-project          (relative path)
/home/user/projects   (absolute path)
~/workspace/project   (home directory)
my-project            (directory in current path)
```

**Implementation:**

```python
# Use scripts/fetch_repo_info.py with RepoParser class
from scripts.fetch_repo_info import RepoParser
parsed = RepoParser.parse_url(url)
# Returns: {platform, owner, repo, qualified_name, original_url}
```

### Step 2: Fetch Repository Data

Use mirror rotation with retry logic:

**Fetch metadata:**

- Description, stars, forks
- Primary language
- Default branch
- Homepage URL

**Fetch content:**

- README content (try default_branch, main, master, develop)
- File tree structure (for large projects)
- Key documentation files

**Mirror rotation:**

```python
# Automatic mirror rotation with exponential backoff
from scripts.fetch_repo_info import MirrorConfig, RepoFetcher

config = MirrorConfig()  # Loads scripts/mirrors.json
fetcher = RepoFetcher(config)
metadata = fetcher.fetch_metadata(parsed)
readme = fetcher.fetch_readme(parsed, metadata)
commit_hash = fetcher.get_commit_hash(parsed)
```

**Retry strategy:**

- 5 retries per mirror
- Exponential backoff: 1s, 2s, 4s, 8s
- Auto switch on 3 consecutive failures
- 30-second timeout per request

### Step 3: AI-Powered Analysis

Use your configured LLM to analyze the repository:

**Extract information:**

1. **Project Overview**: Purpose, target users, key features
2. **Installation**: Prerequisites, install commands, setup steps
3. **Usage**: Quick start, common tasks, code examples
4. **API Reference**: Main endpoints, key functions, parameters
5. **Configuration**: Environment variables, config files, defaults
6. **Development**: Architecture, testing, contributing
7. **Troubleshooting**: Common issues, solutions

**Analysis prompts:**

```
Analyze this repository and extract:
- Installation instructions (npm/pip/cargo/etc.)
- Usage examples with code snippets
- API endpoints or function signatures
- Configuration options
- Common issues and solutions

Base the analysis on the README and repository structure.
```

### Step 4: Generate Enhanced SKILL.md

**Required metadata schema (MANDATORY for lifecycle management):**

```yaml
---
name: <kebab-case-repo-name>
description: <concise-description-for-agent-triggering>
# Extended Metadata (MANDATORY for skill-manager)
github_url: <original-repo-url>  # or gitlab_url/gitee_url
github_hash: <latest-commit-hash-at-creation>
version: <tag-or-0.1.0>
created_at: <ISO-8601-timestamp>
platform: <github|gitlab|gitee>
source: <repo-url>
stars: <star-count>
language: <primary-language>
entry_point: scripts/wrapper.py
dependencies: []  # List main dependencies
tags: []  # Auto-generated tags
mirror_used: <mirror-name-if-github>  # For debugging
---
```

**Generate comprehensive sections:**

```markdown
# {Repo Name} Skill

## Quick Start
[Installation and basic usage]

## Overview
[Project description, purpose, target users]

## Features
[Key features with descriptions]

## Installation
[Detailed installation guide with multiple package managers]

## Usage
[Usage guide with real code examples]

## API Reference (if applicable)
[API documentation with examples]

## Configuration
[Settings, environment variables, config files]

## Development
[Development setup, testing, contributing]

## Troubleshooting
[FAQ and solutions]

## Resources
[Links to docs, examples, community]
```

### Step 5: Directory Structure

Create standardized skill structure:

```
{skill-name}/
鈹溾攢鈹€ SKILL.md              # Main skill definition
鈹溾攢鈹€ IMPLEMENTATION.md     # Optional: technical details
鈹溾攢鈹€ scripts/
鈹?  鈹斺攢鈹€ wrapper.py        # Tool wrapper script
鈹溾攢鈹€ references/           # Optional: API references
鈹?  鈹斺攢鈹€ api.md
鈹斺攢鈹€ assets/               # Optional: diagrams, logos
```

### Step 6: Installation Path

Ask user where to save the skill:

**Option 1: Project Local**

```
./.opencode/skills/{skill-name}/
```

Available only in current project.

**Option 2: Global User**

```
~/.config/opencode/skills/{skill-name}/
```

Available in all projects (OpenCode).

**Option 3: Claude Compatible**

```
~/.claude/skills/{skill-name}/
```

Works with OpenCode and Claude Code.

## Mirror Configuration

**GitHub API Mirrors** (8 mirrors, priority order):

1. api.github.com (official)
2. gh.api.888888888.xyz
3. gh-proxy.com/api/github
4. api.fastgit.org
5. api.kgithub.com
6. githubapi.muicss.com
7. github.91chi.fun
8. mirror.ghproxy.com

**GitHub Raw Mirrors** (3 mirrors):

1. raw.githubusercontent.com
2. raw.fastgit.org
3. raw.kgithub.com

**GitLab API Mirrors** (2 mirrors):

1. gitlab.com/api/v4 (official)
2. gl.gitmirror.com/api/v4

**Gitee API** (1 mirror):

1. gitee.com/api/v5 (official - native speed in China)

See `scripts/mirrors.json` for complete configuration.

## Resources

- `scripts/fetch_repo_info.py`: Multi-platform fetcher with mirror rotation
- `scripts/create_skill.py`: Skill scaffolding and generation
- `scripts/mirrors.json`: Mirror configuration and retry settings
- `references/github-api.md`: GitHub API quick reference
- `references/gitlab-api.md`: GitLab API quick reference
- `references/gitee-api.md`: Gitee API quick reference

## Best Practices

### For Generated Skills

- **Name Format**: Use kebab-case, no spaces (e.g., `nextjs-skill`)
- **Metadata Completeness**: All extended metadata fields are MANDATORY
- **Idempotency**: The `github_hash` field allows `skill-manager` to detect updates
- **Progressive Disclosure**: Don't dump entire repo. Include wrapper + reference original
- **Isolation**: Generated skill should handle its own dependencies

### For Updates

When updating an existing skill:

1. Fetch latest hash from repository
2. Compare with local `github_hash`
3. If different:
   - Fetch latest README
   - Compare with local SKILL.md
   - Check for new features, deprecated features, breaking changes
   - Update SKILL.md content AND hash
   - Re-fetch hash at the end to avoid race conditions

### For Error Handling

**Repository not accessible:**

```
鉂?Unable to access repository: {url}
Possible reasons:
- Repository doesn't exist
- Repository is private (need token)
- Network issues (all mirrors failed)
- Rate limit exceeded

Suggestions:
1. Verify the URL is correct
2. Check if repository is public
3. Try accessing in browser
4. Wait a few minutes and retry
```

**README missing:**

```
鈿狅笍 No README found for {repo}
Falling back to file structure analysis...
鉁?Generated skill based on code structure
Note: Documentation may be limited
```

## Batch Conversion

For multiple repositories:

**Process:**

1. Accept all URLs
2. Process sequentially or in parallel (AI choice)
3. Generate each skill to same or different location (ask user)
4. Report overall results

**Example output:**

```
馃摝 Repository Conversion Results

鉁?vercel/next.js 鈫?nextjs-skill
   Location: ~/.config/opencode/skills/nextjs-skill/SKILL.md
   Size: 18KB
   Mirror: api.github.com

鉁?facebook/react 鈫?react-skill
   Location: ~/.config/opencode/skills/react-skill/SKILL.md
   Size: 15KB
   Mirror: gh.api.888888888.xyz (rate limited on official)

Total: 2 repositories converted
Time: 3 minutes 15 seconds
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 更新已有 skill 时应对比上游变化，不能只更新 hash
- 安装 skill 时必须包含 github_url 和 github_hash 用于版本追踪
- 安装新技能后必须执行三层分级合规检查：检查必需文件 → 判断层级 → 移入层级目录 → 创建 junction → 更新 .tier-registry.json

### Known Fixes & Workarounds
- 生成 SKILL.md 时 name 字段必须使用 kebab-case 格式，不能包含空格
- name 字段应与目标文件夹名保持一致
- 安装完成后应验证 name 字段格式是否正确
- 更新活跃仓库时应在最后一步再次获取最新 hash，避免更新过程中远程又有新提交
- 更新 skill 时需要对比上游 README 和本地 SKILL.md，如有新功能/命令/废弃功能等实质性变化，必须更新 SKILL.md 内容
- 从 monorepo 安装子目录 skill 时，github_url 应指向主仓库根目录，source 字段可指向具体子目录路径
- 三层分级目录结构已部署：.system/(12个) .curated/(14个) .experimental/(9个)，新技能默认归入 .experimental/
- agents/claude.yaml 是必需文件，缺失时需根据 SKILL.md 生成（含 display_name/description/icon/triggers/category/tier）
- Windows 下使用 mklink /J 创建兼容性 junction 不需要管理员权限

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 安装路径选择 | Step 6 生成 SKILL.md 后保存前 | 确认安装位置（项目本地 / 全局用户 / Claude 兼容） |
| 覆盖已有 Skill | 目标路径已存在同名 Skill 时 | 展示差异（新增/修改/删除内容），确认是否覆盖 |
| 批量转换执行 | 同时转换多个仓库前 | 展示所有仓库列表和目标路径，确认全部正确 |
| 分层合规检查 | 安装完成后执行三层分级检查前 | 确认 Skill 分类层级（.system/.curated/.experimental） |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 仓库不可访问 | 所有镜像均返回非 200 响应 | 检查仓库 URL 是否正确、是否为私有仓库，尝试浏览器访问验证 |
| README 缺失 | fetch_readme 返回空内容 | 回退到文件结构分析，基于代码推断功能（文档可能有限） |
| AI 分析 LLM 不可用 | LLM API 调用失败或超时 | 基于 README 原文直接生成 SKILL.md（不经过 AI 分析） |
| name 格式错误 | 生成的 name 包含空格或大写 | 自动转为 kebab-case，验证与目标文件夹名一致 |