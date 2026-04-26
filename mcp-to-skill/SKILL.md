---
name: mcp-to-skill
description: |
  Convert MCP (Model Context Protocol) servers to Claude Code Skills. Use when:
  (1) User wants to convert an MCP server project to a skill
  (2) User mentions "MCP to skill", "convert MCP", or "MCP 杞?skill"
  (3) User has an MCP server codebase and wants to make it a reusable skill
  (4) User wants to analyze MCP server structure for skill creation
  Supports TypeScript/JavaScript and Python MCP servers. Generates complete skill package with SKILL.md, scripts, and references.
  Do NOT use for creating skills from scratch (use skill-creator instead) or converting GitHub repos (use github-to-skills instead).
license: MIT
version: 0.1.0
metadata:
  category: workflow-automation
---

# MCP to Skill Converter

Convert MCP servers into Claude Code Skills for easier distribution and usage.

## Conversion Workflow

### 1. Analyze MCP Server

Read and understand the MCP server structure:

```bash
# Key files to analyze
- package.json / pyproject.toml  # Dependencies and entry point
- src/index.ts / main.py         # Entry point and tool registration
- src/**/*.ts / **/*.py          # Tool implementations
```

Extract this information:
- **Server name and description**
- **Available tools** (name, description, parameters, implementation)
- **Dependencies** (runtime requirements)
- **Execution method** (node, python, etc.)

### 2. Map MCP Tools to Skill Structure

| MCP Concept | Skill Equivalent |
|-------------|------------------|
| Tool name | Script or instruction section |
| Tool description | Used in SKILL.md description |
| Tool parameters | Script arguments or instruction parameters |
| Tool implementation | `scripts/` executable or inline instructions |

### 3. Generate Skill Structure

```
{skill-name}/
鈹溾攢鈹€ SKILL.md                    # Core instructions
鈹溾攢鈹€ scripts/
鈹?  鈹溾攢鈹€ run_server.sh          # Server startup script (optional)
鈹?  鈹斺攢鈹€ {tool_name}.{ext}      # Individual tool scripts
鈹斺攢鈹€ references/
    鈹斺攢鈹€ tools.md               # Tool reference documentation
```

### 4. Write SKILL.md

Template structure:

```markdown
---
name: {skill-name}
description: |
  {Original MCP server description}. Use when:
  (1) {Primary use case}
  (2) {Secondary use case}
  {List all tool capabilities}
---

# {Skill Name}

{Brief description of what this skill does}

## Prerequisites

{Any setup requirements - permissions, API keys, etc.}

## Available Tools

{List each tool with usage instructions}

### {Tool Name}

{Description}

**Usage:**
{How to invoke - either via script or direct instruction}

**Parameters:**
- `{param}`: {description}

**Example:**
{Concrete usage example}
```

## Agent-Centric Design Checklist

When converting MCP tools, apply these principles to ensure the resulting skill works well with agents:

| Principle | How to Apply During Conversion |
|-----------|-------------------------------|
| **Build for workflows** | Consolidate related API operations into single script entry points that complete real tasks, not just wrap individual endpoints |
| **Optimize context space** | Default to concise output; offer `--detailed` flag; prefer human-readable names over technical IDs |
| **Actionable errors** | Error messages must include the next step (e.g., "Token expired — run `gh auth login` then retry") |
| **Natural task subdivision** | Name scripts/sections after human tasks (`sync_contacts`) not API endpoints (`POST /contacts/sync`) |
| **Evaluation-driven** | Before finalizing the skill, write 5-10 realistic test questions an agent would face using it |

## Conversion Patterns

### Pattern A: Script-based (for complex tools)

When MCP tool has complex logic, create executable script:

```python
# scripts/tool_name.py
#!/usr/bin/env python3
import argparse
# ... implementation
```

Reference in SKILL.md:
```markdown
Run `scripts/tool_name.py --param value`
```

### Pattern B: Instruction-based (for simple tools)

When MCP tool is simple, use inline instructions:

```markdown
### Send Notification

To send a system notification:
1. Use AppleScript: `display notification "message" with title "title"`
```

### Pattern C: Hybrid (server-dependent tools)

When tools require the MCP server runtime:

```markdown
## Setup

Start the MCP server:
\`\`\`bash
cd {project-path}
npm start  # or: node dist/index.js
\`\`\`

Then use MCP tools via the running server.
```

## AppleScript MCP Example

For applescript-mcp specifically:

1. **No server needed** - Tools are standalone AppleScripts
2. **Use instruction-based pattern** - Each tool becomes a section
3. **Group by category** - System, Calendar, Finder, etc.
4. **Include permission notes** - macOS security requirements

## Output Checklist

Before packaging, verify:

- [ ] SKILL.md has proper frontmatter (name, description)
- [ ] Description includes all use cases and triggers
- [ ] All MCP tools are documented
- [ ] Scripts are executable and tested
- [ ] References are complete but not redundant
- [ ] No unnecessary files (README, CHANGELOG, etc.)

## Package the Skill

```bash
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py /path/to/skill
```

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 转换模式选择 | MCP server 结构分析完成后 | 展示工具列表和建议的转换模式（脚本型/指令型/混合型），确认选择 |
| Skill 名称和路径 | 生成 SKILL.md 之前 | 确认 skill 名称（kebab-case）、安装路径、是否与已有 skill 冲突 |
| 生成文件覆盖 | 目标路径已有同名文件 | 列出将被覆盖的文件，确认用户同意覆盖 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| MCP server 入口文件无法解析 | package.json/pyproject.toml 缺失或格式异常 | 手动检查项目结构；询问用户提供入口文件路径 |
| 工具参数提取失败 | 无法从源码中自动提取参数 schema | 回退到手动模式：读取工具实现代码，人工编写参数文档 |
| 生成的脚本不可执行 | 运行测试脚本时权限错误或依赖缺失 | 添加执行权限（`chmod +x`）；检查 `requirements.txt` 依赖是否完整 |
