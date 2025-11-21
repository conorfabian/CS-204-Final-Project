#!/usr/bin/env python3
"""
Create comparison plots across all trials
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from plot_config import *

def plot_metrics_comparison():
    """Compare key metrics across all trials"""

    metrics_file = Path('data/processed/metrics_summary.csv')

    if not metrics_file.exists():
        print("ERROR: metrics_summary.csv not found")
        print("Run calculate_metrics.py first")
        return False

    df = pd.read_csv(metrics_file)

    # Create figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Performance Metrics Comparison Across Trials',
                fontsize=16, fontweight='bold')

    # Plot 1: Average Bitrate
    ax = axes[0, 0]
    if 'avg_bitrate_kbps' in df.columns:
        bars = ax.bar(df['trial'], df['avg_bitrate_kbps'], color=COLORS['quality'])
        ax.set_ylabel('Average Bitrate (kbps)', fontsize=11)
        ax.set_title('Average Video Bitrate', fontsize=12, fontweight='bold')
        ax.set_xlabel('Trial', fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)

    # Plot 2: Quality Switches
    ax = axes[0, 1]
    if 'quality_switches' in df.columns:
        bars = ax.bar(df['trial'], df['quality_switches'], color=COLORS['network'])
        ax.set_ylabel('Number of Switches', fontsize=11)
        ax.set_title('Quality Switches Per Trial', fontsize=12, fontweight='bold')
        ax.set_xlabel('Trial', fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)

    # Plot 3: Buffer Statistics
    ax = axes[1, 0]
    if 'avg_buffer_seconds' in df.columns:
        bars = ax.bar(df['trial'], df['avg_buffer_seconds'], color=COLORS['buffer'])
        ax.set_ylabel('Average Buffer (seconds)', fontsize=11)
        ax.set_title('Average Buffer Level', fontsize=12, fontweight='bold')
        ax.set_xlabel('Trial', fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)

    # Plot 4: Time at Each Quality
    ax = axes[1, 1]
    quality_cols = [col for col in df.columns if 'time_at_' in col and '_percent' in col]

    if quality_cols:
        # Create stacked bar chart
        quality_data = df[['trial'] + quality_cols].set_index('trial')

        # Rename columns for legend
        quality_data.columns = [col.replace('time_at_', '').replace('p_percent', 'p')
                               for col in quality_data.columns]

        quality_data.plot(kind='bar', stacked=True, ax=ax, width=0.7)
        ax.set_ylabel('Percentage of Time (%)', fontsize=11)
        ax.set_title('Time Spent at Each Quality Level', fontsize=12, fontweight='bold')
        ax.set_xlabel('Trial', fontsize=11)
        ax.legend(title='Resolution', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.grid(axis='y', alpha=0.3)

    save_figure(fig, 'metrics_comparison.png')
    plt.close()

    return True

def plot_bitrate_overlay():
    """Overlay bitrate from multiple trials"""

    proc_dir = Path('data/processed')
    trial_dirs = sorted([d for d in proc_dir.iterdir()
                        if d.is_dir() and d.name.startswith('trial_')])

    if len(trial_dirs) < 2:
        print("Need at least 2 trials for overlay plot")
        return False

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

    for trial_dir in trial_dirs:
        trial_num = trial_dir.name.split('_')[1]
        unified_file = trial_dir / 'unified_timeline.csv'

        if not unified_file.exists():
            continue

        df = pd.read_csv(unified_file)

        if 'bitrate_kbps' in df.columns:
            ax.plot(df['time_seconds'], df['bitrate_kbps'] / 1000,
                   label=f'Trial {trial_num}', linewidth=2, alpha=0.7)

    # Add phase markers
    ax.axvline(x=45, color='red', linestyle='--', alpha=0.5, linewidth=2)
    ax.axvline(x=90, color='green', linestyle='--', alpha=0.5, linewidth=2)

    # Add phase labels
    ax.text(22, ax.get_ylim()[1]*0.95, '20 Mbps', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(67, ax.get_ylim()[1]*0.95, '1.5 Mbps', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    ax.text(112, ax.get_ylim()[1]*0.95, '20 Mbps', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Bitrate (Mbps)', fontsize=12)
    ax.set_title('Bitrate Comparison Across All Trials',
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    format_time_axis(ax)

    save_figure(fig, 'bitrate_overlay.png')
    plt.close()

    return True

def main():
    # Create figures directory
    Path('figures').mkdir(exist_ok=True)

    print("Creating comparison plots...")

    success = plot_metrics_comparison()
    if success:
        print("✓ Metrics comparison plot created")

    success = plot_bitrate_overlay()
    if success:
        print("✓ Bitrate overlay plot created")

    print("\nAll comparison plots complete!")

if __name__ == "__main__":
    main()
