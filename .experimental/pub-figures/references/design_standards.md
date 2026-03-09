# Design Standards for Publication-Quality Figures

## Journal Requirements Overview

Most scientific journals have specific requirements for figure submissions. This document summarizes common standards.

## Typography

### Font Family
- **Primary**: Arial, Helvetica, or sans-serif
- **Avoid**: Times New Roman (except for math), decorative fonts
- **Consistency**: Use the same font family throughout all figures

### Font Sizes (for print at 100%)
| Element | Size Range | Recommended |
|---------|------------|-------------|
| Main title | 12-14 pt | 14 pt |
| Axis labels | 10-12 pt | 10 pt |
| Tick labels | 8-10 pt | 9 pt |
| Legend text | 8-10 pt | 9 pt |
| Annotations | 8-10 pt | 8-9 pt |
| Panel labels | 12-14 pt | 14 pt bold |

### Font Weight
- **Panel labels (A, B, C, D)**: Bold
- **Axis titles**: Normal or bold
- **Axis labels**: Normal
- **Annotations**: Normal or italic

## Dimensions

### Common Journal Widths
| Width Type | mm | inches |
|------------|-----|--------|
| Single column | 85 | 3.35 |
| 1.5 columns | 140 | 5.51 |
| Double column | 180 | 7.08 |

### Aspect Ratios
- **Square plots**: 1:1
- **Wide plots**: 4:3 or 16:9
- **Tall plots**: 3:4

### Maximum Height
- Most journals: 225-250 mm (8.9-9.8 inches)
- A4 page with margins: ~230 mm

## Resolution and File Formats

### Resolution (DPI)
| Use Case | Minimum DPI |
|----------|-------------|
| Line art | 1000-1200 |
| Grayscale | 600 |
| Color photos | 300 |
| Combination | 600 |

### File Formats
| Format | Use Case |
|--------|----------|
| PDF | Vector graphics, best quality |
| EPS | Legacy vector format |
| TIFF | Raster, high quality |
| PNG | Screen, web, raster |
| SVG | Vector, web |

**Recommendation**: Save as PDF (vector) and PNG (600 DPI raster)

## Color Standards

### Color-Blind Friendly Design
- ~8% of males have color vision deficiency
- Avoid red-green combinations as sole differentiator
- Use patterns, shapes, or labels in addition to color

### Recommended Palettes

**Categorical (5 colors)**:
```
Gray:   #95a5a6
Blue:   #3498db
Purple: #9b59b6
Orange: #f39c12
Red:    #e74c3c
```

**Diverging (for heatmaps)**:
- RdBu_r (red-white-blue)
- coolwarm
- PiYG (pink-green)

**Sequential**:
- viridis (recommended)
- plasma
- Blues, Reds

### Color Contrast
- Foreground/background ratio: minimum 4.5:1
- Use black or white text based on background luminance

## Line Styles

### Line Weights
| Element | Weight |
|---------|--------|
| Data lines | 1.5-2.0 pt |
| Error bars | 1.0-1.5 pt |
| Axis lines | 0.5-1.0 pt |
| Grid lines | 0.25-0.5 pt |
| Reference lines | 0.5-1.0 pt dashed |

### Marker Sizes
- Small dataset (< 20 points): 6-10 pt
- Medium dataset (20-100): 4-6 pt
- Large dataset (> 100): 2-4 pt

## Layout Guidelines

### Panel Labels
- Position: Upper-left corner, outside plot area
- Typical coordinates: x=-0.12, y=1.08 (axes coordinates)
- Consistent across all panels

### Margins
- Left margin: 10-12% of figure width
- Right margin: 3-5%
- Top margin: 5-8%
- Bottom margin: 8-12%

### Panel Spacing
- Horizontal (wspace): 0.25-0.40
- Vertical (hspace): 0.30-0.45
- Tighter for related panels, wider for distinct panels

### Legend Placement
- Inside plot if space allows (upper-left, lower-right)
- Outside if overlapping data
- Never cut off by figure boundaries

## Statistical Visualization

### Error Bars
- Show SEM or 95% CI (specify in caption)
- Cap width: 3-5 pt
- Line weight: 1.0-1.5 pt

### Significance Markers
| p-value | Symbol |
|---------|--------|
| < 0.05 | * |
| < 0.01 | ** |
| < 0.001 | *** |
| >= 0.05 | ns |

### Box Plots
- Box: IQR (25th-75th percentile)
- Line: Median
- Whiskers: 1.5脳 IQR or min/max
- Outliers: Individual points

## Common Mistakes to Avoid

1. **Inconsistent panel label positions**
2. **Font sizes too small for print**
3. **Low resolution raster images**
4. **Color combinations inaccessible to color-blind readers**
5. **Legends overlapping data**
6. **Axes labels cut off by figure boundaries**
7. **Inconsistent decimal places in annotations**
8. **Missing scale bars or units**
9. **3D plots when 2D would suffice**
10. **Unnecessary grid lines or chartjunk**

## Pre-Submission Checklist

- [ ] Correct resolution (600+ DPI)
- [ ] Appropriate file format (PDF/TIFF)
- [ ] Figure dimensions within journal limits
- [ ] All text readable at print size
- [ ] Panel labels consistent (A, B, C or a, b, c)
- [ ] Color-blind friendly palette
- [ ] Error bars explained in caption
- [ ] Statistical tests specified
- [ ] Units on all axes
- [ ] No overlapping elements
