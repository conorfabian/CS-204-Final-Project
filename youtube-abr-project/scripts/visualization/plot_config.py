"""
Common plotting configuration for all visualizations
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)
sns.set_palette("husl")

# Color scheme
COLORS = {
    'network': '#2E86AB',    # Blue
    'quality': '#A23B72',    # Purple
    'buffer': '#F18F01',     # Orange
    'phase_marker': '#C73E1D', # Red
    'recovery': '#06A77D'    # Green
}

# Figure sizes
FIGURE_SIZE = (14, 8)
FIGURE_SIZE_WIDE = (16, 6)
FIGURE_SIZE_TALL = (12, 10)

# DPI for publication quality
DPI = 300

def save_figure(fig, filename, dpi=DPI):
    """Save figure with consistent settings"""
    fig.tight_layout()
    output_path = f'figures/{filename}'
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")

def format_time_axis(ax):
    """Format x-axis as MM:SS"""
    import matplotlib.ticker as ticker

    def format_func(value, tick_number):
        minutes = int(value // 60)
        seconds = int(value % 60)
        return f'{minutes}:{seconds:02d}'

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    ax.set_xlabel('Time (MM:SS)', fontsize=12)
