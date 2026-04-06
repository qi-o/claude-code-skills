---
name: baoyu-article-illustrator
description: 分析文章结构，识别需要配图的位置，使用 Type × Style 二维方案生成插图。当用户要求 "illustrate article"、"add images"、"generate images for article" 或 "为文章配图" 时使用。不要用于数据图表或科学图表（请使用 pub-figures）。
version: 1.57.0
github_url: https://github.com/JimLiu/baoyu-skills
github_hash: c5c54e26dab507ba9dbba69aa00a85e65796becb
source: skills/baoyu-article-illustrator
license: MIT
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator
  ref: refs/heads/main
---

# Article Illustrator

分析文章，识别配图位置，使用 Type × Style 一致性方案生成图片。

## 两个维度

| 维度 | 控制 | 示例 |
|-----------|----------|----------|
| **Type（类型）** | 信息结构 | infographic, scene, flowchart, comparison, framework, timeline |
| **Style（风格）** | 视觉美学 | notion, warm, minimal, blueprint, watercolor, elegant |

自由组合: `--type infographic --style blueprint`

或使用预设: `--preset tech-explainer` → 一个参数包含 type + style。详见 [Style Presets](references/style-presets.md)。

## 类型

| Type | 适用场景 |
|------|----------|
| `infographic` | 数据、指标、技术类 |
| `scene` | 叙事、情感类 |
| `flowchart` | 流程、工作流 |
| `comparison` | 对比、选项 |
| `framework` | 模型、架构 |
| `timeline` | 历史、演进 |

## 风格

详见 [references/styles.md](references/styles.md) 了解核心风格、完整画廊及 Type × Style 兼容性矩阵。

## 工作流

```
- [ ] Step 1: 预检查 (EXTEND.md, references, config)
- [ ] Step 2: 分析内容
- [ ] Step 3: 确认设置 (AskUserQuestion)
- [ ] Step 4: 生成大纲
- [ ] Step 5: 生成图片
- [ ] Step 6: 收尾
```

### Step 1: 预检查

**1.5 加载偏好设置 (EXTEND.md) ⛔ 阻塞项**

检查 EXTEND.md 是否存在并加载偏好设置。完整加载流程和路径优先级见 [extend-preferences.md](references/extend-preferences.md)。

```bash
# macOS, Linux, WSL, Git Bash
test -f .baoyu-skills/baoyu-article-illustrator/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-article-illustrator/EXTEND.md" && echo "xdg"
test -f "$HOME/.baoyu-skills/baoyu-article-illustrator/EXTEND.md" && echo "user"
```

```powershell
# PowerShell (Windows)
if (Test-Path .baoyu-skills/baoyu-article-illustrator/EXTEND.md) { "project" }
$xdg = if ($env:XDG_CONFIG_HOME) { $env:XDG_CONFIG_HOME } else { "$HOME/.config" }
if (Test-Path "$xdg/baoyu-skills/baoyu-article-illustrator/EXTEND.md") { "xdg" }
if (Test-Path "$HOME/.baoyu-skills/baoyu-article-illustrator/EXTEND.md") { "user" }
```

| 结果 | 操作 |
|--------|--------|
| 找到 | 读取、解析、显示摘要 |
| 未找到 | ⛔ 运行 [首次设置](references/config/first-time-setup.md) |

完整流程: [references/workflow.md](references/workflow.md#step-1-pre-check)

### Step 2: 分析

| 分析项 | 输出 |
|----------|--------|
| 内容类型 | 技术 / 教程 / 方法论 / 叙事 |
| 目的 | 信息传达 / 可视化 / 想象力 |
| 核心论点 | 2-5 个要点 |
| 位置 | 配图能增加价值的地方 |

**关键**: 隐喻 → 可视化底层概念，而非字面图片。

完整流程: [references/workflow.md](references/workflow.md#step-2-setup--analyze)

### Step 3: 确认设置 ⚠️

**单次 AskUserQuestion，最多 4 个问题。Q1-Q2 必填。选择预设时 Q3 可跳过。**

| Q | 选项 |
|---|---------|
| **Q1: 预设或类型** | [推荐预设], [备选预设], 或手动选择: infographic, scene, flowchart, comparison, framework, timeline, mixed |
| **Q2: 密度** | minimal (1-2), balanced (3-5), per-section (推荐), rich (6+) |
| **Q3: 风格** | [推荐], minimal-flat, sci-fi, hand-drawn, editorial, scene, poster, 其他 — **选择预设时可跳过** |
| Q4: 语言 | 当文章语言与 EXTEND.md 设置不同时 |

完整流程: [references/workflow.md](references/workflow.md#step-3-confirm-settings-)

### Step 4: 生成大纲

保存 `outline.md`，包含 frontmatter（type, density, style, image_count）和条目：

```yaml
## Illustration 1
**Position**: [section/paragraph]
**Purpose**: [why]
**Visual Content**: [what]
**Filename**: 01-infographic-concept-name.png
```

完整模板: [references/workflow.md](references/workflow.md#step-4-generate-outline)

### Step 5: 生成图片

⛔ **阻塞项: 必须先保存 prompt 文件，然后才能生成任何图片。**

**执行策略**: 当多个插图已保存 prompt 文件且当前任务仅为生成时，优先使用 `baoyu-imagine` 批量模式（`build-batch.ts` → `--batchfile`）而非启动子代理。仅在每张图片仍需单独 prompt 迭代或创意探索时才使用子代理。

1. 为每个插图，按照 [references/prompt-construction.md](references/prompt-construction.md) 创建 prompt 文件
2. 保存到 `prompts/NN-{type}-{slug}.md`，包含 YAML frontmatter
3. Prompt **必须** 使用类型特定的模板，包含结构化区块（ZONES / LABELS / COLORS / STYLE / ASPECT）
4. LABELS **必须** 包含文章特定数据：实际数字、术语、指标、引用
5. **禁止** 在未先保存 prompt 文件的情况下直接向 `--prompt` 传递临时内联 prompt
6. 选择生成技能，处理引用（`direct`/`style`/`palette`）
7. 如 EXTEND.md 启用，应用水印
8. 从保存的 prompt 文件生成；失败时重试一次

完整流程: [references/workflow.md](references/workflow.md#step-5-generate-images)

### Step 6: 收尾

在段落后插入 `![description]({relative-path}/NN-{type}-{slug}.png)`。路径根据输出目录设置相对于文章文件计算。

```
Article Illustration Complete!
Article: [path] | Type: [type] | Density: [level] | Style: [style]
Images: X/N generated
```

## 输出目录

输出目录由 EXTEND.md 中的 `default_output_dir` 决定（首次设置时配置）：

| `default_output_dir` | 输出路径 | Markdown 插入路径 |
|----------------------|-------------|----------------------|
| `imgs-subdir`（默认） | `{article-dir}/imgs/` | `imgs/NN-{type}-{slug}.png` |
| `same-dir` | `{article-dir}/` | `NN-{type}-{slug}.png` |
| `illustrations-subdir` | `{article-dir}/illustrations/` | `illustrations/NN-{type}-{slug}.png` |
| `independent` | `illustrations/{topic-slug}/` | `illustrations/{topic-slug}/NN-{type}-{slug}.png`（相对于 cwd） |

所有辅助文件（大纲、prompt）保存在输出目录内：

```
{output-dir}/
├── outline.md
├── prompts/
│   └── NN-{type}-{slug}.md
└── NN-{type}-{slug}.png
```

当输入为**粘贴内容**（无文件路径）时，始终使用 `illustrations/{topic-slug}/`，并将 `source-{slug}.{ext}` 保存在一起。

**Slug**: 2-4 个单词，kebab-case。**冲突**: 追加 `-YYYYMMDD-HHMMSS`。

## 修改

| 操作 | 步骤 |
|--------|--------|
| 编辑 | 更新 prompt → 重新生成 → 更新引用 |
| 添加 | 定位 → Prompt → 生成 → 更新大纲 → 插入 |
| 删除 | 删除文件 → 移除引用 → 更新大纲 |

## 参考资料

| 文件 | 内容 |
|------|---------|
| [references/workflow.md](references/workflow.md) | 详细流程 |
| [references/usage.md](references/usage.md) | 命令语法 |
| [references/styles.md](references/styles.md) | 风格画廊 |
| [references/style-presets.md](references/style-presets.md) | 预设快捷方式（type + style） |
| [references/prompt-construction.md](references/prompt-construction.md) | Prompt 模板 |
| [references/config/first-time-setup.md](references/config/first-time-setup.md) | 首次设置 |
