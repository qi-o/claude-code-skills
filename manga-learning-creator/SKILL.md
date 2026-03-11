---
name: manga-learning-creator
version: 2.4.7
description: |
  将任何文本内容（论文、文章、教程等）转化为漫画风格的学习读本。
  当用户请求「用漫画解读」「生成学习漫画」「把这篇文章/论文变成漫画」「创建漫画教程」或类似需求时使用。
  支持 5 种画风、7 种基调、6 种布局、3 种预设模式。
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

# Manga Learning Creator v2.1

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

预设不仅设置 art+tone，还有特殊规则：

| 预设 | 等价设置 | 特殊规则 |
|------|---------|---------|
| **ohmsha** | `--art manga --tone neutral` | 视觉隐喻、无头像特写、道具揭示 |
| **wuxia** | `--art ink-brush --tone action` | 气功特效、战斗视觉、氛围元素 |
| **shoujo** | `--art manga --tone romantic` | 装饰元素、眼部细节、浪漫节拍 |

## 自动选择

内容信号决定默认设置：

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

## 工作流程（9 步）

```
漫画进度检查清单:
- [ ] 第1步：设置与分析
  - [ ] 1.1 偏好设置 (EXTEND.md) ⛔ 阻塞
    - [ ] 找到 → 加载偏好 → 继续
    - [ ] 未找到 → 首次设置 → 必须先完成
  - [ ] 1.2 分析, 1.3 检查现有
- [ ] 第2步：确认 - 风格与选项 ⚠️ 必需
- [ ] 第3步：生成分镜 + 角色
- [ ] 第4步：审核大纲（条件性）
- [ ] 第5步：生成提示词
- [ ] 第6步：审核提示词（条件性）
- [ ] 第7步：生成图片 ⚠️ 角色引用必需
  - [ ] 7.1 **首先生成角色表** → characters/characters.png
  - [ ] 7.2 **每页都使用角色引用** → 用 `--ref characters/characters.png`
- [ ] 第8步：合并为 PDF
- [ ] 第9步：完成报告
```

### 流程图

```
输入 → [偏好] ─┬─ 找到 → 继续
              │
              └─ 未找到 → 首次设置 ⛔ 阻塞
                                 │
                                 └─ 完成设置 → 保存 EXTEND.md → 继续
                                                                         │
        ┌─────────────────────────────────────────────────────────────────┘
        ↓
分析 → [检查现有?] → [确认: 风格 + 审核] → 分镜 → [审核?] → 提示词 → [审核?] → 图片 → PDF → 完成
```

### 步骤概览

| 步骤 | 操作 | 关键输出 |
|------|------|---------|
| 1.1 | 加载 EXTEND.md 偏好 ⛔ 阻塞 | 配置加载 |
| 1.2 | 分析内容 | `analysis.md` |
| 1.3 | 检查现有目录 | 处理冲突 |
| 2 | 确认风格、焦点、受众、审核 | 用户偏好 |
| 3 | 生成分镜 + 角色 | `storyboard.md`, `characters/` |
| 4 | 审核大纲（如请求）| 用户批准 |
| 5 | 生成提示词 | `prompts/*.md` |
| 6 | 审核提示词（如请求）| 用户批准 |
| **7.1** | **首先生成角色表** | `characters/characters.png` |
| **7.2** | **每页都引用角色** | `*.png` 文件 |
| 8 | 合并为 PDF | `{slug}.pdf` |
| 9 | 完成报告 | 摘要 |

---

### 第 1 步：设置与分析

**1.1 加载偏好（EXTEND.md）** ⛔ **阻塞步骤**

**关键**：如果未找到 EXTEND.md，**必须**先完成首次设置，然后才能进行其他步骤。不要继续到内容分析、不要询问画风、不要询问基调——**只**完成偏好设置。

```bash
# 检查项目级
test -f .baoyu-skills/baoyu-comic/EXTEND.md && echo "project"

# 检查用户级
test -f "$HOME/.baoyu-skills/baoyu-comic/EXTEND.md" && echo "user"
```

| 路径 | 位置 |
|------|------|
| `.baoyu-skills/baoyu-comic/EXTEND.md` | 项目目录 |
| `$HOME/.baoyu-skills/baoyu-comic/EXTEND.md` | 用户主目录 |

| 结果 | 操作 |
|------|------|
| 找到 | 读取、解析、显示摘要 → 继续 |
| 未找到 | ⛔ **阻塞**：仅运行首次设置 → 完成并保存 EXTEND.md → 然后继续 |

**支持**：水印 | 偏好画风/基调/布局 | 自定义风格定义 | 角色预设 | 语言偏好

---

**1.2 分析内容**

1. 加载用户偏好（检查 EXTEND.md）
2. 阅读用户提供的文本内容
3. 提取核心知识点和学习目标
4. 分析内容类型，推荐画风/基调/布局组合

**内容信号自动检测**：
- 教程/入门 → 推荐 `ohmsha` 预设
- 武侠/古典 → 推荐 `wuxia` 预设
- 爱情/文艺 → 推荐 `shoujo` 预设

---

**1.3 检查现有目录**

输出目录：`comic/{topic-slug}/`
- Slug：2-4 个词的 kebab-case（如 `alan-turing-bio`）
- 冲突：附加时间戳（如 `turing-story-20260118-143052`）

处理已存在目录的策略：
- 询问用户：覆盖、备份、或新建

---

### 第 2 步：确认选项 ⚠️ 必须

向用户确认以下选项：

```
📋 漫画生成配置确认

主题：[主题名称]
画风：manga (日漫)
基调：neutral (中性)
布局：standard (标准)
页数：8-10 页
角色：[角色A] + [角色B]

中间审核：
- [ ] 分镜审核（生成大纲后暂停）
- [ ] 提示词审核（生成提示词后暂停）

是否确认？或调整参数：
--art ligne-claire --tone warm --layout cinematic
```

**此步骤不可跳过**，除非用户使用 `--quick` 参数。

---

### 第 3 步：角色设定 + 生成分镜

**3.1 确定漫画角色**

**默认角色**：
- 讲解者：智慧老师/专家形象
- 学习者：好奇学生/新手形象

**自定义角色**（用户可指定）：
- 哆啦A梦 + 大雄
- 柯南 + 小兰
- 自定义角色描述

**角色定义格式**：

```yaml
角色A（讲解者）:
  名称: 哆啦A梦
  外观: 蓝色机器猫，圆圆的身体，白色肚皮，红色鼻子
  特征: 戴着铃铛项圈，有四次元口袋
  性格: 聪明、耐心、偶尔吐槽
  服装: 无（机器猫本体）

角色B（学习者）:
  名称: 大雄
  外观: 小学生男孩，戴圆框眼镜，黑色短发
  特征: 表情丰富，经常困惑或恍然大悟
  性格: 好奇、有点懒、但认真学习时很专注
  服装: 黄色上衣，蓝色短裤
```

保存到 `characters/characters.md`

---

**3.2 生成分镜脚本**

根据内容复杂度规划页数：

| 内容复杂度 | 页数 | 示例 |
|-----------|------|------|
| 简单概念 | 3-5 页 | 单一概念解释 |
| 中等复杂度 | 6-10 页 | 技术教程 |
| 复杂内容 | 10-15 页 | 论文解读 |

**结构模板**（保存到 `storyboard.md`）：

```markdown
## 漫画结构规划

总页数：X 页
主题：[主题名称]
画风：[选定画风]
基调：[选定基调]
布局：[选定布局]

### 第 1 页 - 开场
- 场景：[场景描述]
- 布局：splash（跨页大图）
- 对话要点：引入主题，角色登场
- 知识点：无（铺垫）

### 第 2 页 - 问题提出
- 场景：[场景描述]
- 布局：standard
- 对话要点：学习者提出疑问
- 知识点：[核心问题]

### 第 3-N 页 - 核心讲解
- 每页 1-2 个知识点
- 由浅入深

### 最后 1-2 页 - 总结
- 回顾要点
- 实际应用示例
```

---

### 第 4 步：审核大纲（条件性）

如果在第 2 步用户选择了分镜审核：
- 展示 `storyboard.md`
- 询问是否批准或需要修改
- 根据反馈调整

---

### 第 5 步：生成图像提示词

为每页生成详细提示词：

```markdown
## 第 X 页提示词

【画风】{art} 风格
【基调】{tone} 氛围
【布局】{layout} 排版

【场景】
[具体场景描述，包括背景、光线、氛围]

【角色】（参考角色表 characters/characters.png）
- {角色A}：[表情/动作]，[位置]
- {角色B}：[表情/动作]，[位置]

【对话气泡】
- {角色A}："[对话内容，不超过20字]"
- {角色B}："[对话内容，不超过20字]"

【画面元素】
[道具、视觉元素、知识图示]

【特殊要求】
- 保持角色外观与角色表一致
- [其他特殊要求]
```

保存到 `prompts/NN-{cover|page}-[slug].md`

**备份规则**：如果提示词文件存在，重命名为 `prompts/NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.md`

---

### 第 6 步：审核提示词（条件性）

如果在第 2 步用户选择了提示词审核：
- 展示生成的提示词
- 询问是否批准或需要修改
- 根据反馈调整

---

### 第 7 步：生成图片 ⚠️ **关键**

**角色引用对视觉一致性是必需的。**

**7.1 首先生成角色表**：

**备份规则**：如果 `characters/characters.png` 存在，重命名为 `characters/characters-backup-YYYYMMDD-HHMMSS.png`

```bash
# 使用 characters/characters.md 中的参考表提示词
npx -y bun ${SKILL_DIR}/../baoyu-image-gen/scripts/main.ts \
  --promptfiles characters/characters.md \
  --image characters/characters.png --ar 4:3
```

**压缩角色表**（推荐）：
压缩以减少用作引用时的 token 使用：
- 使用可用的图片压缩技能
- 或系统工具：`pngquant`, `optipng`, `sips` (macOS)
- **保持 PNG 格式**，优先无损压缩

**7.2 每页都使用角色引用生成**：

| 技能能力 | 策略 |
|----------|------|
| 支持 `--ref` | 每页都传递 `characters/characters.png` |
| 不支持 `--ref` | 将角色描述添加到每页提示词文件开头 |

**页面生成备份规则**：
- 如果提示词文件存在：重命名为 `prompts/NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.md`
- 如果图片文件存在：重命名为 `NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.png`

```bash
# 示例：**始终**包含 --ref 以保持一致性
npx -y bun ${SKILL_DIR}/../baoyu-image-gen/scripts/main.ts \
  --promptfiles prompts/01-page-xxx.md \
  --image 01-page-xxx.png --ar 3:4 \
  --ref characters/characters.png
```

**重要**：
- 一次只生成一页，确认效果后再生成下一页
- 所有页面必须引用角色表（`--ref`）确保一致性
- 如果某页效果不佳，使用 `--regenerate N` 重新生成

---

### 第 8 步：合并 PDF

```bash
# 使用 ImageMagick
convert pages/manga_page_*.png output/manga_book.pdf

# 或使用 Python 脚本
python scripts/merge_pdf.py --input pages/ --output output/manga_book.pdf

# 或使用 TypeScript 脚本
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts --input pages/ --output {slug}.pdf
```

---

### 第 9 步：输出报告

```markdown
## 生成完成报告

📚 漫画：[主题名称]
🎨 画风：{art}
🎭 基调：{tone}
📐 布局：{layout}
📄 页数：X 页

### 输出文件
- 角色表：characters/characters.png
- 漫画页面：01-page-xxx.png ~ NN-page-xxx.png
- 完整 PDF：{slug}.pdf

### 使用的角色
- {角色A}：讲解者
- {角色B}：学习者
```

---

## 输出目录结构

```
comic/{topic-slug}/
├── source/                    # 原始内容
│   └── source.md
├── analysis.md                # 内容分析
├── storyboard.md              # 分镜脚本
├── characters/                # 角色相关
│   ├── characters.md          # 角色定义
│   └── characters.png         # 角色表图片
├── prompts/                   # 图像提示词
│   ├── 01-cover-{slug}.md
│   ├── 02-page-{slug}.md
│   └── ...
├── 01-cover-{slug}.png        # 生成的图片
├── 02-page-{slug}.png
├── ...
└── {slug}.pdf                 # 最终 PDF
```

---

## 页面修改

| 操作 | 步骤 |
|------|------|
| **编辑** | **先更新提示词文件** → `--regenerate N` → 重新生成 PDF |
| **添加** | 在位置创建提示词 → 用角色引用生成 → 后续页重新编号 → 更新分镜 → 重新生成 PDF |
| **删除** | 移除文件 → 后续页重新编号 → 更新分镜 → 重新生成 PDF |

**重要**：更新页面时，**始终**先更新提示词文件 (`prompts/NN-{cover|page}-[slug].md`) 再重新生成。这确保变更被记录和可复现。

---

## 环境要求

- Node.js 18+
- 环境变量：`GEMINI_API_KEY` 或 `TUZI_API_KEY`

安装依赖：

```bash
cd scripts
npm install
```

---

## 配置扩展 (EXTEND.md)

在以下位置创建 `EXTEND.md` 自定义默认设置：

- 项目级：`.baoyu-skills/baoyu-comic/EXTEND.md`
- 用户级：`~/.baoyu-skills/baoyu-comic/EXTEND.md`

```yaml
# 默认设置
defaults:
  art: manga
  tone: warm
  layout: standard
  language: zh-CN

# 水印设置
watermark:
  enabled: true
  text: "Created by Manga Learning Creator"
  position: bottom-right

# 自定义角色库
character_presets:
  doraemon:
    讲解者: 哆啦A梦
    学习者: 大雄
  conan:
    讲解者: 柯南
    学习者: 小兰
```

---

## 参考文件

**核心模板**：
- `references/analysis-framework.md` - 深度内容分析
- `references/character-template.md` - 角色定义格式
- `references/storyboard-template.md` - 分镜结构
- `references/ohmsha-guide.md` - 欧姆社漫画 specifics

**风格定义**：
- `references/art-styles/` - 画风（ligne-claire, manga, realistic, ink-brush, chalk）
- `references/tones/` - 基调（neutral, warm, dramatic, romantic, energetic, vintage, action）
- `references/presets/` - 带特殊规则的预设（ohmsha, wuxia, shoujo）
- `references/layouts/` - 布局（standard, cinematic, dense, splash, mixed, webtoon）

**工作流**：
- `references/workflow.md` - 完整工作流详情
- `references/auto-selection.md` - 内容信号分析
- `references/partial-workflows.md` - 部分工作流选项

**配置**：
- `references/config/preferences-schema.md` - EXTEND.md 模式
- `references/config/first-time-setup.md` - 首次设置
- `references/config/watermark-guide.md` - 水印配置

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

**检测优先级**：
1. `--lang` 标志（显式）
2. EXTEND.md `language` 设置
3. 用户对话语言
4. 源内容语言

**规则**：对所有交互使用用户的输入语言或保存的语言偏好：
- 分镜大纲和场景描述
- 图像生成提示词
- 用户选择选项和确认
- 进度更新、问题、错误、摘要

技术术语保持英文。

---

## 版本历史

- **v2.4.3** (2026-02-15): 上游 hash 同步 (8f1c4a6)
  - 同步上游仓库最新提交
  - 上游新 commits 主要针对 baoyu-post-to-x 和 baoyu-post-to-wechat，不涉及本技能
  - 保留本地完整中文 SKILL.md 内容

- **v2.4.2** (2026-02-12): 上游 hash 同步 (6cc8627)
  - 同步上游 v1.33.0 变更
  - 上游新增技能，本技能内容无变化

- **v2.4.1** (2026-02-11): 上游 hash 同步 (9ff468a)
  - 上游仓库有新提交但未涉及本技能内容变更
  - 脚本和 references 文件均无变化

- **v2.4.0** (2026-02-08): 上游同步 (hash 6cbf0f4)
  - 同步上游 references 目录（画风、基调、布局、预设、工作流、配置等完整定义文件）
  - 同步上游 merge-to-pdf.ts 脚本
  - 本地保留完整中文 SKILL.md 内容和自定义角色库

- **v2.3.0** (2026-02-07): 上游同步 + 功能合并
  - 同步上游 hash 7465f37
  - 合并上游功能变更：`--preset` 参数重命名为 `--style`
  - 上游 `--art` 默认值改为 ligne-claire，本地保留 manga 作为默认（自定义选择）
  - 上游重构为精简主文档 + references 引用架构，本地保留完整中文内容

- **v2.1.1** (2026-02-03): 上游哈希同步
  - 同步上游 baoyu-comic v2.1 最新提交
  - 当前为融合增强版，功能比上游原版更丰富（完整中文支持、自定义角色库）
  - 保持与上游核心功能兼容

- **v2.1.0** (2026-02-02): 上游 baoyu-comic v2.1 同步
  - 更新工作流程 Step 7：先生成角色表再生成页面
  - 添加 `--ref` 角色引用机制确保一致性
  - 合并新的预设和自动选择功能
  - 增加部分工作流选项（--storyboard-only, --prompts-only, --images-only, --regenerate）
  - 添加兼容性矩阵指导风格选择
  - 改进备份规则（时间戳命名）
  - 增加进度检查清单

- **v2.0.0** (2026-01-30): 重大升级
  - 新增 5 种画风、7 种基调、6 种布局选项
  - 新增 3 种预设模式（ohmsha、wuxia、shoujo）
  - 新增角色表机制确保一致性
  - 新增自动 PDF 合并
  - 完善 9 步工作流程
  - 新增 EXTEND.md 配置支持

- **v1.0.0**: 初始版本
  - 基础漫画生成功能
  - 支持自定义角色
  - Gemini API 集成
