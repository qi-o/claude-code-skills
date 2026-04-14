---
name: webnovel-init
description: |
  深度初始化网文项目。通过分阶段交互收集完整创作信息，调用 InkOS 创建标准化项目结构。
  触发场景：
  (1) 用户说"新建网文项目"、"初始化小说"、"创建网文"、"开始写小说"、"/webnovel-init"
  (2) 用户想从零开始创作一部新网文
  Do NOT use for importing existing novels (use webnovel-import instead).
allowed-tools: Read Write Edit Grep Bash Task AskUserQuestion WebSearch WebFetch
---

# Project Initialization (InkOS 集成版)

## 目标

- 通过结构化交互收集足够信息，避免"先生成再返工"
- 调用 InkOS `book create` 创建标准化项目结构
- 产出 InkOS 标准 `books/{id}/` 目录结构，包含 Truth Files
- 保证后续 `/webnovel-plan` 与 `/webnovel-write` 可直接运行

## 执行原则

1. 先收集，再生成；未过充分性闸门，不执行 `inkos book create`。
2. 分波次提问，每轮只问"当前缺失且会阻塞下一步"的信息。
3. 允许调用 `Read/Grep/Bash/Task/AskUserQuestion/WebSearch/WebFetch` 辅助收集。
4. 用户已明确的信息不重复问；冲突信息优先让用户裁决。

## 引用加载等级（strict, lazy）

- L0：未确认任务前，不预加载参考。
- L1：每个阶段仅加载该阶段"必读"文件。
- L2：仅在题材、金手指、创意约束触发条件满足时加载扩展参考。
- L3：市场趋势类、时效类资料仅在用户明确要求时加载。

路径约定：
- `references/...` 相对当前 skill 目录。

默认加载清单：
- L1（启动前）：`references/genre-tropes.md`
- L2（按需）：
  - 世界观：`references/worldbuilding/faction-systems.md`
  - 创意约束：按下方"逐文件引用清单"触发加载
- L3（显式请求）：
  - `references/creativity/market-trends-2026.md`

## References（逐文件引用清单）

### 根目录
- `references/genre-tropes.md` — 题材归一化、题材特征提示。所有项目必读。

### worldbuilding
- `references/worldbuilding/character-design.md` — Step 2 角色维度补问
- `references/worldbuilding/faction-systems.md` — Step 4 势力格局设计
- `references/worldbuilding/power-systems.md` — Step 4 力量体系
- `references/worldbuilding/setting-consistency.md` — Step 6 一致性检查
- `references/worldbuilding/world-rules.md` — Step 4 世界规则

### creativity
- `references/creativity/creativity-constraints.md` — Step 5 创意约束包
- `references/creativity/category-constraint-packs.md` — Step 5 约束包模板
- `references/creativity/creative-combination.md` — 复合题材融合
- `references/creativity/inspiration-collection.md` — 用户卡顿时灵感
- `references/creativity/selling-points.md` — Step 5 卖点生成
- `references/creativity/market-positioning.md` — 平台定位
- `references/creativity/market-trends-2026.md` — 市场趋势（L3）
- `references/creativity/anti-trope-xianxia.md` — 反套路库（修仙/玄幻）
- `references/creativity/anti-trope-urban.md` — 反套路库（都市/历史）
- `references/creativity/anti-trope-game.md` — 反套路库（游戏/科幻/末世）
- `references/creativity/anti-trope-rules-mystery.md` — 反套路库（规则/悬疑/克苏鲁）

## 交互流程（Deep）

### Step 0：预检与上下文加载

必须做：
- 确认当前目录可写
- 确认 InkOS 项目可用（`E:\inkos-master` 或通过 `inkos --version` 检查）
- 加载最小参考：`references/genre-tropes.md`

输出：
- 进入 Deep 采集前的"已知信息清单"和"待收集清单"

### Step 1：故事核与商业定位

收集项（必收）：
- 书名（可先给工作名）
- 题材（支持 A+B 复合题材）
- 目标规模（总字数或总章数）
- 一句话故事
- 核心冲突
- 目标读者/平台

题材集合（用于归一化与映射）：
- 玄幻修仙类：修仙 | 系统流 | 高武 | 西幻 | 无限流 | 末世 | 科幻
- 都市现代类：都市异能 | 都市日常 | 都市脑洞 | 现实题材 | 黑暗题材 | 电竞 | 直播文
- 言情类：古言 | 宫斗宅斗 | 青春甜宠 | 豪门总裁 | 职场婚恋 | 民国言情 | 幻想言情 | 现言脑洞 | 女频悬疑 | 狗血言情 | 替身文 | 多子多福 | 种田 | 年代
- 特殊题材：规则怪谈 | 悬疑脑洞 | 悬疑灵异 | 历史古代 | 历史脑洞 | 游戏体育 | 抗战谍战 | 知乎短篇 | 克苏鲁

### Step 2：角色骨架与关系冲突

收集项（必收）：
- 主角姓名、欲望、缺陷
- 主角结构（单主角/多主角）
- 感情线配置（无/单女主/多女主）
- 反派分层（小/中/大）与镜像对抗

### Step 3：金手指与兑现机制

收集项（必收）：
- 金手指类型（可为"无金手指"）
- 名称/系统名、风格、可见度
- 不可逆代价（必须有代价）
- 成长节奏

### Step 4：世界观与力量规则

收集项（必收）：
- 世界规模、力量体系类型
- 势力格局、社会阶层与资源分配

### Step 5：创意约束包（差异化核心）

流程：
1. 基于题材映射加载反套路库（最多 2 个）
2. 生成 2-3 套创意包
3. 三问筛选
4. 展示五维评分
5. 用户选择最终方案

### Step 6：一致性复述与最终确认

输出"初始化摘要草案"并让用户确认。

## 内部数据模型（初始化收集对象）

```json
{
  "project": {
    "title": "",
    "genre": "",
    "target_words": 0,
    "target_chapters": 0,
    "one_liner": "",
    "core_conflict": "",
    "target_reader": "",
    "platform": ""
  },
  "protagonist": { "name": "", "desire": "", "flaw": "", "archetype": "", "structure": "单主角" },
  "relationship": { "heroine_config": "", "antagonist_tiers": {}, "antagonist_mirror": "" },
  "golden_finger": { "type": "", "name": "", "style": "", "visibility": "", "irreversible_cost": "", "growth_rhythm": "" },
  "world": { "scale": "", "factions": "", "power_system_type": "", "social_class": "" },
  "constraints": { "anti_trope": "", "hard_constraints": [], "core_selling_points": [], "opening_hook": "" }
}
```

## 充分性闸门（必须通过）

未满足以下条件前，禁止执行 `inkos book create`：

1. 书名、题材已确定
2. 目标规模可计算
3. 主角姓名 + 欲望 + 缺陷完整
4. 世界规模 + 力量体系类型完整
5. 金手指类型已确定
6. 创意约束已确定（反套路 1 条 + 硬约束 2 条，或用户明确拒绝）

## 执行生成

### 1) 调用 InkOS 创建项目

```bash
# 构建 InkOS book create 命令
inkos book create \
  --title "{书名}" \
  --genre "{题材归一化值}" \
  --strand-weave \
  --anti-trope "{题材对应的反套路 genre}" \
  --idea "{一句话故事 + 核心冲突 + 主角设定}"
```

InkOS 自动创建：
```
books/{book-id}/
├── book.json               # 书籍配置（含 genre、target）
├── chapters/
│   └── index.json          # 章节索引
└── story/
    ├── story_bible.md      # 世界观设定
    ├── volume_outline.md   # 卷大纲
    ├── book_rules.md       # 题材规则 + webnovelCraft 配置
    ├── current_state.md    # 当前叙事状态
    ├── particle_ledger.md  # 资源追踪
    ├── pending_hooks.md    # 伏笔/悬念池
    ├── chapter_summaries.md # 章节摘要
    ├── author_intent.md    # 作者意图
    ├── current_focus.md    # 近期焦点
    ├── craft_state.md      # Craft 状态（strand/contract/violations）
    └── craft_snapshots/    # Craft 快照目录
```

### 2) 补充 Truth Files

InkOS 的 Architect agent 自动生成基础设定文件。
如需补充，手动编辑以下文件：

- `story/story_bible.md` — 补充世界观细节
- `story/author_intent.md` — 写入核心冲突、故事核
- `story/book_rules.md` — 确认 webnovelCraft 配置

### 3) 写入创意约束

将创意约束写入 `story/book_rules.md` 的 YAML frontmatter：

```yaml
webnovelCraft:
  enabled: true
  strandWeave:
    questWeight: 60
    fireWeight: 25
    constellationWeight: 15
    enforcement: flexible
  antiTrope:
    genre: xianxia
  contractV2:
    enabled: true
    differentiationWindow: 5
  creativeConstraints:
    - name: "{约束包名}"
      rules: ["..."]
      hardConstraints: ["..."]
      sellingPoints: ["..."]
  hilGate:
    forceTriggers: [p1_failure, anti_ai_failure, dimension_below_70]
    suggestTriggers: [first_chapter, volume_end]
```

## 验证与交付

```bash
# 检查项目已创建
inkos book list

# 检查项目状态
inkos status <book-id>

# 检查 Truth Files 存在
ls books/<book-id>/story/
```

成功标准：
- `inkos book list` 显示新书
- `inkos status` 显示正确的基础信息
- `book_rules.md` 包含 `webnovelCraft` 配置
- `craft_state.md` 存在

## 失败处理

1. `inkos book create` 失败 → 检查 InkOS 配置和日志
2. Truth Files 不完整 → 手动编辑补充
3. 创意约束未写入 → 编辑 `book_rules.md` frontmatter

---

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 项目初始化完成 | 使用 `webnovel-plan` — 网文大纲规划 |
| 需要导入已有作品 | 使用 `webnovel-import` — 已有作品导入 |

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 充分性闸门通过确认 | 6 项充分性条件全部满足，准备执行 `inkos book create` 时 | 展示初始化摘要草案（书名/题材/主角/世界观/金手指/创意约束），获取最终确认 |
| 创意约束方案选择 | 生成了 2-3 套创意约束包时 | 展示各方案的反套路规则、硬约束和卖点五维评分，请用户选择 |
| 题材归一化 | 用户输入的题材与标准集合不完全匹配时 | 展示归一化映射结果，确认映射是否准确（如"修真"→"修仙"） |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| InkOS 不可用 | `inkos --version` 或 `inkos book create` 返回命令未找到 | 引导用户安装/配置 InkOS，或检查 `E:\inkos-master` 路径是否正确 |
| 充分性闸门未通过 | 6 项条件中有任一缺失 | 暂停执行，展示缺失项清单，回到对应 Step 补充收集 |
| Truth Files 不完整 | `inkos status` 显示 story/ 目录下文件缺失 | 手动编辑补充缺失的 Truth File（story_bible.md/author_intent.md 等） |
| 项目 ID 冲突 | `inkos book create` 报告同名项目已存在 | 提示用户选择：使用不同书名/ID，或删除已有项目后重新创建 |
