---
name: manga-learning-creator
version: 2.4.7
description: |
  将任何文本内容（论文、文章、教程等）转化为漫画风格的学习读本。
  当用户请求「用漫画解读」「生成学习漫画」「把这篇文章/论文变成漫画」「创建漫画教程」「漫画化」「comic learning」「manga tutorial」「visual learning comic」「turn this into a manga」「create comic from article」或类似需求时使用。
  支持 5 种画风、7 种基调、6 种布局、3 种预设模式。
  Do NOT use for text-only summaries or reports (use deep-research or academic-writing-suite instead).
  支持自定义角色（如哆啦A梦、大雄等），通过角色表确保全篇一致性。
  通过 Gemini API 生成图片，自动合并为 PDF。
github_url: ""
local_only: true
source: skills/baoyu-comic
upstream_skill: baoyu-comic
fusion_note: |
  本 skill 基于 baoyu-comic v2.3 构建，融合了其多风格系统（5画风x7基调x6布局）和角色一致性机制。
  保留了自定义角色特色（哆啦A梦、柯南等）和 Gemini API 集成。
  工作流程已更新为 v2.3 版本，包括角色表优先生成、--ref 引用机制等。
  上游将 --preset 重命名为 --style，--art 默认值改为 ligne-claire（本地保留 manga 作为默认）。
  当前版本为融合增强版，功能比上游原版更丰富（中文支持、自定义角色库）。
license: MIT
compatibility: Requires Gemini API key (GEMINI_API_KEY env var)
metadata:
  category: document-creation
---

# Manga Learning Creator v2.4.7

将任何文本内容转化为漫画风格学习读本的工具。

## 核心特性

- **5 种画风** × **7 种基调** × **6 种布局** = 210 种组合
- **3 种预设模式**：快速启动常见场景
- **角色一致性**：先生成角色表，后续页面引用
- **自定义角色**：支持哆啦A梦、柯南等知名角色或完全自定义
- **自动 PDF 合并**：生成完整漫画书
- **部分工作流**：支持分阶段生成（仅分镜、仅提示词等）

---

## 画风选项 (--art)

| 画风 | 英文 | 描述 | 适用场景 |
|------|------|------|----------|
| **清线** | `ligne-claire` | 欧式清晰线条，丁丁历险记风格 | 科普、历史 |
| **日漫** | `manga` | 日式漫画，大眼睛、夸张表情 | 教程、故事 (默认) |
| **写实** | `realistic` | 接近真实的绘画风格 | 严肃主题、传记 |
| **水墨** | `ink-brush` | 中国水墨画风格 | 古典文学、哲学 |
| **粉笔** | `chalk` | 黑板粉笔画风格 | 课堂教学、数学 |

## 基调选项 (--tone)

| 基调 | 英文 | 描述 | 适用场景 |
|------|------|------|----------|
| **中性** | `neutral` | 平衡、客观 | 科普、技术 (默认) |
| **温暖** | `warm` | 温馨、治愈 | 儿童教育、心理 |
| **戏剧** | `dramatic` | 紧张、冲突 | 历史、商战 |
| **浪漫** | `romantic` | 柔和、梦幻 | 文学、艺术 |
| **活力** | `energetic` | 动感、热血 | 体育、创业 |
| **复古** | `vintage` | 怀旧、经典 | 历史、传统 |
| **动作** | `action` | 激烈、速度感 | 科技、竞争 |

## 布局选项 (--layout)

| 布局 | 英文 | 描述 | 适用场景 |
|------|------|------|----------|
| **标准** | `standard` | 传统 2×2 或 3×2 格子 | 通用 (默认) |
| **电影** | `cinematic` | 宽幅横条，电影分镜感 | 叙事、历史 |
| **密集** | `dense` | 多格小图，信息量大 | 技术细节、流程 |
| **跨页** | `splash` | 单页大图，视觉冲击 | 重要概念、高潮 |
| **混合** | `mixed` | 大小格混排 | 节奏变化 |
| **条漫** | `webtoon` | 垂直滚动式 | 移动端阅读 |

## 兼容性矩阵

| 画风 | ✓✓ 最佳搭配 | ✓ 可用 | ✗ 避免 |
|------|------------|--------|--------|
| ligne-claire | neutral, warm | dramatic, vintage, energetic | romantic, action |
| manga | neutral, romantic, energetic, action | warm, dramatic | vintage |
| realistic | neutral, warm, dramatic, vintage | action | romantic, energetic |
| ink-brush | neutral, dramatic, action, vintage | warm | romantic, energetic |
| chalk | neutral, warm, energetic | vintage | dramatic, action, romantic |

## 预设模式 (--style)

| 预设 | 等价设置 | 特殊规则 |
|------|---------|---------|
| **ohmsha** | `--art manga --tone neutral` | 视觉隐喻、无头像特写、道具揭示 |
| **wuxia** | `--art ink-brush --tone action` | 气功特效、战斗视觉、氛围元素 |
| **shoujo** | `--art manga --tone romantic` | 装饰元素、眼部细节、浪漫节拍 |

## 自动选择

| 内容特征 | 推荐 |
|----------|------|
| 教程、入门、编程、教育 | **ohmsha** 预设 |
| 1950年前、古典、古代 | realistic + vintage |
| 个人故事、导师 | ligne-claire + warm |
| 武侠、修仙 | **wuxia** 预设 |
| 爱情、校园 | **shoujo** 预设 |
| 传记、平衡 | ligne-claire + neutral |

---

## 命令行参数

### 视觉维度

| 参数 | 取值 | 说明 |
|------|------|------|
| `--art` | ligne-claire, manga, realistic, ink-brush, chalk | 画风 |
| `--tone` | neutral, warm, dramatic, romantic, energetic, vintage, action | 基调 |
| `--layout` | standard, cinematic, dense, splash, mixed, webtoon | 布局 |
| `--aspect` | 3:4 (默认), 4:3, 16:9 | 页面比例 |
| `--lang` | auto (默认), zh, en, ja | 输出语言 |
| `--style` | ohmsha, wuxia, shoujo | 预设模式 |

### 部分工作流选项

| 参数 | 说明 |
|------|------|
| `--storyboard-only` | 仅生成分镜，跳过提示词和图片 |
| `--prompts-only` | 生成分镜+提示词，跳过图片 |
| `--images-only` | 从现有 prompts 目录生成图片 |
| `--regenerate N` | 仅重新生成指定页面（如 `3` 或 `2,5,8`） |

### 其他参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--pages` | 页数 | 自动 |
| `--characters` | 角色描述 | 默认角色 |
| `--quick` | 跳过确认 | false |
| `--ref` | 角色表引用 | 无 |
| `--output` | 输出目录 | `./output` |

---

## 工作流程（9 步概览）

| 步骤 | 操作 | 关键输出 |
|------|------|---------|
| 1.1 | 加载 EXTEND.md 偏好 ⛔ 阻塞 | 配置加载 |
| 1.2 | 分析内容 | `analysis.md` |
| 1.3 | 检查现有目录 | 处理冲突 |
| 2 | 确认风格、焦点、受众、审核 ⚠️ 必须 | 用户偏好 |
| 3 | 生成分镜 + 角色 | `storyboard.md`, `characters/` |
| 4 | 审核大纲（如请求）| 用户批准 |
| 5 | 生成提示词 | `prompts/*.md` |
| 6 | 审核提示词（如请求）| 用户批准 |
| **7.1** | **首先生成角色表** | `characters/characters.png` |
| **7.2** | **每页都引用角色** | `*.png` 文件 |
| 8 | 合并为 PDF | `{slug}.pdf` |
| 9 | 完成报告 | 摘要 |

完整步骤详情（模板、命令、备份规则）→ `references/workflow_details.md`

---

## 环境要求

- Node.js 18+
- 环境变量：`GEMINI_API_KEY` 或 `TUZI_API_KEY`

```bash
cd scripts
npm install
```

---

## 最佳实践

1. **首先生成角色表**：确保全篇角色一致性
2. **逐页确认**：每页生成后检查效果再继续
3. **控制对话长度**：每个气泡不超过 20 字
4. **知识点分散**：每页 1-2 个知识点，避免信息过载
5. **善用布局变化**：重要概念用 splash，细节用 dense
6. **保持风格统一**：全篇使用相同的画风和基调
7. **使用预设**：ohmsha 适合教程，wuxia 适合武侠，shoujo 适合爱情

---

## 语言处理

**检测优先级**：`--lang` 标志 → EXTEND.md `language` → 用户对话语言 → 源内容语言

对所有交互使用用户的输入语言或保存的语言偏好（分镜、提示词、确认、进度更新）。技术术语保持英文。

---

## 参考文件

**工作流详情**：
- `references/workflow_details.md` — 9步完整流程、角色模板、分镜模板、提示词模板、输出目录结构、页面修改规则、EXTEND.md 配置 Schema、版本历史

**核心模板**：
- `references/analysis-framework.md` — 深度内容分析
- `references/character-template.md` — 角色定义格式
- `references/storyboard-template.md` — 分镜结构
- `references/ohmsha-guide.md` — 欧姆社漫画 specifics

**风格定义**：
- `references/art-styles/` — 画风（ligne-claire, manga, realistic, ink-brush, chalk）
- `references/tones/` — 基调（neutral, warm, dramatic, romantic, energetic, vintage, action）
- `references/presets/` — 带特殊规则的预设（ohmsha, wuxia, shoujo）
- `references/layouts/` — 布局（standard, cinematic, dense, splash, mixed, webtoon）

**工作流**：
- `references/workflow.md` — 完整工作流详情
- `references/auto-selection.md` — 内容信号分析
- `references/partial-workflows.md` — 部分工作流选项

**配置**：
- `references/config/preferences-schema.md` — EXTEND.md 模式
- `references/config/first-time-setup.md` — 首次设置
- `references/config/watermark-guide.md` — 水印配置

---

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 风格与预设确认 | Step 2 选择画风/基调/布局/预设 | 确认视觉维度组合，此决定影响全篇 210 种组合中的一种 |
| 分镜大纲审批 | Step 4 storyboard.md 生成完毕 | 确认每页的知识点分配和叙事节奏，避免生成后需要大量重绘 |
| 角色表确认 | Step 7.1 角色表首次生成后 | 确认角色外观描述准确，确保后续页面引用一致 |
| 页面批量生成 | 计划生成 >10 页 | 确认继续，提示 Gemini API 调用次数和预估耗时 |

---

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| Gemini API Key 未配置 | 脚本报错 `GEMINI_API_KEY` 缺失 | 阻断执行，引导用户配置环境变量 |
| 角色一致性丢失 | 后续页面角色外观与角色表明显不符 | 检查 `--ref` 引用是否正确传递，重新生成角色表并刷新引用 |
| 单页生成失败 | 某页图片生成返回错误或质量极差 | 记录失败页码，跳过并继续生成其余页面，最后支持 `--regenerate` 重试失败页 |
| PDF 合并失败 | 最终合并步骤报错 | 检查输出目录中所有 PNG 是否完整，手动用 `npx pdfkit` 或其他工具合并 |
| EXTEND.md 不存在 | Step 1.1 Pre-check 阶段 | 阻塞并运行 first-time-setup，完成后继续 |
