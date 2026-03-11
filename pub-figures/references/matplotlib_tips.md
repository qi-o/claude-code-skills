# Matplotlib Tips and Troubleshooting

## Common Pitfalls and Solutions

### Text and Labels

#### Unicode Symbols Not Rendering

**Problem**: Greek letters or special symbols appear as boxes.

**Solution**: Use matplotlib's mathtext:
```python
# Instead of: ax.set_xlabel('螖 Score')
ax.set_xlabel(r'$\Delta$ Score')

# Common symbols:
# 伪: $\alpha$    尾: $\beta$     纬: $\gamma$
# 未: $\delta$    渭: $\mu$       蟽: $\sigma$
# 蟻: $\rho$      卤: $\pm$       脳: $\times$
```

#### Text Clipped on Save

**Problem**: Labels cut off in saved figure.

**Solution**:
```python
# Option 1: Use bbox_inches='tight'
fig.savefig('figure.pdf', bbox_inches='tight')

# Option 2: Adjust subplot params
fig.subplots_adjust(bottom=0.15, left=0.12)

# Option 3: Increase figure size
fig = plt.figure(figsize=(7.5, 5.0))  # Slightly larger
```

#### Overlapping Labels

**Problem**: Tick labels or annotations overlap.

**Solution**:
```python
# Rotate labels
ax.set_xticklabels(labels, rotation=45, ha='right')

# Reduce font size
ax.tick_params(axis='x', labelsize=8)

# Skip every other label
ax.set_xticks(ax.get_xticks()[::2])

# Use auto date locator for dates
from matplotlib.dates import AutoDateLocator
ax.xaxis.set_major_locator(AutoDateLocator())
```

### Colors and Legends

#### Legend Overlapping Data

**Solution**:
```python
# Move outside plot
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1))

# Use best location
ax.legend(loc='best')

# Make semi-transparent
ax.legend(framealpha=0.8)

# Place in empty corner
ax.legend(loc='lower right')
```

#### Colors Too Similar

**Solution**:
```python
# Use distinct categorical palette
colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']

# Or use colormap
import matplotlib.cm as cm
colors = cm.Set1(np.linspace(0, 1, n_categories))
```

#### White Background in Saved Figure

**Problem**: Figure has white background instead of transparent.

**Solution**:
```python
# For PNG with transparency
fig.savefig('figure.png', transparent=True)

# For white background (publication)
fig.savefig('figure.pdf', facecolor='white')
```

### Layout Issues

#### Uneven Panel Sizes

**Problem**: Panels appear different sizes.

**Solution**:
```python
# Use GridSpec for precise control
from matplotlib.gridspec import GridSpec

gs = GridSpec(2, 2, figure=fig, width_ratios=[1, 1], height_ratios=[1, 1])

# Ensure consistent axis limits
for ax in axes:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 100)
```

#### Figure Title Overlaps Panels

**Solution**:
```python
# Adjust top margin
gs = GridSpec(..., top=0.88)  # Leave room for title

# Or use constrained_layout
fig, axes = plt.subplots(2, 2, figsize=(7, 7), constrained_layout=True)
```

#### Colorbar Changes Plot Size

**Solution**:
```python
# Method 1: Shrink colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.8)

# Method 2: Use axes divider
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
```

### Performance

#### Slow Rendering with Many Points

**Solution**:
```python
# Use rasterized=True for dense scatter plots
ax.scatter(x, y, s=1, alpha=0.3, rasterized=True)

# Save as vector with rasterized elements
fig.savefig('figure.pdf', dpi=300)  # Rasterized parts at 300 DPI
```

#### Memory Issues with Large Figures

**Solution**:
```python
# Close figures after saving
plt.close(fig)

# Or close all
plt.close('all')

# Use non-interactive backend
import matplotlib
matplotlib.use('Agg')
```

### Statistical Plots

#### Error Bars Not Visible

**Problem**: Error bars too small or hidden.

**Solution**:
```python
# Increase cap size and line width
ax.errorbar(x, y, yerr=errors, capsize=5, capthick=1.5, linewidth=1.5)

# Use different marker
ax.errorbar(x, y, yerr=errors, fmt='s', markersize=6)
```

#### Box Plot Outliers Overwhelming

**Solution**:
```python
# Customize outlier appearance
ax.boxplot(data, flierprops=dict(marker='.', markersize=3, alpha=0.5))

# Or hide outliers
ax.boxplot(data, showfliers=False)
```

### File Output

#### PDF Text Not Editable in Illustrator

**Solution**:
```python
# Embed fonts
plt.rcParams['pdf.fonttype'] = 42  # TrueType fonts
plt.rcParams['ps.fonttype'] = 42

# Or use Type 3 fonts (smaller file)
plt.rcParams['pdf.fonttype'] = 3
```

#### PNG Has Jagged Edges

**Solution**:
```python
# Increase DPI
fig.savefig('figure.png', dpi=600)

# Use anti-aliasing
plt.rcParams['text.antialiased'] = True
plt.rcParams['lines.antialiased'] = True
```

#### Inconsistent Figure Sizes

**Solution**:
```python
# Always specify figsize
fig = plt.figure(figsize=(7.08, 5.0))

# Don't rely on defaults
plt.rcParams['figure.figsize'] = [7.08, 5.0]
```

## Best Practices

### Figure Setup Template

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

# Publication defaults
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 600,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'pdf.fonttype': 42,
})

# Create figure
fig = plt.figure(figsize=(7.08, 5.0))
gs = GridSpec(1, 2, figure=fig,
              left=0.10, right=0.95, top=0.90, bottom=0.12,
              wspace=0.30)

# Add subplots
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# ... add content ...

# Save
fig.savefig('figure.pdf', bbox_inches='tight', facecolor='white')
fig.savefig('figure.png', dpi=600, bbox_inches='tight', facecolor='white')
plt.close(fig)
```

### Debugging Checklist

1. [ ] Check figure size: `print(fig.get_size_inches())`
2. [ ] Check axes limits: `print(ax.get_xlim(), ax.get_ylim())`
3. [ ] Preview before save: `plt.show()` (interactive mode)
4. [ ] Check font availability: `matplotlib.font_manager.findSystemFonts()`
5. [ ] Verify data: `print(data.describe())`

### Version Compatibility

```python
import matplotlib
print(matplotlib.__version__)

# Common version-specific issues:
# - constrained_layout: requires 3.0+
# - GridSpec subgridspec: requires 3.1+
# - set_box_aspect: requires 3.3+
```
