#!/usr/bin/env python3
"""
Calculate summary metrics for all trials
"""

import pandas as pd
import numpy as np
from pathlib import Path

def calculate_trial_metrics(trial_num):
    """Calculate summary metrics for one trial"""

    unified_file = Path(f'data/processed/trial_{trial_num}/unified_timeline.csv')

    if not unified_file.exists():
        print(f"WARNING: {unified_file} not found, skipping")
        return None

    df = pd.read_csv(unified_file)

    metrics = {
        'trial': trial_num,
        'duration_seconds': len(df),
    }

    # Quality metrics
    if 'bitrate_kbps' in df.columns:
        metrics['avg_bitrate_kbps'] = df['bitrate_kbps'].mean()
        metrics['max_bitrate_kbps'] = df['bitrate_kbps'].max()
        metrics['min_bitrate_kbps'] = df['bitrate_kbps'].min()
        metrics['stddev_bitrate_kbps'] = df['bitrate_kbps'].std()

        # Count quality switches
        switches = (df['bitrate_kbps'] != df['bitrate_kbps'].shift()).sum() - 1
        metrics['quality_switches'] = switches

    # Buffer metrics
    if 'buffer_seconds' in df.columns:
        metrics['avg_buffer_seconds'] = df['buffer_seconds'].mean()
        metrics['min_buffer_seconds'] = df['buffer_seconds'].min()
        metrics['max_buffer_seconds'] = df['buffer_seconds'].max()

        # Buffer empty events
        buffer_empty = (df['buffer_seconds'] <= 0).sum()
        metrics['buffer_empty_count'] = buffer_empty

    # Time at each quality level
    if 'resolution_height' in df.columns:
        for height in [360, 480, 720, 1080]:
            time_pct = (df['resolution_height'] == height).sum() / len(df) * 100
            metrics[f'time_at_{height}p_percent'] = round(time_pct, 2)

    # Phase-specific metrics
    phases = {
        'phase1': (0, 45),
        'phase2': (45, 90),
        'phase3': (90, 136)
    }

    for phase_name, (start, end) in phases.items():
        phase_df = df[(df['time_seconds'] >= start) & (df['time_seconds'] < end)]

        if 'bitrate_kbps' in phase_df.columns:
            metrics[f'{phase_name}_avg_bitrate'] = phase_df['bitrate_kbps'].mean()

        if 'buffer_seconds' in phase_df.columns:
            metrics[f'{phase_name}_avg_buffer'] = phase_df['buffer_seconds'].mean()

    return metrics

def calculate_all_trials():
    """Calculate metrics for all processed trials"""

    proc_dir = Path('data/processed')
    if not proc_dir.exists():
        print("ERROR: data/processed directory not found")
        return

    trial_dirs = sorted([d for d in proc_dir.iterdir()
                        if d.is_dir() and d.name.startswith('trial_')])

    if not trial_dirs:
        print("ERROR: No processed trials found")
        print("Run process_trial.py first")
        return

    print(f"Calculating metrics for {len(trial_dirs)} trials...")

    all_metrics = []

    for trial_dir in trial_dirs:
        trial_num = trial_dir.name.split('_')[1]
        metrics = calculate_trial_metrics(trial_num)

        if metrics:
            all_metrics.append(metrics)
            print(f"✓ Trial {trial_num}")

    if not all_metrics:
        print("ERROR: No metrics calculated")
        return

    # Create summary dataframe
    summary = pd.DataFrame(all_metrics)

    # Save summary
    output_file = proc_dir / 'metrics_summary.csv'
    summary.to_csv(output_file, index=False)

    print(f"\n✓ Metrics summary saved: {output_file}")
    print(f"\nSummary Statistics:")
    print("=" * 60)
    print(summary[['trial', 'avg_bitrate_kbps', 'quality_switches',
                   'avg_buffer_seconds']].to_string(index=False))
    print("=" * 60)

    return summary

if __name__ == "__main__":
    calculate_all_trials()
