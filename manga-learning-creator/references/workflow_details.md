# Manga Learning Creator — Workflow Details

## Table of Contents

1. [9-Step Workflow (Full Detail)](#9-step-workflow-full-detail)
2. [Character Definition Templates](#character-definition-templates)
3. [Storyboard Template](#storyboard-template)
4. [Image Prompt Template](#image-prompt-template)
5. [Output Directory Structure](#output-directory-structure)
6. [Page Modification Rules](#page-modification-rules)
7. [EXTEND.md Configuration Schema](#extendmd-configuration-schema)
8. [Version History](#version-history)

---

## 9-Step Workflow (Full Detail)

### Progress Checklist

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
  - [ ] 7.1 首先生成角色表 → characters/characters.png
  - [ ] 7.2 每页都使用角色引用 → 用 --ref characters/characters.png
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

---

### 第 1 步：设置与分析

#### 1.1 加载偏好（EXTEND.md）⛔ 阻塞步骤

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

#### 1.2 分析内容

1. 加载用户偏好（检查 EXTEND.md）
2. 阅读用户提供的文本内容
3. 提取核心知识点和学习目标
4. 分析内容类型，推荐画风/基调/布局组合

**内容信号自动检测**：
- 教程/入门 → 推荐 `ohmsha` 预设
- 武侠/古典 → 推荐 `wuxia` 预设
- 爱情/文艺 → 推荐 `shoujo` 预设

#### 1.3 检查现有目录

输出目录：`comic/{topic-slug}/`
- Slug：2-4 个词的 kebab-case（如 `alan-turing-bio`）
- 冲突：附加时间戳（如 `turing-story-20260118-143052`）

处理已存在目录的策略：询问用户：覆盖、备份、或新建

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

#### 3.1 确定漫画角色

**默认角色**：
- 讲解者：智慧老师/专家形象
- 学习者：好奇学生/新手形象

**自定义角色**（用户可指定）：
- 哆啦A梦 + 大雄
- 柯南 + 小兰
- 自定义角色描述

保存到 `characters/characters.md`

#### 3.2 生成分镜脚本

根据内容复杂度规划页数：

| 内容复杂度 | 页数 | 示例 |
|-----------|------|------|
| 简单概念 | 3-5 页 | 单一概念解释 |
| 中等复杂度 | 6-10 页 | 技术教程 |
| 复杂内容 | 10-15 页 | 论文解读 |

---

### 第 4 步：审核大纲（条件性）

如果在第 2 步用户选择了分镜审核：
- 展示 `storyboard.md`
- 询问是否批准或需要修改
- 根据反馈调整

---

### 第 5 步：生成图像提示词

为每页生成详细提示词，保存到 `prompts/NN-{cover|page}-[slug].md`

**备份规则**：如果提示词文件存在，重命名为 `prompts/NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.md`

---

### 第 6 步：审核提示词（条件性）

如果在第 2 步用户选择了提示词审核：
- 展示生成的提示词
- 询问是否批准或需要修改
- 根据反馈调整

---

### 第 7 步：生成图片 ⚠️ 关键

**角色引用对视觉一致性是必需的。**

#### 7.1 首先生成角色表

**备份规则**：如果 `characters/characters.png` 存在，重命名为 `characters/characters-backup-YYYYMMDD-HHMMSS.png`

```bash
# 使用 characters/characters.md 中的参考表提示词
npx -y bun ${SKILL_DIR}/../baoyu-image-gen/scripts/main.ts \
  --promptfiles characters/characters.md \
  --image characters/characters.png --ar 4:3
```

**压缩角色表**（推荐）：
- 使用可用的图片压缩技能
- 或系统工具：`pngquant`, `optipng`, `sips` (macOS)
- **保持 PNG 格式**，优先无损压缩

#### 7.2 每页都使用角色引用生成

| 技能能力 | 策略 |
|----------|------|
| 支持 `--ref` | 每页都传递 `characters/characters.png` |
| 不支持 `--ref` | 将角色描述添加到每页提示词文件开头 |

**页面生成备份规则**：
- 如果提示词文件存在：重命名为 `prompts/NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.md`
- 如果图片文件存在：重命名为 `NN-{cover|page}-[slug]-backup-YYYYMMDD-HHMMSS.png`

```bash
# 示例：始终包含 --ref 以保持一致性
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

## Character Definition Templates

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

---

## Storyboard Template

保存到 `storyboard.md`：

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

## Image Prompt Template

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

---

## Output Directory Structure

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

## Page Modification Rules

| 操作 | 步骤 |
|------|------|
| **编辑** | **先更新提示词文件** → `--regenerate N` → 重新生成 PDF |
| **添加** | 在位置创建提示词 → 用角色引用生成 → 后续页重新编号 → 更新分镜 → 重新生成 PDF |
| **删除** | 移除文件 → 后续页重新编号 → 更新分镜 → 重新生成 PDF |

**重要**：更新页面时，**始终**先更新提示词文件 (`prompts/NN-{cover|page}-[slug].md`) 再重新生成。这确保变更被记录和可复现。

---

## EXTEND.md Configuration Schema

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

## Version History

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
