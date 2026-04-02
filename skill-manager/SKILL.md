---
name: skill-manager
description: Lifecycle manager for GitHub-based skills with dual-source support. Use this to batch scan your skills directory, check for updates on GitHub, perform guided upgrades, discover popular skills, and batch update outdated skills. Use when user says "检查更新", "skill更新", "扫描技能", "批量更新", "推荐技能", "scan skills", "check for updates", "batch update", "update skills", or "/skill-manager". Do NOT use for installing new skills from scratch (use github-to-skills instead).
license: MIT
github_url: https://github.com/KKKKhazix/Khazix-Skills
github_hash: fe15fea6cf7ac216027d11c2c64e87b462cc0427
version: 1.0.0
metadata:
  category: workflow-automation
---

# Skill Lifecycle Manager

This skill helps you maintain your library of GitHub-wrapped skills by automating the detection of updates, discovering popular skills, and assisting in the refactoring process.

## What's New: Dual-Source Support

**Version 2.0** now supports **fusion skills** with multiple source repositories:

- **Single-source skills**: Traditional skills with one `github_url`
- **Fusion skills**: Skills with primary source + `secondary_sources` (e.g., repo-to-skills)

When checking for updates, skill-manager now monitors **all sources** for fusion skills:

```yaml
---
# Single-source skill
github_url: https://github.com/owner/repo
github_hash: abc123

# Fusion skill
github_url: https://github.com/primary/repo
github_hash: abc123
secondary_sources:
  - name: secondary-repo
    url: https://github.com/secondary/repo
    hash: def456
---
```

**Update behavior:**
- Single-source: Checks primary repository
- Fusion: Checks ALL sources, reports outdated if ANY source has updates

## Core Capabilities

1.  **Audit**: Scans your local skills folder for skills with `github_url` metadata.
2.  **Check**: Queries GitHub (via `git ls-remote`) to compare local commit hashes against the latest remote HEAD.
3.  **Dual-Source Checking**: For fusion skills, checks both primary and secondary sources.
4.  **Report**: Generates a status report identifying which skills are "Current", "Outdated", or "Error".
5.  **Update Workflow**: Provides a structured process for the Agent to upgrade a skill.
6.  **Inventory Management**: Lists all local skills and provides deletion capabilities.
7.  **Discover**: Fetches popular skills from skills.sh and marks already installed ones.
8.  **Batch Update**: Checks all GitHub-based skills for updates and provides batch update capability.

## Usage

**Trigger**: `/skill-manager check` or "Scan my skills for updates"
**Trigger**: `/skill-manager list` or "List my skills"
**Trigger**: `/skill-manager delete <skill_name>` or "Delete skill <skill_name>"
**Trigger**: `/skill-manager recommend` or "Recommend popular skills"
**Trigger**: `/skill-manager batch-update` or "Batch update all outdated skills"

### Workflow 1: Check for Updates

1.  **Run Scanner**: The agent runs `scripts/scan_and_check.py` to analyze all skills.
2.  **Review Report**: The script outputs a JSON summary. The Agent presents this to the user.
    *   Example: "Found 3 outdated skills: `yt-dlp` (behind 50 commits), `ffmpeg-tool` (behind 2 commits)..."

### Workflow 2: Update a Skill

**Trigger**: "Update [Skill Name]" (after a check)

1.  **Fetch New Context**: The agent fetches the *new* README from the remote repo.
2.  **Diff Analysis**:
    *   The agent compares the new README with the old `SKILL.md`.
    *   Identifies new features, deprecated flags, or usage changes.
3.  **Refactor**:
    *   The agent rewrites `SKILL.md` to reflect the new capabilities.
    *   The agent updates the `github_hash` in the frontmatter.
    *   The agent (optionally) attempts to update the `wrapper.py` if CLI args have changed.
4.  **Verify**: Runs a quick validation (if available).

### Workflow 3: Discover Popular Skills

**Trigger**: `/skill-manager recommend` or "Show me popular skills"

1.  **Fetch Rankings**: The agent runs `scripts/recommend_skills.py` to fetch popular skills from skills.sh.
2.  **Present Results**: Shows a ranked list of popular skills with install counts.
    *   Already installed skills are marked with `[Installed]`.
3.  **Install Option**: User can choose to install any recommended skill using `github-to-skills`.

**Command Options**:
```bash
python scripts/recommend_skills.py --limit 20 --format table
python scripts/recommend_skills.py --limit 10 --format json --include-installed
```

### Workflow 4: Batch Update Skills

**Trigger**: `/skill-manager batch-update` or "Update all my outdated skills"

1.  **Scan All Skills**: The agent runs `scripts/batch_update.py` to check all GitHub-based skills.
2.  **Generate Report**: Shows summary of current, outdated, and error states.
3.  **Update Process**: For each outdated skill:
    *   The agent uses `github-to-skills` to regenerate the skill wrapper.
    *   Updates are applied sequentially to avoid conflicts.

**Command Options**:
```bash
python scripts/batch_update.py --check-only           # Only check, don't update
python scripts/batch_update.py --format json          # JSON output for parsing
python scripts/batch_update.py --auto-update          # Auto-update outdated skills
```

## Scripts

- `scripts/scan_and_check.py`: The workhorse. Scans directories, parses Frontmatter, fetches remote hashes for ALL sources, returns status.
- `scripts/update_helper.py`: (Optional) Helper to backup files before update.
- `scripts/list_skills.py`: Lists all installed skills with type and version.
- `scripts/delete_skill.py`: Permanently removes a skill folder.
- `scripts/recommend_skills.py`: Fetches and displays popular skills from skills.sh.
- `scripts/batch_update.py`: Batch checks and updates all GitHub-based skills.

## Metadata Requirements

This manager relies on the `github-to-skills` metadata standard:

### Single-Source Skills (Traditional)
```yaml
---
github_url: https://github.com/owner/repo
github_hash: abc123...
version: 1.0.0
---
```

### Fusion Skills (Multi-Source)
```yaml
---
# Primary source
github_url: https://github.com/primary/repo
github_hash: abc123...

# Secondary sources
secondary_sources:
  - name: secondary-feature
    url: https://github.com/secondary/repo
    hash: def456...
    contributions: [feature1, feature2]
---
```

**Update Logic:**
- Single-source: Checks if `github_hash` matches remote HEAD
- Fusion: Checks ALL sources (primary + all secondary), marks outdated if ANY source has updates

## Command Line Usage

### Check for Updates
```bash
# Table format (default)
python scripts/scan_and_check.py ~/.claude/skills

# Summary format
python scripts/scan_and_check.py ~/.claude/skills --format summary

# JSON format (for parsing)
python scripts/scan_and_check.py ~/.claude/skills --format json

# Save to file
python scripts/scan_and_check.py ~/.claude/skills --output report.txt
```

### Output Examples

**Table Format:**
```
Name                           Type            Status      Message
----------------------------------------------------------------------------------------------------
repo-to-skills                 fusion 馃敆       鈿狅笍          Updates available from one or more sources
yt-dlp-skill                   single-source   鉁?         Up to date
ffmpeg-tool                    single-source   鉂?         Could not reach remote
```

**Summary Format:**
```
馃搳 Update Check Summary

Total skills: 25
鉁?Current: 20
鈿狅笍  Outdated: 3
鉂?Errors: 2

馃摝 Outdated Skills:
  - repo-to-skills
    Sources needing update: primary, repo2skill
  - nextjs-skill
  - react-skill
```

**JSON Format:**
```json
[
  {
    "name": "repo-to-skills",
    "type": "fusion",
    "status": "outdated",
    "primary_status": "outdated",
    "secondary_status": {
      "0": {
        "status": "outdated",
        "remote_hash": "newhash..."
      }
    },
    "message": "Updates available from one or more sources"
  }
]
```

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 批量更新时优先显示过时的 skills
- 推荐功能应标记已安装的 skills
- 更新 skill 时必须进行完整内容检查，不能只更新哈希值
- 批量更新时应先对比上游 README 和本地 SKILL.md 的差异
- 更新 fusion skill 时需要检查主源和所有次源的更新状态
- 双源检查功能通过扫描 secondary_sources 字段识别融合技能
- 用户希望基于 master 分支（稳定版）而非默认分支（可能是 dev）进行更新检查
- 在推荐外部 Skill 前，先检查用户是否已有功能相似的本地 Skill
- 对比分析时列出具体功能差异表格
- 推荐 skill 时应根据用户现有技能组合进行个性化分析
- 推荐前应对比功能覆盖度，标注与现有 skill 的互补或重叠关系
- 对于功能相近的 skill，应提供详细对比表格帮助用户决策
- 用户要求使用简体中文回复
- 混合更新模式：当上游有重大重构（如语言变更）时，可选择保留本地语言+合并上游新功能
- 版本号升级规范：minor版本增加表示功能升级（1.0.0→1.1.0），major版本增加表示重大重构（1.x→2.x）
- 更新技能时应同时更新：version、github_hash、source（如路径变化）
- 上游仓库结构变化时需检查：原baoyu-skills直接存放skill，现改为skills/子目录
- 批量更新采用混合策略（保留本地+合并上游新功能）而非全量替换
- 更新前对比上游commits了解具体变化
- omo-skills需同步到最新默认分支而非仅master分支
- 批量更新时按来源分组处理（anthropics/skills、JimLiu/baoyu-skills 等），同一仓库的技能共享 hash
- Anthropic 官方技能更新时需同步 scripts/office/ 共享框架（含 schemas、validators、helpers）
- baoyu-skills 上游趋势是精简主文档+references引用架构，混合更新时保留本地中文详细内容
- 安装新技能后必须执行三层分级合规检查流程
- 本地 skill（无 GitHub 仓库）应设置 github_url: "" 和 local_only: true，scan_and_check.py 会跳过远程检查并标记为 current
- skills 目录结构：技能同时存在于根目录和 .curated/ 子目录，两处都会被扫描，修复 github_url 时需同时更新两处副本
- 验证本地安装的 Skill（无 GitHub 源）时应使用 migrate.py --verify，scan_and_check.py 只扫描有 GitHub 远程源的 Skill
- skills 目录结构：技能同时存在于根目录（符号链接）和子目录（.curated/、.experimental/），扫描脚本应同时扫描两处
- scan_and_check.py 已支持递归扫描子目录，自动发现 .curated/ 和 .experimental/ 中的 skills
- 更新 skill 时必须同时更新 description frontmatter 以反映新增数据源
- paper-search 更新采用混合策略：保留本地中文内容，合并上游新数据源和架构说明
- 更新后版本号规则：新增数据源/功能升级用 minor 版本（1.0.0→1.1.0）

### Known Fixes & Workarounds
- skills.sh 使用 Next.js 渲染，数据嵌入在 __next_f 脚本中，需要用正则提取转义 JSON
- 转义 JSON 的模式为: "source":"owner/repo","skillId":"name","installs":123
- Anthropic 官方 skills 仓库是 https://github.com/anthropics/skills
- 为 Standard 类型的 skills 添加 github_url 和 github_hash 可使其变为 GitHub 类型
- scan_and_check.py 输出的 JSON 在 Windows 下通过管道传递给 Python 解析时可能因为编码问题失败，建议直接读取完整输出
- 完整更新流程：1)获取上游README 2)读取本地SKILL.md 3)对比功能变化 4)更新内容 5)最后更新hash
- 如果上游有新功能、新命令、废弃功能等实质性变化，必须同步更新 SKILL.md 内容
- Windows 下输出中文表情符号时使用 JSON 格式避免编码错误
- fusion skill 的更新需要同时更新所有源的 hash 值
- scan_and_check.py 已修改为优先检查 master 分支，然后是 main，最后才是 HEAD，确保基于稳定版本进行更新检查
- Windows 下 summary 格式输出中文表情符号时会因编码问题失败，应使用 JSON 格式
- 获取上游README时需确认正确路径（如skills/baoyu-comic/SKILL.md而非根目录）
- Windows下curl获取GitHub内容时优先使用raw.githubusercontent.com
- 混合更新策略：对比本地和上游差异后，选择性地合并新功能而非全量替换
- Windows下curl通过管道传递JSON给Python时需保存到文件再读取避免编码问题
- 获取GitHub commits对比时需使用UTF-8编码读取JSON
- omo-skills的本地版本可能比master分支更新，应检查默认分支的最新commit
- planning-with-files上游README不在master分支根目录
- GitHub API 限流时使用 git clone --depth 1 --filter=blob:none --sparse 浅克隆获取上游文件
- Anthropic 0.2.0到0.3.0 脚本路径从 ooxml/scripts/ 迁移到 scripts/office/，更新时需同步删除旧目录并复制新目录
- pptx 0.3.0 从 html2pptx 迁移到 pptxgenjs，需删除 ooxml/ ooxml.md html2pptx.md 并复制 editing.md pptxgenjs.md
- 大型更新任务（如5个技能同时更新）agent 可能因 token 限制中断，需检查完成状态并恢复继续
- scan_and_check.py 已支持 local_only 标志：在 scan_skills() 中检测 local_only 或空 github_url，直接返回 current 状态；在 check_updates() 中跳过 local-only 类型的 skill；在状态汇总循环中也跳过 local-only 类型
- 创建本地 skill 后需检查根目录（skills/）和子目录（.curated/）是否都有副本，两处的 github_url 都需要清空
- PowerShell 双引号字符串中反斜杠在变量前会被吃掉（如 "$src" 变成 skillsbiopython），应使用 Join-Path $src $skill 构建路径
- 稀疏克隆安装本地 Skill 后 scan_and_check.py 显示 MISSING 属正常现象（无 GitHub URL），migrate.py --verify 的 Check 5 才是正确验证入口
- 技能整理方案：将散落的 skills 移动到 .curated/（精选）或 .experimental/（实验），根目录通过符号链接暴露
- scan_and_check.py 扫描时会同时发现根目录符号链接和子目录源文件，导致重复扫描，这是预期行为不影响功能
- paper-search 环境变量统一改为 PAPER_SEARCH_MCP_* 前缀，旧名仍向后兼容
- scan_and_check.py 对 local-only skill（github_url 为空）应直接标记为 current 跳过远程检查
- scan_and_check.py 在 Windows 下 table 格式输出中文编码异常，确认数据正确性永远用 --format json，再通过 python -c "import json; ..." 管道解析字段，而非读取 table 文本
- Windows 下 Python re.sub 替换含数字的 hash 字符串时，repl 参数中的数字会被误判为 regex group reference 导致 PatternError。批量更新 hash 应使用 str.replace() 或 re.sub(pattern, lambda m: new_value, content) 替代