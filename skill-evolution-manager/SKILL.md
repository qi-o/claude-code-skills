---
name: skill-evolution-manager
description: 在对话结束时，根据用户反馈总结优化并迭代现有 Skills 的核心工具。通过吸取对话"精华"持续演进 Skills 库。当用户说"优化skill"、"迭代技能"、"总结对话经验"、"把这个经验保存到skill"、"记录一下这个教训"、"evolve skill"、"update skill from conversation"、"/skill-evolution-manager"或对话结束时主动触发。Do NOT use for installing or updating skills from GitHub (use skill-manager instead).
license: MIT
github_url: ""
github_hash: ""
local_only: true
---

# Skill Evolution Manager

这是整个 AI 技能系统的“进化中枢”。它不仅负责优化单个 Skill，还负责跨 Skill 的经验复盘和沉淀。

## 核心职责

1.  **复盘诊断 (Session Review)**：在对话结束时，分析所有被调用的 Skill 的表现。
2.  **经验提取 (Experience Extraction)**：将非结构化的用户反馈转化为结构化的 JSON 数据（`evolution.json`）。
3.  **智能缝合 (Smart Stitching)**：将沉淀的经验自动写入 `SKILL.md`，确保持久化且不被版本更新覆盖。

## 使用场景

**Trigger**: 
- `/evolve`
- "复盘一下刚才的对话"
- "我觉得刚才那个工具不太好用，记录一下"
- "把这个经验保存到 Skill 里"

## 工作流 (The Evolution Workflow)

### 1. 经验复盘 (Review & Extract)
当用户触发复盘时，Agent 必须执行：
1.  **扫描上下文**：找出用户不满意的点（报错、风格不对、参数错误）或满意的点（特定 Prompt 效果好）。
2.  **定位 Skill**：确定是哪个 Skill 需要进化（例如 `yt-dlp` 或 `baoyu-comic`）。
3.  **生成 JSON**：在内存中构建如下 JSON 结构：
    ```json
    {
      "preferences": ["用户希望下载默认静音"],
      "fixes": ["Windows 下 ffmpeg 路径需转义"],
      "custom_prompts": "在执行前总是先打印预估耗时"
    }
    ```

### 2. 经验持久化 (Persist)
Agent 调用 `scripts/merge_evolution.py`，将上述 JSON 增量写入目标 Skill 的 `evolution.json` 文件中。
- **命令**: `python scripts/merge_evolution.py <skill_path> <json_string>`

### 3. 文档缝合 (Stitch)
Agent 调用 `scripts/smart_stitch.py`，将 `evolution.json` 的内容转化为 Markdown 并追加到 `SKILL.md` 末尾。
- **命令**: `python scripts/smart_stitch.py <skill_path>`

### 4. 跨版本对齐 (Align)
当 `skill-manager` 更新了某个 Skill 后，Agent 应主动运行 `smart_stitch.py`，将之前保存的经验“重新缝合”到新版文档中。

## 核心脚本

- `scripts/merge_evolution.py`: **增量合并工具**。负责读取旧 JSON，去重合并新 List，保存。
- `scripts/smart_stitch.py`: **文档生成工具**。负责读取 JSON，在 `SKILL.md` 末尾生成或更新 `## User-Learned Best Practices & Constraints` 章节。
- `scripts/align_all.py`: **全量对齐工具**。一键遍历所有 Skill 文件夹，将存在的 `evolution.json` 经验重新缝合回对应的 `SKILL.md`。常用于 `skill-manager` 批量更新后的经验还原。

## 最佳实践

- **不要直接修改 SKILL.md 的正文**：除非是明显的拼写错误。所有的经验修正应通过 `evolution.json` 通道进行，这样可以保证在 Skill 升级时经验不丢失。
- **多 Skill 协同**：如果一次对话涉及多个 Skill，请依次为每个 Skill 执行上述流程。

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 跨 Skill 链接验证时，grep 应只匹配推荐表行格式（^|.*使用 `...`），避免正文中的代码引用（如 auto 路由、PAPER_SEARCH_MCP_* 环境变量、download_with_fallback 函数名）产生误报。

### Known Fixes & Workarounds
- SKILL.md 的 name 字段必须使用 kebab-case 格式，不能包含空格（如 skill-evolution-manager 而非 Skill Evolution Manager）
- name 字段应与文件夹名保持一致，否则 Claude Code 无法正确识别 skill

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 写入 SKILL.md | `smart_stitch.py` 准备追加内容时 | 展示将要追加的内容摘要，确认用户同意修改 SKILL.md |
| 修改 evolution.json | `merge_evolution.py` 合并新经验时 | 展示新增/变更的经验条目，确认后写入 |
| 全量对齐 | `align_all.py` 批量更新所有 Skill 时 | 提示影响范围（哪些 Skill 会被修改），确认后执行 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 脚本执行失败 | merge_evolution.py 或 smart_stitch.py 返回非零退出码 | 检查 Python 环境和脚本路径，手动执行 JSON 合并和文档追加 |
| SKILL.md 无写入权限 | 文件写入时报权限错误 | 提示用户检查文件权限，或手动复制生成的内容 |
| evolution.json 格式损坏 | JSON 解析失败 | 从 SKILL.md 末尾的 User-Learned 章节反向重建 JSON |
| 目标 Skill 不存在 | 指定的 skill_path 目录为空或缺少 SKILL.md | 列出可用的 Skill 目录供用户选择正确的路径 |

**原则**：不要静默失败——报错时同时提供修复建议。