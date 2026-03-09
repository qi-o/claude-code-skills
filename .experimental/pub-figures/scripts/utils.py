#!/usr/bin/env python3
"""
Utility Functions for Publication-Quality Figures
==================================================
Common functions and constants for creating journal-ready figures.
"""

from typing import Tuple, Optional, Dict, List
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
import numpy as np


# =============================================================================
# COLOR PALETTES
# =============================================================================

# Primary scientific palette (color-blind friendly)
PALETTE_SCIENTIFIC = {
    'blue': '#2E86AB',
    'magenta': '#A23B72',
    'orange': '#F18F01',
    'red': '#C73E1D',
    'gray': '#95A5A6',
    'green': '#27ae60',
    'purple': '#9b59b6',
    'teal': '#16a085'
}

# Categorical palette (5 colors, distinguishable)
PALETTE_CATEGORICAL = [
    '#95a5a6',  # Gray
    '#3498db',  # Blue
    '#9b59b6',  # Purple
    '#f39c12',  # Orange
    '#e74c3c'   # Red
]

# Extended categorical palette (8 colors)
PALETTE_CATEGORICAL_EXT = [
    '#95a5a6',  # Gray
    '#3498db',  # Blue
    '#9b59b6',  # Purple
    '#f39c12',  # Orange
    '#e74c3c',  # Red
    '#1abc9c',  # Teal
    '#34495e',  # Dark gray
    '#27ae60'   # Green
]

# Species colors
SPECIES_COLORS = {
    'mouse': '#2E86AB',
    'human': '#A23B72',
    'rat': '#F18F01',
    'zebrafish': '#27ae60'
}

# Condition colors
CONDITION_COLORS = {
    'control': '#3498db',
    'disease': '#e74c3c',
    'treatment': '#27ae60',
    'vehicle': '#95a5a6'
}

# Binary colormaps
CMAP_BINARY_GREEN_RED = ListedColormap(['#e74c3c', '#27ae60'])
CMAP_BINARY_BLUE_RED = ListedColormap(['#3498db', '#e74c3c'])


# =============================================================================
# PUBLICATION DEFAULTS
# =============================================================================

def setup_publication_defaults() -> None:
    """
    Apply publication-quality matplotlib defaults.
    Call this at the start of any figure generation.
    """
    plt.rcParams.update({
        # Font settings
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica', 'Liberation Sans'],
        'font.size': 10,

        # Axes settings
        'axes.titlesize': 11,
        'axes.labelsize': 10,
        'axes.linewidth': 1.0,
        'axes.spines.top': False,
        'axes.spines.right': False,

        # Tick settings
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'xtick.major.width': 1.0,
        'ytick.major.width': 1.0,

        # Legend settings
        'legend.fontsize': 9,
        'legend.frameon': True,
        'legend.fancybox': False,
        'legend.edgecolor': '#cccccc',

        # Figure settings
        'figure.dpi': 300,
        'figure.facecolor': 'white',

        # Save settings
        'savefig.dpi': 600,
        'savefig.facecolor': 'white',
        'savefig.bbox': 'tight',

        # Math text
        'mathtext.default': 'regular',
    })


def reset_defaults() -> None:
    """Reset matplotlib to default settings."""
    plt.rcdefaults()


# =============================================================================
# JOURNAL FIGURE SIZES
# =============================================================================

# Journal column widths in inches
JOURNAL_WIDTHS = {
    'single': 3.35,      # 85 mm - single column
    'one_half': 5.51,    # 140 mm - 1.5 columns
    'double': 7.08,      # 180 mm - double column (full width)
}


def get_journal_figsize(
    width: str = 'double',
    aspect: float = 1.0,
    height: Optional[float] = None
) -> Tuple[float, float]:
    """
    Get figure size for journal specifications.

    Args:
        width: 'single', 'one_half', or 'double'
        aspect: height/width ratio (default 1.0 = square)
        height: explicit height in inches (overrides aspect)

    Returns:
        (width, height) tuple in inches
    """
    w = JOURNAL_WIDTHS.get(width, JOURNAL_WIDTHS['double'])
    h = height if height is not None else w * aspect
    return (w, h)


# =============================================================================
# PANEL LABELS
# =============================================================================

def add_panel_label(
    ax: plt.Axes,
    label: str,
    fontsize: int = 14,
    fontweight: str = 'bold',
    x: float = -0.12,
    y: float = 1.08
) -> None:
    """
    Add panel label (A, B, C, D) consistently positioned.

    Args:
        ax: Matplotlib axes object
        label: Label text (typically 'A', 'B', 'C', etc.)
        fontsize: Font size for label
        fontweight: Font weight ('bold' or 'normal')
        x: X position in axes coordinates
        y: Y position in axes coordinates
    """
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=fontsize, fontweight=fontweight,
            va='top', ha='left')


def add_panel_labels(
    axes: List[plt.Axes],
    labels: Optional[List[str]] = None,
    **kwargs
) -> None:
    """
    Add panel labels to multiple axes.

    Args:
        axes: List of axes objects
        labels: List of labels (default: A, B, C, ...)
        **kwargs: Additional arguments passed to add_panel_label
    """
    if labels is None:
        labels = [chr(65 + i) for i in range(len(axes))]

    for ax, label in zip(axes, labels):
        add_panel_label(ax, label, **kwargs)


# =============================================================================
# LEGEND UTILITIES
# =============================================================================

def create_color_legend(
    colors: Dict[str, str],
    marker: str = 'o',
    markersize: int = 8
) -> List[Line2D]:
    """
    Create legend handles for color-coded categories.

    Args:
        colors: Dictionary mapping labels to colors
        marker: Marker style
        markersize: Size of markers

    Returns:
        List of Line2D objects for use with ax.legend()
    """
    return [
        Line2D([0], [0], marker=marker, color='w',
               markerfacecolor=color, markersize=markersize, label=label)
        for label, color in colors.items()
    ]


def create_patch_legend(
    colors: Dict[str, str]
) -> List[mpatches.Patch]:
    """
    Create legend handles using patches.

    Args:
        colors: Dictionary mapping labels to colors

    Returns:
        List of Patch objects for use with ax.legend()
    """
    return [
        mpatches.Patch(facecolor=color, label=label, edgecolor='black', linewidth=0.5)
        for label, color in colors.items()
    ]


# =============================================================================
# AXIS UTILITIES
# =============================================================================

def remove_top_right_spines(ax: plt.Axes) -> None:
    """Remove top and right spines from axes."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def add_zero_line(
    ax: plt.Axes,
    orientation: str = 'horizontal',
    **kwargs
) -> None:
    """
    Add a reference line at zero.

    Args:
        ax: Matplotlib axes object
        orientation: 'horizontal' or 'vertical'
        **kwargs: Additional arguments for axhline/axvline
    """
    defaults = {'color': '#888888', 'linestyle': '--', 'linewidth': 1, 'alpha': 0.7}
    defaults.update(kwargs)

    if orientation == 'horizontal':
        ax.axhline(y=0, **defaults)
    else:
        ax.axvline(x=0, **defaults)


def format_axis_labels(
    ax: plt.Axes,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    title: Optional[str] = None,
    title_weight: str = 'bold',
    title_pad: int = 10
) -> None:
    """
    Format axis labels and title consistently.

    Args:
        ax: Matplotlib axes object
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Axes title
        title_weight: Font weight for title
        title_pad: Padding for title
    """
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title, fontweight=title_weight, pad=title_pad)


# =============================================================================
# STATISTICAL ANNOTATIONS
# =============================================================================

def add_significance_bar(
    ax: plt.Axes,
    x1: float,
    x2: float,
    y: float,
    p_value: float,
    height: float = 0.02,
    color: str = 'black'
) -> None:
    """
    Add significance bar with asterisks between two points.

    Args:
        ax: Matplotlib axes object
        x1, x2: X positions for bar endpoints
        y: Y position for bar
        p_value: P-value for determining asterisks
        height: Height of bar caps
        color: Line color
    """
    # Determine significance symbol
    if p_value < 0.001:
        sig = '***'
    elif p_value < 0.01:
        sig = '**'
    elif p_value < 0.05:
        sig = '*'
    else:
        sig = 'ns'

    # Draw bar
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y],
            lw=1.0, color=color)

    # Add text
    ax.text((x1 + x2) / 2, y + height, sig,
            ha='center', va='bottom', fontsize=10, color=color)


def format_p_value(p: float) -> str:
    """
    Format p-value for display.

    Args:
        p: P-value

    Returns:
        Formatted string
    """
    if p < 0.001:
        return 'p < 0.001'
    elif p < 0.01:
        return f'p = {p:.3f}'
    elif p < 0.05:
        return f'p = {p:.2f}'
    else:
        return f'p = {p:.2f}'


# =============================================================================
# DATA VISUALIZATION HELPERS
# =============================================================================

def calculate_bar_positions(
    n_categories: int,
    n_groups: int,
    total_width: float = 0.8
) -> Tuple[np.ndarray, float]:
    """
    Calculate bar positions for grouped bar charts.

    Args:
        n_categories: Number of categories on x-axis
        n_groups: Number of groups per category
        total_width: Total width allocated for bars per category

    Returns:
        (x_positions, bar_width) tuple
    """
    x = np.arange(n_categories)
    width = total_width / n_groups
    return x, width


def get_bar_offset(group_index: int, n_groups: int, width: float) -> float:
    """
    Get offset for a specific group in grouped bar chart.

    Args:
        group_index: Index of current group (0-based)
        n_groups: Total number of groups
        width: Width of each bar

    Returns:
        Offset to apply to x position
    """
    return (group_index - n_groups / 2 + 0.5) * width


# =============================================================================
# COLOR UTILITIES
# =============================================================================

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def lighten_color(hex_color: str, factor: float = 0.3) -> str:
    """
    Lighten a color by mixing with white.

    Args:
        hex_color: Hex color string
        factor: Lightening factor (0-1)

    Returns:
        Lightened hex color
    """
    rgb = hex_to_rgb(hex_color)
    lightened = tuple(int(c + (255 - c) * factor) for c in rgb)
    return rgb_to_hex(lightened)


def darken_color(hex_color: str, factor: float = 0.3) -> str:
    """
    Darken a color by mixing with black.

    Args:
        hex_color: Hex color string
        factor: Darkening factor (0-1)

    Returns:
        Darkened hex color
    """
    rgb = hex_to_rgb(hex_color)
    darkened = tuple(int(c * (1 - factor)) for c in rgb)
    return rgb_to_hex(darkened)
