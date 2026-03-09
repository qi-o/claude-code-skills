# Layout Patterns with GridSpec

## Overview

GridSpec provides flexible subplot layouts with precise control over spacing and size ratios. This document covers common patterns for scientific figures.

## Basic Syntax

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(width, height))
gs = GridSpec(nrows, ncols, figure=fig,
              left=0.10, right=0.95, top=0.92, bottom=0.08,
              wspace=0.35, hspace=0.35)

ax = fig.add_subplot(gs[row, col])
```

## Standard Layouts

### 2脳2 Grid (Most Common)

```python
fig = plt.figure(figsize=(7.08, 7.5))
gs = GridSpec(2, 2, figure=fig,
              left=0.10, right=0.95, top=0.92, bottom=0.08,
              wspace=0.35, hspace=0.35)

ax_a = fig.add_subplot(gs[0, 0])  # Top-left
ax_b = fig.add_subplot(gs[0, 1])  # Top-right
ax_c = fig.add_subplot(gs[1, 0])  # Bottom-left
ax_d = fig.add_subplot(gs[1, 1])  # Bottom-right
```

**Use for**: Main manuscript figures with 4 related panels.

### 1脳3 Horizontal

```python
fig = plt.figure(figsize=(7.08, 3.0))
gs = GridSpec(1, 3, figure=fig,
              left=0.08, right=0.95, top=0.85, bottom=0.18,
              wspace=0.30)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
```

**Use for**: Comparing three conditions side-by-side.

### 2脳3 Grid

```python
fig = plt.figure(figsize=(7.08, 5.5))
gs = GridSpec(2, 3, figure=fig,
              left=0.08, right=0.95, top=0.92, bottom=0.10,
              wspace=0.30, hspace=0.40)

axes = []
for i in range(6):
    ax = fig.add_subplot(gs[i // 3, i % 3])
    axes.append(ax)
```

**Use for**: Six panels with equal weight.

### 3脳1 Vertical Stack

```python
fig = plt.figure(figsize=(3.35, 7.0))
gs = GridSpec(3, 1, figure=fig,
              left=0.18, right=0.95, top=0.95, bottom=0.08,
              hspace=0.30)

ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[1, 0])
ax_c = fig.add_subplot(gs[2, 0])
```

**Use for**: Single-column figures, time series stacked vertically.

## Unequal Panel Sizes

### Full-Width Top Panel

```python
fig = plt.figure(figsize=(7.08, 6.0))
gs = GridSpec(2, 2, figure=fig,
              height_ratios=[1.2, 1],  # Top row taller
              left=0.10, right=0.95, top=0.92, bottom=0.08,
              wspace=0.30, hspace=0.35)

ax_a = fig.add_subplot(gs[0, :])   # Full width top
ax_b = fig.add_subplot(gs[1, 0])   # Bottom-left
ax_c = fig.add_subplot(gs[1, 1])   # Bottom-right
```

### Wide Left Panel

```python
fig = plt.figure(figsize=(7.08, 4.0))
gs = GridSpec(2, 3, figure=fig,
              width_ratios=[2, 1, 1],  # Left column wider
              left=0.08, right=0.95, top=0.90, bottom=0.12,
              wspace=0.25, hspace=0.35)

ax_a = fig.add_subplot(gs[:, 0])   # Full height left
ax_b = fig.add_subplot(gs[0, 1])   # Top-middle
ax_c = fig.add_subplot(gs[0, 2])   # Top-right
ax_d = fig.add_subplot(gs[1, 1])   # Bottom-middle
ax_e = fig.add_subplot(gs[1, 2])   # Bottom-right
```

### Schematic + Data

```python
fig = plt.figure(figsize=(7.08, 4.5))
gs = GridSpec(1, 3, figure=fig,
              width_ratios=[1.5, 1, 1],  # Schematic wider
              left=0.05, right=0.95, top=0.88, bottom=0.15,
              wspace=0.25)

ax_a = fig.add_subplot(gs[0, 0])   # Schematic
ax_b = fig.add_subplot(gs[0, 1])   # Data plot 1
ax_c = fig.add_subplot(gs[0, 2])   # Data plot 2
```

## Nested GridSpec

For complex layouts with sub-grids:

```python
fig = plt.figure(figsize=(7.08, 7.5))

# Outer grid
outer_gs = GridSpec(2, 1, figure=fig, height_ratios=[1, 1.5],
                    left=0.08, right=0.95, top=0.92, bottom=0.08,
                    hspace=0.30)

# Top row: single panel
ax_a = fig.add_subplot(outer_gs[0])

# Bottom row: nested 1脳3 grid
inner_gs = outer_gs[1].subgridspec(1, 3, wspace=0.25)
ax_b = fig.add_subplot(inner_gs[0])
ax_c = fig.add_subplot(inner_gs[1])
ax_d = fig.add_subplot(inner_gs[2])
```

## Inset Axes

For adding magnified regions or small plots within larger ones:

```python
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

fig, ax = plt.subplots(figsize=(5, 4))

# Main plot
ax.plot(x, y)

# Inset in upper-right corner
ax_inset = inset_axes(ax, width="40%", height="35%", loc='upper right',
                      borderpad=1.5)
ax_inset.plot(x_zoom, y_zoom)
ax_inset.set_xlim(x_min, x_max)
```

## Common Margin Settings

| Layout | left | right | top | bottom | wspace | hspace |
|--------|------|-------|-----|--------|--------|--------|
| 2脳2 | 0.10 | 0.95 | 0.92 | 0.08 | 0.35 | 0.35 |
| 1脳3 | 0.08 | 0.95 | 0.85 | 0.18 | 0.30 | - |
| 1脳2 | 0.08 | 0.95 | 0.88 | 0.15 | 0.25 | - |
| 3脳1 | 0.18 | 0.95 | 0.95 | 0.08 | - | 0.30 |
| Wide panel | 0.05 | 0.95 | 0.88 | 0.15 | 0.25 | 0.35 |

## Adjusting for Content

### Wide Y-axis Labels
```python
gs = GridSpec(..., left=0.15)  # Increase left margin
add_panel_label(ax, 'A', x=-0.18)  # Adjust panel label
```

### Rotated X-axis Labels
```python
gs = GridSpec(..., bottom=0.20)  # Increase bottom margin
```

### Colorbar
```python
gs = GridSpec(..., right=0.88)  # Leave room on right
cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
```

### Legend Outside
```python
gs = GridSpec(..., right=0.82)  # Leave room on right
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
```

## Panel Label Positioning

| Scenario | x | y |
|----------|---|---|
| Standard | -0.12 | 1.08 |
| Wide y-labels | -0.15 | 1.08 |
| No y-labels | -0.08 | 1.08 |
| Below title | -0.12 | 1.15 |

## Tips

1. **Start conservative**: Begin with generous margins, then tighten.
2. **Check at final size**: View at 100% scale before saving.
3. **Use `bbox_inches='tight'`**: Automatically trims whitespace on save.
4. **Consistent spacing**: Keep wspace/hspace similar for visual balance.
5. **Align panel labels**: Use the same x/y coordinates for all panels.
