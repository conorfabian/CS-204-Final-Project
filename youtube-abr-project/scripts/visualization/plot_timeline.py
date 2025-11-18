#!/usr/bin/env python3
"""
Create timeline plots showing bitrate, buffer, and resolution over time
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from plot_config import *

def plot_trial_timeline(trial_num):
    """Create comprehensive timeline plot for one trial"""

    unified_file = Path(f'data/processed/trial_{trial_num}/unified_timeline.csv')

    if not unified_file.exists():
        print(f"ERROR: {unified_file} not found")
        return False

    df = pd.read_csv(unified_file)

    # Create figure with 2 subplots
    fig, axes = plt.subplots(2, 1, figsize=FIGURE_SIZE, sharex=True)

    # Plot 1: Bitrate
    ax1 = axes[0]
    ax1.plot(df['time_seconds'], df['bitrate_kbps'] / 1000,
            linewidth=2.5, color=COLORS['quality'], label='Video Bitrate')

    # Add phase markers
    ax1.axvline(x=45, color=COLORS['phase_marker'], linestyle='--',
               alpha=0.6, linewidth=2, label='Bandwidth Drop')
    ax1.axvline(x=90, color=COLORS['recovery'], linestyle='--',
               alpha=0.6, linewidth=2, label='Recovery')

    # Add phase labels
    ax1.text(22, ax1.get_ylim()[1]*0.95, '20 Mbps', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax1.text(67, ax1.get_ylim()[1]*0.95, '1.5 Mbps', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    ax1.text(112, ax1.get_ylim()[1]*0.95, '20 Mbps', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    ax1.set_ylabel('Bitrate (Mbps)', fontsize=12)
    ax1.set_title(f'Trial {trial_num}: Video Quality and Buffer Over Time',
                 fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Buffer
    ax2 = axes[1]
    ax2.plot(df['time_seconds'], df['buffer_seconds'],
            linewidth=2.5, color=COLORS['buffer'], label='Buffer Level')
    ax2.axhline(y=0, color=COLORS['phase_marker'], linestyle=':',
               linewidth=1.5, alpha=0.7, label='Empty Buffer')

    # Add phase markers
    ax2.axvline(x=45, color=COLORS['phase_marker'], linestyle='--',
               alpha=0.6, linewidth=2)
    ax2.axvline(x=90, color=COLORS['recovery'], linestyle='--',
               alpha=0.6, linewidth=2)

    ax2.set_ylabel('Buffer (seconds)', fontsize=12)
    ax2.set_xlabel('Time (seconds)', fontsize=12)
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)

    # Format x-axis
    format_time_axis(ax2)

    save_figure(fig, f'trial_{trial_num}_timeline.png')
    plt.close()

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_timeline.py TRIAL_NUM")
        print("Example: python plot_timeline.py 003")
        sys.exit(1)

    trial_num = sys.argv[1]

    # Create figures directory if needed
    Path('figures').mkdir(exist_ok=True)

    success = plot_trial_timeline(trial_num)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
