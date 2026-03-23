# AI 写作模式详细参考

本文档提供24种AI写作模式的详细定义、检测方法和修复指南。

---

## 内容模式 (Content Patterns)

### 模式 1: 过度强调意义 (Symbolic Overemphasis)

**定义**：夸大事物的历史、文化或象征意义，让普通事件看起来具有里程碑式的重要性。

**信号词/短语**：
- 中文：「标志着」「具有里程碑意义」「开创性的」「划时代的」「历史性的」「前所未有的」
- 英文：「marks a pivotal moment」「groundbreaking」「unprecedented」「revolutionary」

**检测规则**：
- 每1000字超过2次使用上述短语
- 没有具体数据或事实支撑的重大声明

**修复指南**：
1. 识别夸张的意义声明
2. 用具体的事实或数据替代
3. 如果没有具体内容支撑，删除该声明

**示例**：
| 原文 | 修复后 |
|------|--------|
| 这标志着行业的一个关键转折点 | 这改变了30%企业的运营方式 |
| 这项具有里程碑意义的成就 | 这个项目按时完成了 |

---

### 模式 2: 知名度堆砌 (Name-Dropping)

**定义**：声称某事已被「广泛报道」或「获得国际认可」，但不提供任何具体来源。

**信号词/短语**：
- 中文：「广受好评」「备受瞩目」「引发广泛关注」「获得业界一致认可」
- 英文：「widely acclaimed」「internationally recognized」「garnered significant attention」

**检测规则**：
- 知名度声明后没有引用来源
- 使用模糊的群体作为认可来源

**修复指南**：
1. 删除无来源的知名度声明
2. 或者添加具体的引用（媒体名称、日期、奖项等）

---

### 模式 3: -ing结尾的浅层分析 (Shallow -ing Analysis)

**定义**：用-ing动词结尾来制造正在进行深度分析的假象，但实际上只是表面描述。

**信号词/短语**：
- 英文：「exploring」「demonstrating」「highlighting」「showcasing」「examining」「investigating」

**检测规则**：
- 同一段落中多个-ing动词
- -ing动词后没有具体的分析内容

**修复指南**：
1. 将-ing动词改为具体的动作结果
2. 添加实际的分析内容

**示例**：
| 原文 | 修复后 |
|------|--------|
| The study is exploring new methods | The study tested three new methods and found... |

---

### 模式 4: 模糊归因 (Vague Attribution)

**定义**：引用不明确或不可核实的来源。

**信号词/短语**：
- 中文：「专家表示」「研究表明」「据报道」「业内人士认为」「有关部门指出」
- 英文：「experts say」「studies show」「according to reports」「sources indicate」

**检测规则**：
- 引用后没有具体的专家名称或研究引用
- 使用集体名词作为信息来源

**修复指南**：
1. 添加具体的专家姓名、职位、单位
2. 添加具体的研究引用（作者、年份、期刊）
3. 如果无法核实，删除该声明或改为个人观点

---

### 模式 5: 宣传性语言 (Propaganda Language)

**定义**：使用过于正面、推销性的形容词和副词。

**信号词/短语**：
- 中文：「令人惊叹」「独一无二」「无与伦比」「完美」「最佳」「绝对」
- 英文：「amazing」「incredible」「unparalleled」「perfect」「ultimate」「absolutely」

**检测规则**：
- 形容词过于极端（最、绝对、完美等）
- 没有对比数据支撑的优势声明

**修复指南**：
1. 用中性描述替代
2. 添加具体的对比数据
3. 让读者自己得出结论

---

### 模式 6: 模板化结构 (Template Structure)

**定义**：使用「挑战与展望」「问题与机遇」等公式化的章节结构。

**特征**：
- 每篇文章都有相似的开头/结尾结构
- 「首先...其次...最后」的固定顺序
- 「挑战」和「机遇」成对出现

**修复指南**：
1. 根据具体内容定制结构
2. 打破固定的段落顺序
3. 如果内容不需要「展望」部分，就不写

---

## 语言/语法模式 (Language/Grammar Patterns)

### 模式 7: AI词汇滥用 (AI Vocabulary Overuse)

**详见**: `vocabulary.md` 完整词汇表

**检测规则**：
- 计算每1000字中AI典型词的出现频率
- 人类基线：每1000字 1.5 个
- 警告阈值：每1000字 3 个以上
- 危险阈值：每1000字 5 个以上

---

### 模式 8: 系动词回避 (Copula Avoidance)

**定义**：用复杂短语替代简单的「是」「为」。

**示例**：
| AI写法 | 人类写法 |
|--------|----------|
| serves as | is |
| functions as | is |
| acts as | is |
| represents | is |

**检测规则**：
- 「serves as」「functions as」等短语的出现频率

**修复指南**：直接使用「是」「为」

---

### 模式 9: 否定排比 (Negation Parallelism)

**定义**：过度使用「不仅...而且...」「既...又...」等排比结构。

**检测规则**：
- 同一文档中出现3次以上相同的排比结构
- 每个段落都有排比句

**修复指南**：
1. 用简单句替代部分排比
2. 保持句式多样性

---

### 模式 10: 三连排比 (Rule of Three)

**定义**：强制性地使用三个并列项。

**示例**：「快速、高效、可靠」「创新、协作、共赢」

**检测规则**：
- 文章中三项列表的比例过高
- 三项列表中有明显的凑数项

**修复指南**：
- 根据实际需要调整列表长度
- 两项就够用时不要强凑三项

---

### 模式 11: 同义词循环 (Synonym Cycling)

**定义**：在同一段落中用多个同义词描述同一事物，试图避免重复但造成混乱。

**示例**：「研究/调查/探索」「重要/关键/至关重要/不可或缺」

**检测规则**：
- 同义词组在同一段落中出现
- 指代同一事物但用词不一致

**修复指南**：
- 选择最准确的一个词
- 保持用词一致

---

### 模式 12: 虚假范围 (False Scope)

**定义**：使用「从A到B」结构夸大覆盖范围。

**示例**：「从初学者到专家」「从小型企业到大型集团」「从理论到实践」

**检测规则**：
- 「从...到...」结构没有具体数据支撑
- 范围声明与实际内容不符

**修复指南**：
- 如果范围不重要，直接删除
- 如果重要，用具体数据说明

---

## 风格模式 (Style Patterns)

### 模式 13-18

详见 SKILL.md 第三部分。

---

## 交流模式 (Communication Patterns)

### 模式 19-24

详见 SKILL.md 第四部分。

---

## 检测优先级

| 优先级 | 模式 | 严重程度 |
|--------|------|----------|
| P1 | AI词汇滥用 | 高 |
| P1 | 机器人痕迹 | 高 |
| P1 | 知识截止声明 | 高 |
| P2 | 过度强调意义 | 中 |
| P2 | 模糊归因 | 中 |
| P2 | 模板化结构 | 中 |
| P3 | 破折号过度 | 低 |
| P3 | 加粗过度 | 低 |
| P3 | 表情符号 | 低 |

---

## Stop Slop 结构模式（新增借鉴）

### 模式 A: 虚假主语 (False Agency)

**定义**：使用抽象主体隐藏实际执行动作的人。

**示例：**
| 原文 | 修复后 |
|------|--------|
| "The decision emerges from the committee" | "The committee decided" |
| "The complaint becomes a fix" | "Users' complaints led us to create a fix" |
| "the system enables teams to..." | "Our platform helps teams..." |
| "the solution addresses the issue" | "We built X to solve Y" |

---

### 模式 B: 被动语态过度 (Passive Voice Overuse)

**定义**：过度使用被动语态，隐藏行动者。

**示例：**
| 原文 | 修复后 |
|------|--------|
| "Changes were made to the policy" | "We updated the policy" |
| "It was found that the drug was effective" | "Researchers found the drug reduced symptoms by 40%" |
| "The data shows a significant correlation" | "Our analysis found a strong correlation" |

---

### 模式 C: 二元对比 (Binary Contrasts)

**定义**：使用 "Not X. But Y." 结构制造虚假戏剧性。

**示例：**
| 原文 | 修复后 |
|------|--------|
| "Not everyone agrees. But we believe..." | "We believe..." |
| "It's not about X. It's about Y." | 直接陈述 Y 的具体内容 |

---

### 模式 D: 负面列表 (Negative Listing)

**定义**：先否定再肯定的结构，用"不是什么"来定义"是什么"。

**示例：**
| 原文 | 修复后 |
|------|--------|
| "Not a simple tool. Not a basic calculator. A complete solution." | 直接说明产品是什么 |
| "This isn't just about cost. It's not about speed. It's about reliability." | 直接说明核心优势 |

---

### 模式 E: 远距离叙述者 (Distant Narrator)

**定义**：使用 "Nobody designed this" 等叙述方式，让读者感觉置身事外。

**示例：**
| 原文 | 修复后 |
|------|--------|
| "Nobody could have predicted this" | "We didn't predict X" |
| "It goes without saying" | 删除，或直接说明 |

---

## 参考来源

- Wikipedia: Signs of AI writing (WikiProject AI Cleanup)
- blader/humanizer
- hardikpandya/stop-slop
