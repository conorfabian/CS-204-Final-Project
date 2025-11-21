#!/usr/bin/env python3
"""
Process a single trial's data
Combines quality and buffer timelines into unified timeline
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

def process_trial(trial_num):
    """
    Process trial data into unified timeline

    Args:
        trial_num: Trial number (e.g., '001', '003')
    """
    print(f"Processing trial {trial_num}...")

    # Read from raw directory, write to processed directory
    raw_dir = Path(f'data/raw/trial_{trial_num}')
    proc_dir = Path(f'data/processed/trial_{trial_num}')
    proc_dir.mkdir(parents=True, exist_ok=True)

    # Check for required files in raw directory
    quality_file = raw_dir / 'quality_timeline.csv'
    buffer_file = raw_dir / 'buffer_timeline.csv'

    if not quality_file.exists():
        print(f"ERROR: {quality_file} not found!")
        print("Please create quality_timeline.csv from your observations")
        return False

    if not buffer_file.exists():
        print(f"ERROR: {buffer_file} not found!")
        print("Please create buffer_timeline.csv from your observations")
        return False

    # Load data
    quality = pd.read_csv(quality_file)
    buffer = pd.read_csv(buffer_file)

    print(f"  Loaded {len(quality)} quality observations")
    print(f"  Loaded {len(buffer)} buffer observations")

    # Create unified timeline (0-135 seconds)
    timeline = pd.DataFrame({'time_seconds': range(0, 136)})

    # Merge quality data (forward fill)
    timeline = timeline.merge(
        quality[['time_seconds', 'resolution_width', 'resolution_height', 'bitrate_kbps']],
        on='time_seconds',
        how='left'
    )
    timeline[['resolution_width', 'resolution_height', 'bitrate_kbps']] = \
        timeline[['resolution_width', 'resolution_height', 'bitrate_kbps']].ffill()

    # Merge buffer data (interpolate)
    timeline = timeline.merge(
        buffer[['time_seconds', 'buffer_seconds']],
        on='time_seconds',
        how='left'
    )
    timeline['buffer_seconds'] = timeline['buffer_seconds'].interpolate()

    # Add network phase information
    timeline['network_phase'] = 'unknown'
    timeline.loc[timeline['time_seconds'] < 45, 'network_phase'] = 'phase1_high'
    timeline.loc[(timeline['time_seconds'] >= 45) & (timeline['time_seconds'] < 90), 'network_phase'] = 'phase2_low'
    timeline.loc[timeline['time_seconds'] >= 90, 'network_phase'] = 'phase3_high'

    timeline['network_bandwidth_mbps'] = 20.0
    timeline.loc[(timeline['time_seconds'] >= 45) & (timeline['time_seconds'] < 90), 'network_bandwidth_mbps'] = 1.5

    # Save unified timeline
    output_file = proc_dir / 'unified_timeline.csv'
    timeline.to_csv(output_file, index=False)

    print(f"✓ Created unified timeline: {output_file}")
    print(f"  {len(timeline)} time points (0-135 seconds)")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_trial.py TRIAL_NUM")
        print("Example: python process_trial.py 003")
        sys.exit(1)

    trial_num = sys.argv[1]
    success = process_trial(trial_num)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
