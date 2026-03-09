#!/usr/bin/env python3
"""
Publication-Quality Figure Generator
====================================
Create journal-ready multi-panel scientific figures with consistent
styling, proper alignment, and professional typography.

Usage:
    python create_figures.py --type <figure_type> --data <data.csv> --output <output_dir>
    python create_figures.py --type forest --data results.csv --output figures/
    python create_figures.py --type heatmap --data matrix.csv --output figures/

Figure Types:
    forest    - Forest plot with effect sizes and CIs
    heatmap   - Annotated heatmap matrix
    bars      - Grouped bar chart with error bars
    scatter   - Scatter plot with regression line
    cascade   - Vertical cascade/flow diagram
    multipanel - Custom multi-panel figure (requires config)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap

from utils import (
    setup_publication_defaults,
    add_panel_label,
    PALETTE_SCIENTIFIC,
    PALETTE_CATEGORICAL,
    SPECIES_COLORS,
    get_journal_figsize
)


def create_forest_plot(
    data: pd.DataFrame,
    output_path: Path,
    cohort_col: str = 'cohort',
    effect_col: str = 'effect_size',
    ci_low_col: Optional[str] = None,
    ci_high_col: Optional[str] = None,
    color_col: Optional[str] = None,
    title: str = 'Forest Plot'
) -> None:
    """
    Create a forest plot showing effect sizes with confidence intervals.

    Args:
        data: DataFrame with cohort, effect size, and optional CI columns
        output_path: Directory to save the figure
        cohort_col: Column name for cohort/study labels
        effect_col: Column name for effect sizes
        ci_low_col: Column name for CI lower bound (optional)
        ci_high_col: Column name for CI upper bound (optional)
        color_col: Column name for color grouping (optional)
        title: Figure title
    """
    setup_publication_defaults()

    fig, ax = plt.subplots(figsize=(5.5, max(3.5, len(data) * 0.5)))

    cohorts = data[cohort_col].values
    effects = data[effect_col].values
    y_pos = np.arange(len(cohorts))

    # Determine colors
    if color_col and color_col in data.columns:
        color_values = data[color_col].values
        unique_colors = list(set(color_values))
        color_map = {v: PALETTE_CATEGORICAL[i % len(PALETTE_CATEGORICAL)]
                     for i, v in enumerate(unique_colors)}
        colors = [color_map[v] for v in color_values]
    else:
        colors = [PALETTE_SCIENTIFIC['blue']] * len(cohorts)

    # Calculate CI if provided
    if ci_low_col and ci_high_col and ci_low_col in data.columns:
        ci_low = data[ci_low_col].values
        ci_high = data[ci_high_col].values
        xerr = np.array([effects - ci_low, ci_high - effects])
    else:
        xerr = np.full((2, len(effects)), 0.1)  # Default small CI

    # Plot
    for i, (eff, c) in enumerate(zip(effects, colors)):
        ax.errorbar(eff, i, xerr=[[xerr[0, i]], [xerr[1, i]]],
                   fmt='o', color=c, capsize=4, capthick=1.5,
                   markersize=8, markeredgecolor='white', markeredgewidth=0.5)
        ax.annotate(f'{eff:.2f}', (eff + xerr[1, i] + 0.05, i),
                   fontsize=8, va='center')

    ax.axvline(x=0, color='#888888', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cohorts)
    ax.set_xlabel('Effect Size')
    ax.set_title(title, fontweight='bold', pad=10)

    # Add legend if color grouping used
    if color_col and color_col in data.columns:
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor=color_map[v],
                   markersize=8, label=v)
            for v in unique_colors
        ]
        ax.legend(handles=legend_elements, loc='upper left',
                  frameon=True, fancybox=False, edgecolor='#cccccc')

    plt.tight_layout()
    save_figure(fig, output_path, 'forest_plot')


def create_heatmap(
    data: pd.DataFrame,
    output_path: Path,
    row_col: str = 'row',
    value_cols: Optional[List[str]] = None,
    cmap: str = 'RdBu_r',
    vmin: float = -1,
    vmax: float = 1,
    title: str = 'Heatmap',
    annotate: bool = True
) -> None:
    """
    Create an annotated heatmap.

    Args:
        data: DataFrame with row labels and value columns
        output_path: Directory to save the figure
        row_col: Column name for row labels
        value_cols: List of column names to display (None = all numeric)
        cmap: Colormap name
        vmin, vmax: Color scale limits
        title: Figure title
        annotate: Whether to add value annotations
    """
    setup_publication_defaults()

    if value_cols is None:
        value_cols = data.select_dtypes(include=[np.number]).columns.tolist()

    matrix = data[value_cols].values
    row_labels = data[row_col].values if row_col in data.columns else data.index.values
    col_labels = value_cols

    fig, ax = plt.subplots(figsize=(max(4, len(col_labels) * 0.8 + 1),
                                     max(3, len(row_labels) * 0.4 + 1)))

    im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=vmin, vmax=vmax)

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_xticklabels(col_labels, fontsize=8, rotation=45, ha='right')
    ax.set_yticklabels(row_labels, fontsize=9)

    if annotate:
        for i in range(len(row_labels)):
            for j in range(len(col_labels)):
                val = matrix[i, j]
                color = 'white' if abs(val) > (vmax - vmin) * 0.4 else 'black'
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                       color=color, fontsize=8, fontweight='medium')

    cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Value', fontsize=9)
    ax.set_title(title, fontweight='bold', pad=10)

    plt.tight_layout()
    save_figure(fig, output_path, 'heatmap')


def create_grouped_bars(
    data: pd.DataFrame,
    output_path: Path,
    category_col: str = 'category',
    group_col: str = 'group',
    value_col: str = 'value',
    error_col: Optional[str] = None,
    title: str = 'Grouped Bar Chart'
) -> None:
    """
    Create a grouped bar chart with optional error bars.

    Args:
        data: DataFrame in long format with category, group, value columns
        output_path: Directory to save the figure
        category_col: Column name for x-axis categories
        group_col: Column name for grouping variable
        value_col: Column name for bar heights
        error_col: Column name for error bars (optional)
        title: Figure title
    """
    setup_publication_defaults()

    categories = data[category_col].unique()
    groups = data[group_col].unique()
    n_groups = len(groups)

    x = np.arange(len(categories))
    width = 0.8 / n_groups

    fig, ax = plt.subplots(figsize=(max(4, len(categories) * 0.8 + 1), 4))

    for i, group in enumerate(groups):
        group_data = data[data[group_col] == group]
        values = [group_data[group_data[category_col] == cat][value_col].values[0]
                  for cat in categories]

        if error_col and error_col in data.columns:
            errors = [group_data[group_data[category_col] == cat][error_col].values[0]
                      for cat in categories]
        else:
            errors = None

        offset = (i - n_groups/2 + 0.5) * width
        ax.bar(x + offset, values, width, yerr=errors, label=group,
              color=PALETTE_CATEGORICAL[i % len(PALETTE_CATEGORICAL)],
              edgecolor='black', linewidth=0.8, capsize=3)

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=35, ha='right')
    ax.set_ylabel('Value')
    ax.set_title(title, fontweight='bold', pad=10)
    ax.legend(frameon=True, fancybox=False, edgecolor='#cccccc')
    ax.axhline(y=0, color='#888888', linestyle='--', linewidth=0.8, alpha=0.5)

    plt.tight_layout()
    save_figure(fig, output_path, 'grouped_bars')


def create_scatter_plot(
    data: pd.DataFrame,
    output_path: Path,
    x_col: str = 'x',
    y_col: str = 'y',
    color_col: Optional[str] = None,
    title: str = 'Scatter Plot',
    add_regression: bool = True
) -> None:
    """
    Create a scatter plot with optional regression line.

    Args:
        data: DataFrame with x and y columns
        output_path: Directory to save the figure
        x_col: Column name for x values
        y_col: Column name for y values
        color_col: Column name for color grouping (optional)
        title: Figure title
        add_regression: Whether to add regression line
    """
    setup_publication_defaults()

    fig, ax = plt.subplots(figsize=(5, 4.5))

    x = data[x_col].values
    y = data[y_col].values

    if color_col and color_col in data.columns:
        color_values = data[color_col].values
        unique_colors = list(set(color_values))
        for i, v in enumerate(unique_colors):
            mask = color_values == v
            ax.scatter(x[mask], y[mask], alpha=0.7, s=50,
                      color=PALETTE_CATEGORICAL[i % len(PALETTE_CATEGORICAL)],
                      label=v, edgecolor='white', linewidth=0.5)
        ax.legend(frameon=True, fancybox=False, edgecolor='#cccccc')
    else:
        ax.scatter(x, y, alpha=0.7, s=50, color=PALETTE_SCIENTIFIC['blue'],
                  edgecolor='white', linewidth=0.5)

    if add_regression:
        # Add regression line
        mask = ~(np.isnan(x) | np.isnan(y))
        if mask.sum() > 2:
            z = np.polyfit(x[mask], y[mask], 1)
            p = np.poly1d(z)
            x_line = np.linspace(x[mask].min(), x[mask].max(), 100)
            ax.plot(x_line, p(x_line), '--', color='#e74c3c', linewidth=1.5,
                   label=f'y = {z[0]:.2f}x + {z[1]:.2f}')

            # Calculate R-squared
            y_pred = p(x[mask])
            ss_res = np.sum((y[mask] - y_pred) ** 2)
            ss_tot = np.sum((y[mask] - np.mean(y[mask])) ** 2)
            r2 = 1 - ss_res / ss_tot
            ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes,
                   fontsize=9, va='top')

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title, fontweight='bold', pad=10)

    plt.tight_layout()
    save_figure(fig, output_path, 'scatter')


def create_cascade_diagram(
    output_path: Path,
    labels: List[str],
    colors: List[str],
    title: str = 'Cascade Diagram'
) -> None:
    """
    Create a vertical cascade/flow diagram.

    Args:
        output_path: Directory to save the figure
        labels: List of box labels from top to bottom
        colors: List of colors for each box
        title: Figure title
    """
    setup_publication_defaults()

    fig, ax = plt.subplots(figsize=(3.5, max(3, len(labels) * 1.2)))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2 + len(labels) * 1.8)
    ax.axis('off')

    box_width, box_height = 3.2, 1.0
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
            arrow_style = "Simple,tail_width=0.4,head_width=4,head_length=4"
            arrow = FancyArrowPatch(
                (x_center, y - box_height/2 - 0.1),
                (x_center, y - 1.8 + box_height/2 + 0.1),
                arrowstyle=arrow_style, color='#333333', lw=1.5
            )
            ax.add_patch(arrow)

    ax.set_title(title, fontweight='bold', pad=10, y=1.0)

    plt.tight_layout()
    save_figure(fig, output_path, 'cascade')


def create_multipanel_figure(
    config: Dict[str, Any],
    output_path: Path
) -> None:
    """
    Create a custom multi-panel figure from configuration.

    Args:
        config: Dictionary with figure configuration
            - figsize: (width, height) tuple
            - layout: (rows, cols) tuple
            - panels: list of panel configurations
            - title: optional main title
        output_path: Directory to save the figure
    """
    setup_publication_defaults()

    figsize = config.get('figsize', (7.08, 7.5))
    layout = config.get('layout', (2, 2))
    panels = config.get('panels', [])
    title = config.get('title', '')

    fig = plt.figure(figsize=figsize)
    gs = GridSpec(layout[0], layout[1], figure=fig,
                  left=0.10, right=0.95, top=0.92, bottom=0.08,
                  wspace=0.35, hspace=0.35)

    for i, panel_config in enumerate(panels):
        row = i // layout[1]
        col = i % layout[1]
        ax = fig.add_subplot(gs[row, col])

        label = panel_config.get('label', chr(65 + i))  # A, B, C, D...
        add_panel_label(ax, label)

        # Panel content would be added here based on panel_config['type']
        panel_type = panel_config.get('type', 'empty')
        if panel_type == 'empty':
            ax.text(0.5, 0.5, f'Panel {label}', transform=ax.transAxes,
                   ha='center', va='center', fontsize=12, color='#888888')

    if title:
        fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)

    save_figure(fig, output_path, 'multipanel')


def save_figure(fig: plt.Figure, output_path: Path, name: str) -> None:
    """Save figure in PDF and PNG formats."""
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    for fmt in ['pdf', 'png']:
        filepath = output_path / f"{name}.{fmt}"
        fig.savefig(filepath,
                    dpi=600 if fmt == 'png' else None,
                    bbox_inches='tight',
                    facecolor='white')
        print(f"Saved: {filepath}")

    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(
        description='Create publication-quality scientific figures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--type', '-t', required=True,
                       choices=['forest', 'heatmap', 'bars', 'scatter', 'cascade', 'multipanel'],
                       help='Type of figure to create')
    parser.add_argument('--data', '-d',
                       help='Path to data CSV file')
    parser.add_argument('--output', '-o', default='.',
                       help='Output directory (default: current directory)')
    parser.add_argument('--config', '-c',
                       help='Path to JSON config file (for multipanel or cascade)')
    parser.add_argument('--title',
                       help='Figure title')

    args = parser.parse_args()

    output_path = Path(args.output)

    # Load data if provided
    data = None
    if args.data:
        data = pd.read_csv(args.data)

    # Load config if provided
    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)

    # Create figure based on type
    title = args.title or config.get('title', f'{args.type.title()} Plot')

    if args.type == 'forest':
        if data is None:
            print("Error: --data required for forest plot")
            sys.exit(1)
        create_forest_plot(data, output_path, title=title, **config)

    elif args.type == 'heatmap':
        if data is None:
            print("Error: --data required for heatmap")
            sys.exit(1)
        create_heatmap(data, output_path, title=title, **config)

    elif args.type == 'bars':
        if data is None:
            print("Error: --data required for bar chart")
            sys.exit(1)
        create_grouped_bars(data, output_path, title=title, **config)

    elif args.type == 'scatter':
        if data is None:
            print("Error: --data required for scatter plot")
            sys.exit(1)
        create_scatter_plot(data, output_path, title=title, **config)

    elif args.type == 'cascade':
        labels = config.get('labels', ['Step 1', 'Step 2', 'Step 3'])
        colors = config.get('colors', PALETTE_CATEGORICAL[:len(labels)])
        create_cascade_diagram(output_path, labels, colors, title=title)

    elif args.type == 'multipanel':
        if not config:
            print("Error: --config required for multipanel figure")
            sys.exit(1)
        config['title'] = title
        create_multipanel_figure(config, output_path)

    print("\nFigure generation complete!")


if __name__ == "__main__":
    main()
