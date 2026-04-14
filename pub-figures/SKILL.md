---
name: pub-figures
description: |
  Generate publication-quality multi-panel scientific figures for journals.
  Use when users need: journal-grade Figure with A/B/C/D panels, forest plots,
  heatmaps, cascade/flow diagrams, grouped bar charts, or any scientific
  visualization requiring precise alignment, consistent typography, and
  professional styling. Trigger phrases: publication figure, journal figure,
  multi-panel figure, forest plot, scientific visualization, 600 DPI figure.
  触发场景：
  (1) 用户需要发表图、期刊图、多面板图、森林图、热图、科研绘图
  (2) 用户说"发表图"、"期刊图"、"多面板图"、"森林图"、"热图"、"科研绘图"、"publication figure"、"journal figure"、"heatmap"、"forest plot"、"multi-panel"
  Do NOT use for conceptual diagrams or schematics (use scientific-schematics instead) or DICOM imaging (use pydicom instead).
license: MIT
compatibility: Requires Python with matplotlib and seaborn
version: 0.1.0
metadata:
  category: media-tools
---

# Publication-Quality Scientific Figures

## Overview

This skill generates journal-ready multi-panel figures with:
- Consistent panel labeling (A, B, C, D)
- Professional typography (Arial/Helvetica, appropriate sizing)
- Color-blind friendly palettes
- High resolution output (600 DPI for publication)
- Proper layout management using GridSpec

> **前置检查（SOFT 门控）**
>
> 生成图表前建议确认以下条件：
>
> | 检查项 | 建议状态 | 未满足时 |
> |--------|---------|---------|
> | 数据源已确认 | 已有原始数据或模拟数据说明 | 提示用户确认数据来源，允许继续 |
> | 图表类型已选定 | 已确定图表类型和面板布局 | 建议先选定类型，允许继续 |
>
> 这两项为建议性质，用户明确要求时可直接生成。

## Supported Figure Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Multi-panel composite** | 2x2, 1x3, 2x3 GridSpec layouts | Main manuscript figures |
| **Forest plot** | Effect sizes with confidence intervals | Meta-analysis, cohort comparisons |
| **Heatmap** | Annotated matrix visualization | Correlation, expression data |
| **Grouped bar chart** | Side-by-side categorical comparisons | Treatment groups, conditions |
| **Scatter plot** | Correlation/relationship display | Continuous variable relationships |
| **Cascade/Flow diagram** | Pathway or process visualization | Signaling cascades, methods flow |

## Quick Start

When the user provides data and requests a publication figure:

1. **Identify figure type** from user description
2. **Set up publication defaults** (see Design Standards below)
3. **Create layout** with appropriate GridSpec
4. **Add panel labels** with consistent positioning
5. **Export** at 600 DPI in PDF and PNG formats

## Design Standards

### Publication-Quality Defaults

Always apply these rcParams at the start of any figure script:

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 600,
    'axes.linewidth': 1.0,
    'axes.spines.top': False,
    'axes.spines.right': False,
})
```

### Panel Label Function

Use this function for consistent panel labeling:

```python
def add_panel_label(ax, label, fontsize=14, fontweight='bold', x=-0.12, y=1.08):
    """Add panel label (A, B, C, D) consistently positioned."""
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=fontsize, fontweight=fontweight, va='top', ha='left')
```

### Journal Figure Dimensions

| Journal Width | Inches | mm |
|---------------|--------|-----|
| Single column | 3.35 | 85 |
| 1.5 columns | 5.51 | 140 |
| Double column | 7.08 | 180 |

Common figure sizes:
- **2x2 panel**: `figsize=(7.08, 7.5)` (double column, square-ish)
- **1x3 panel**: `figsize=(7.08, 3.5)` (double column, landscape)
- **Single plot**: `figsize=(3.35, 3.0)` (single column)

## Layout Patterns

### 2x2 GridSpec Layout

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(7.08, 7.5))
gs = GridSpec(2, 2, figure=fig,
              left=0.10, right=0.95, top=0.92, bottom=0.08,
              wspace=0.35, hspace=0.35)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[1, 0])
ax_d = fig.add_subplot(gs[1, 1])

# Add panel labels
for ax, label in zip([ax_a, ax_b, ax_c, ax_d], 'ABCD'):
    add_panel_label(ax, label)
```

### 1x3 Horizontal Layout

```python
fig = plt.figure(figsize=(7.08, 3.5))
gs = GridSpec(1, 3, figure=fig,
              left=0.08, right=0.95, top=0.85, bottom=0.15,
              wspace=0.30)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])

for ax, label in zip([ax_a, ax_b, ax_c], 'ABC'):
    add_panel_label(ax, label, x=-0.15)
```

### Unequal Panel Sizes

```python
# Panel A spans full width, B and C below
fig = plt.figure(figsize=(7.08, 6.0))
gs = GridSpec(2, 2, figure=fig, height_ratios=[1.2, 1],
              left=0.10, right=0.95, top=0.92, bottom=0.08,
              wspace=0.30, hspace=0.35)

ax_a = fig.add_subplot(gs[0, :])  # Full width
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[1, 1])
```

## Figure Type Templates

### Forest Plot

```python
def create_forest_plot(ax, cohorts, effects, ci_lower, ci_upper, colors=None):
    """Create forest plot with effect sizes and confidence intervals."""
    y_pos = np.arange(len(cohorts))

    if colors is None:
        colors = ['#2E86AB'] * len(cohorts)

    for i, (eff, lo, hi, c) in enumerate(zip(effects, ci_lower, ci_upper, colors)):
        ci = [[eff - lo], [hi - eff]]
        ax.errorbar(eff, i, xerr=ci, fmt='o', color=c,
                   capsize=4, capthick=1.5, markersize=8,
                   markeredgecolor='white', markeredgewidth=0.5)
        ax.annotate(f'd={eff:.2f}', (eff + 0.1, i), fontsize=8, va='center')

    ax.axvline(x=0, color='#888888', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cohorts)
    ax.set_xlabel('Effect Size')
```

### Annotated Heatmap

```python
def create_heatmap(ax, data, row_labels, col_labels, cmap='RdBu_r', vmin=-1, vmax=1):
    """Create heatmap with value annotations."""
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=8)
    ax.set_yticklabels(row_labels, fontsize=9)

    # Add text annotations
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = data[i, j]
            color = 'white' if abs(val) > 0.6 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                   color=color, fontsize=8, fontweight='medium')

    return im
```

### Cascade/Flow Diagram

```python
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def create_cascade_diagram(ax, labels, colors):
    """Create vertical cascade diagram with arrows."""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2 + len(labels) * 1.8)
    ax.axis('off')

    box_width, box_height = 2.8, 0.9
    x_center = 5

    for i, (label, color) in enumerate(zip(labels, colors)):
        y = len(labels) * 1.8 - i * 1.8 + 0.5

        rect = FancyBboxPatch(
            (x_center - box_width/2, y - box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            facecolor=color, edgecolor='#333333',
            linewidth=1.5, alpha=0.9
        )
        ax.add_patch(rect)
        ax.text(x_center, y, label, ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

        # Arrow to next box
        if i < len(labels) - 1:
            arrow_style = "Simple,tail_width=0.4,head_width=3.5,head_length=3"
            arrow = FancyArrowPatch(
                (x_center, y - box_height/2 - 0.1),
                (x_center, y - 1.8 + box_height/2 + 0.1),
                arrowstyle=arrow_style, color='#333333', lw=1.5
            )
            ax.add_patch(arrow)
```

### Grouped Bar Chart

```python
def create_grouped_bars(ax, categories, group_data, group_labels, colors=None):
    """Create grouped bar chart with error bars."""
    x = np.arange(len(categories))
    n_groups = len(group_data)
    width = 0.8 / n_groups

    if colors is None:
        colors = plt.cm.Set2(np.linspace(0, 1, n_groups))

    for i, (data, label, color) in enumerate(zip(group_data, group_labels, colors)):
        means = [d[0] for d in data]
        stds = [d[1] for d in data]
        offset = (i - n_groups/2 + 0.5) * width
        ax.bar(x + offset, means, width, yerr=stds, label=label,
              color=color, edgecolor='black', linewidth=0.8, capsize=3)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=35, ha='right')
    ax.legend(frameon=True, fancybox=False, edgecolor='#cccccc')
    ax.axhline(y=0, color='#888888', linestyle='--', linewidth=0.8, alpha=0.5)
```

## Color Palettes

### Color-Blind Friendly Palettes

```python
# Primary scientific palette
PALETTE_SCIENTIFIC = {
    'blue': '#2E86AB',
    'magenta': '#A23B72',
    'orange': '#F18F01',
    'teal': '#C73E1D',
    'gray': '#95A5A6'
}

# Category palette (5 colors)
PALETTE_CATEGORICAL = ['#95a5a6', '#3498db', '#9b59b6', '#f39c12', '#e74c3c']

# Diverging (for heatmaps)
CMAP_DIVERGING = 'RdBu_r'

# Sequential
CMAP_SEQUENTIAL = 'viridis'

# Binary (match/mismatch)
from matplotlib.colors import ListedColormap
CMAP_BINARY = ListedColormap(['#e74c3c', '#27ae60'])  # red/green
```

### Species Colors

```python
SPECIES_COLORS = {
    'mouse': '#2E86AB',
    'human': '#A23B72'
}
```

## Export Settings

### Standard Export

```python
# Save in both formats
for fmt in ['pdf', 'png']:
    fig.savefig(output_path / f"Figure_1.{fmt}",
                dpi=600 if fmt == 'png' else None,
                bbox_inches='tight',
                facecolor='white')
plt.close()
```

### With Figure Title

```python
# Add main title before saving
fig.suptitle('Figure 1: Descriptive Title',
             fontsize=14, fontweight='bold', y=0.98)
```

## Common Issues & Solutions

### Legend Overlapping Data

```python
# Move legend outside plot
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), frameon=True)

# Or place in empty corner
ax.legend(loc='lower right', frameon=True, fancybox=False, edgecolor='#cccccc')
```

### Text Clipping on Save

```python
# Always use bbox_inches='tight'
fig.savefig('figure.pdf', bbox_inches='tight')

# If still clipping, adjust subplot params
fig.subplots_adjust(bottom=0.15, right=0.85)
```

### Rotated Labels Overlapping

```python
# Use ha='right' for rotated labels
ax.set_xticklabels(labels, rotation=40, ha='right', fontsize=8)

# Increase bottom margin
gs = GridSpec(..., bottom=0.20)
```

### Unicode Symbols Not Rendering

```python
# Use matplotlib's mathtext instead of Unicode
ax.set_xlabel(r'$\Delta$ Score')  # Delta symbol
ax.set_ylabel(r'Correlation ($\rho$)')  # Greek rho
```

### Inconsistent Panel Label Positions

```python
# Adjust x position based on y-axis label width
add_panel_label(ax, 'A', x=-0.12)  # Standard
add_panel_label(ax, 'A', x=-0.15)  # Wider y-labels
add_panel_label(ax, 'A', x=-0.08)  # No y-labels
```

## Workflow

1. **User Request**: Identify figure type, data source, panel layout
2. **Data Preparation**: Load and validate data
3. **Setup**: Apply rcParams, create figure with appropriate size
4. **Layout**: Create GridSpec with proper margins
5. **Panels**: Generate each subplot with panel labels
6. **Styling**: Apply colors, legends, titles
7. **Export**: Save at 600 DPI in PDF and PNG

## Resources

- `scripts/create_figures.py` - Main figure generation script with CLI
- `scripts/utils.py` - Utility functions (panel labels, color palettes)
- `references/design_standards.md` - Detailed journal requirements
- `references/layout_patterns.md` - GridSpec layout examples
- `references/matplotlib_tips.md` - Common pitfalls and solutions
- `assets/color_palettes.json` - Predefined color schemes

## 推荐下一步

| 触发条件 | 推荐 |
|---------|------|
| 图表完成，需要写论文 | 使用 `academic-writing-suite` — 学术写作编排 |
| 需要转为 PPT 展示 | 使用 `pptx` — PowerPoint 生成 |
| 需要转为 Word 文档 | 使用 `docx` — Word 文档生成 |
| 需要科学示意图 | 使用 `scientific-schematics` — 科学示意图 |

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### Known Fixes & Workarounds
- 在整合第三方 API 服务前，必须先确认 API 费用和账户余额状态
- API 端点 URL 必须与官方文档一致，错误的端点会返回 404
- AutoFigure-Edit API 需要上传 PDF 文件，不是纯文本
- deepScientist.cc 的 API 需要完整的 3 步流程：submit -> poll status -> download
- 某些 API 需要额外的确认步骤（428 状态码），用户需要先在网页上确认扣费

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 数据源确认 | 生成图表前 | 确认原始数据文件路径和数据含义是否正确 |
| 图表类型与布局 | 创建 GridSpec 布局前 | 确认面板数量、排列方式和图表类型是否符合期刊要求 |
| 配色方案选择 | 应用调色板前 | 确认是否需要色盲友好配色，是否与目标期刊风格一致 |
| 导出参数确认 | 保存 PDF/PNG 前 | 确认 DPI（600）、尺寸（单栏/双栏）、文件命名规范 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 中文字体缺失 | 图表中文显示为方块 | 设置 `plt.rcParams['font.sans-serif']` 包含中文字体（SimHei/Microsoft YaHei） |
| 图表元素溢出 | savefig 后文字/标签被裁切 | 使用 `bbox_inches='tight'`，调整 subplot 参数（bottom/right margin） |
| 数据维度不匹配 | 绑定数据到图表时 ValueError | 检查 DataFrame 列名与绘图参数是否一致，确认数据是否需要转置 |
| 第三方 API 调用失败 | HTTP 非 200 或超时 | 检查 API 账户余额和端点 URL，回退到本地 matplotlib 渲染 |