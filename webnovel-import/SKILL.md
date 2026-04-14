---
name: webnovel-import
description: |
  导入已有小说（大纲/章节/设定）到 InkOS 项目。用于续写已有内容。
  触发场景：
  (1) 用户说"导入小说"、"导入已有章节"、"续写已有小说"、"/webnovel-import"
  (2) 用户已有小说内容（大纲/章节/设定），想导入后继续写作
  Do NOT use for creating a brand new novel from scratch (use webnovel-init instead).
allowed-tools: Read Write Edit Grep Bash Task AskUserQuestion Glob
---

# Novel Import (InkOS 集成版)

## 目标

- 将用户已有小说内容导入 InkOS 项目结构
- 支续两种模式：从零导入（无章节）/ 章节续写（已有章节）
- 导入后可直接使用 `/webnovel-write` 继续写作

## 前置条件

- InkOS 项目已就绪（E:\inkos-master）
- 用户有需要导入的小说内容

## 模式定义

| 模式 | 说明 | 对应 InkOS 命令 |
|------|------|----------------|
| A. 从零导入 | 只有大纲/设定，无章节 | `inkos import chapters` |
| B. 章节续写 | 已有章节，需要继续写 | `inkos import chapters` + `inkos write sync` |

## 交互流程

### Step 0：确认导入模式

询问用户选择：

**A. 从零导入（无章节）**
- 用户只有大纲/设定，还没有写章节
- 需要创建 InkOS 项目结构

**B. 章节续写（已有章节）**
- 用户已有部分章节，需要导入后继续写

### Step 1：收集项目基础信息

两种模式都需要收集：
1. **书名**（作为 book-id）
2. **题材**（genre，用于加载对应参考）
3. **目标规模**（总字数或总章数）

### Step 2：创建 InkOS 项目

```bash
# 在 InkOS 项目中创建新书籍
inkos book create \
  --title "{书名}" \
  --genre "{题材}" \
  --target-words {目标字数}
```

这会创建标准的 InkOS 目录结构：
```
books/{book-id}/
├── book.json           # 书籍配置
├── chapters/
│   └── index.json      # 章节索引
└── story/
    ├── story_bible.md      # 世界设定
    ├── volume_outline.md   # 卷大纲
    ├── book_rules.md       # 题材规则
    ├── current_state.md    # 当前状态
    ├── particle_ledger.md  # 资源追踪
    ├── pending_hooks.md    # 伏笔池
    └── ...
```

### Step 3：导入大纲

将用户的大纲内容写入 InkOS Truth Files：

- **总纲** → `story/volume_outline.md`
- **世界观** → `story/story_bible.md`
- **核心冲突** → `story/author_intent.md`

```bash
# 导入章节内容
inkos import chapters \
  --input "{章节目录路径}" \
  --book-id "{book-id}"
```

InkOS 自动处理：
- 识别章节编号（从文件名或内容标题）
- 规范化文件格式
- 生成章节摘要
- 更新 Truth Files

### Step 4：导入设定（可选）

将用户设定写入 InkOS story 目录：

| 设定类型 | InkOS Truth File |
|----------|-----------------|
| 世界观 | `story/story_bible.md` |
| 角色 | `story/character_matrix.md` |
| 金手指 | `story/book_rules.md` |
| 力量体系 | `story/book_rules.md` |
| 势力 | `story/story_bible.md` |

### Step 5：同步状态（仅模式B）

```bash
# 同步已有章节的 Truth Files
inkos write sync <book-id> --chapter 1
inkos write sync <book-id> --chapter 2
# ... 或批量同步所有章节

# 验证项目状态
inkos status <book-id>
```

InkOS 的 ChapterAnalyzerAgent 自动从每章中提取：
- 角色出场和状态
- 世界观元素
- 伏笔和钩子
- 时间线信息

### Step 6：验证

```bash
# 检查项目完整性
inkos status <book-id>

# 查看导入的章节
inkos book list
```

成功标准：
- `inkos status` 显示正确的章节数和字数
- Truth Files 已更新（current_state.md 反映最新状态）
- 章节索引完整

## 错误处理

| 错误 | 处理 |
|------|------|
| 章节编号识别失败 | 询问用户手动指定编号规则 |
| 导入后状态不一致 | 运行 `inkos write sync` 重建 |
| 文件编码问题 | 尝试 UTF-8 / GBK 自动检测 |

## 后续操作

导入完成后：
1. **开始续写**：`/webnovel-write` 或 `/webnovel-continue`
2. **查看状态**：`inkos status <book-id>`
3. **质量审查**：`inkos audit <book-id>`

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 导入模式选择 | 开始导入流程时 | 确认是"从零导入"还是"章节续写"，两种模式的后续操作不同 |
| 章节编号规则 | `inkos import chapters` 无法自动识别编号 | 询问用户手动指定编号规则（文件名模式/标题提取/手动映射） |
| Truth Files 覆盖 | 导入的设定与已有 Truth Files 冲突 | 展示冲突内容，请用户确认以导入版本为准还是保留已有版本 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| InkOS CLI 失败 | `inkos` 命令返回非零退出码 | 检查 InkOS 项目路径是否正确；手动创建目录结构并写入配置文件 |
| 文件编码问题 | UnicodeDecodeError 或乱码 | 尝试 GBK/GB18030 编码重新读取；使用 chardet 自动检测编码 |
| 导入后状态不一致 | `inkos status` 显示章节数与实际不符 | 运行 `inkos write sync` 逐章重建 Truth Files；手动修复 chapters/index.json |
