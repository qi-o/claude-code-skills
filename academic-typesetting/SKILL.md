---
name: academic-typesetting
description: |
  学术论文排版助手：参考文献格式化、三线表生成、摘要结构润色、换投期刊适配。
  触发场景：
  (1) 用户需要将参考文献转换为 IEEE/APA/Vancouver/Nature 格式
  (2) 用户需要生成学术三线表（Markdown + LaTeX booktabs）
  (3) 用户需要检查或润色摘要结构（五要素诊断）
  (4) 用户需要将论文适配到新的目标期刊格式
  (5) 用户提到"排版"、"文献格式"、"三线表"、"摘要结构"、"换投"、"改投"、"期刊适配"
  当用户的请求涉及论文格式化、排版、引用格式转换时，即使没有明确提到本技能，也应主动使用。
  Do NOT use for: 文献搜索（用 ai4scholar-integration）、完整论文写作（用 academic-writing-suite）、数据可视化图表（用 pub-figures）。
version: 1.0.0
tags: [academic, writing, latex, reference, typesetting]
---

# 学术论文排版助手

根据用户描述，自动识别以下四类任务并执行。任务不明确时先询问用户意图。

## 任务 A：参考文献格式化

**触发关键词**：文献、引用、参考文献、格式化、IEEE、APA、Vancouver、Nature

**处理规则**：

- 未指定目标格式时先询问
- 英文期刊名按标准缩写（如 Nature Commun. / J. Am. Chem. Soc.）
- 作者人数截断规则：

| 格式 | et al. 阈值 |
|------|-------------|
| IEEE | > 6 人 |
| APA | > 3 人 |
| Vancouver | > 3 人 |
| Nature | > 5 人 |

- 页码之间使用 en dash（–）而非减号（-）
- 卷号、期号、页码不得遗漏
- 禁止捏造 DOI 或出版信息；无法确认的字段标注 `[待核实]`
- 格式存疑的条目单独标注，不静默猜测

> **与 ai4scholar auto_cite 的区别**：`auto_cite` 用于从零开始为文本自动查找并标注引用；本任务用于将用户已有的文献列表重新格式化为目标格式。两者互补。

**示例**：

输入：
```
帮我把下面文献改成 IEEE 格式：
Vaswani et al, attention is all you need, 2017, neurips
LeCun Y, Bengio Y, Hinton G. Deep learning. Nature. 2015.
```

输出：
```
[1] A. Vaswani et al., "Attention is all you need," in Advances in Neural
    Information Processing Systems, 2017, vol. 30, pp. 5998–6008.

[2] Y. LeCun, Y. Bengio, and G. Hinton, "Deep learning," Nature, vol. 521,
    no. 7553, pp. 436–444, May 2015.
```

---

## 任务 B：三线表生成

**触发关键词**：三线表、表格、数据表、Table、LaTeX 表

**处理规则**：

- 只有三条横线：顶线、标题线、底线；无竖线，无内部横线
- 数值列按小数点对齐
- 统计显著性标注：`*` p<0.05，`**` p<0.01，`***` p<0.001
- 表题置于表格上方；注记置于表格下方以"注："或"Note."开头
- 百分比保留一位小数，均值±标准差保留两位小数

**输出（按顺序提供）**：

1. Markdown 格式预览
2. LaTeX booktabs 代码（使用 `\toprule`、`\midrule`、`\bottomrule`）
3. 中英文双语表题建议
4. Word 操作提示：清除内部边框以得到三线表效果

**LaTeX 模板**：

```latex
\begin{table}[h]
\centering
\caption{表题}
\begin{tabular}{lcc}
\toprule
\textbf{列1} & \textbf{列2} & \textbf{列3} \\
\midrule
数据行 ... \\
\bottomrule
\end{tabular}
\begin{tablenotes}
  \item Note. 注记内容
\end{tablenotes}
\end{table}
```

---

## 任务 C：摘要结构润色

**触发关键词**：摘要、Abstract、润色、结构、检查摘要

**五要素诊断**：

| 要素 | 含义 | 典型缺陷 |
|------|------|----------|
| 背景 Background | 研究的现实问题或知识空白 | 过于宽泛，未聚焦到具体空白 |
| 问题 Objective | 本研究具体要回答什么 | 缺失或与背景脱节 |
| 方法 Methods | 手段、样本、分析方法 | 过于简略，缺少关键细节 |
| 结果 Results | 核心发现，需包含具体数据 | 无数据支撑，只有定性描述 |
| 意义 Conclusion | 对领域的贡献或实践启示 | 过度解读或过于空泛 |

**输出**：

1. 诊断报告：逐一标注每个要素的状态
   - `存在` — 清晰且充分
   - `模糊` — 存在但表述不够明确
   - `缺失` — 完全未涉及
2. 针对模糊/缺失要素的具体修改建议
3. 修改后的完整摘要（括号标注修改位置）

**约束**：

- 不改变原作者的核心论点和数据
- 中文 200-300 字，英文 150-250 词（未指定字数时的默认范围）
- 不添加原文未提及的数据或结论

---

## 任务 D：换投期刊适配

**触发关键词**：换投、改投、期刊适配、格式适配

**处理规则**：

- 以用户提供的"期刊投稿指南"为最高优先级规则
- 处理范围：参考文献格式、摘要格式、数字规范、单位规范、图表标注
- 未提供指南时，根据已知常见期刊规范处理；不确定的规定主动提示用户核实
- 不改变论文的实质性内容

**输出**：

1. 修改后的文本（括号标注每处修改点）
2. Word 手动设置 Checklist：

```markdown
## Word 手动设置清单

- [ ] 页边距：[目标值]
- [ ] 正文字体/字号：[目标值]
- [ ] 行距：[目标值]
- [ ] 标题层级格式：[目标值]
- [ ] 图表位置：[嵌入文中 / 末尾集中]
- [ ] 页眉/页脚：[要求]
- [ ] 文件格式：[.docx / .pdf / .tex]
```

---

## 通用约束

- 所有修改均标注修改点，方便用户核查
- 禁止捏造任何学术信息（DOI、出版细节、统计数据）
- 遇到无法确认的信息，标注 `[待核实]` 而非猜测

## 与其他技能的协作

| 需求 | 使用技能 |
|------|----------|
| 从零为文本查找并添加引用 | `ai4scholar-integration` (auto_cite) |
| 将已有文献列表重新格式化 | **本技能** 任务 A |
| 生成数据可视化图表 | `pub-figures` |
| 生成学术规范三线表 | **本技能** 任务 B |
| 完整论文写作流程 | `academic-writing-suite` |
| 论文排版/格式适配 | **本技能** 任务 C/D |
