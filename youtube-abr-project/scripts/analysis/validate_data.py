#!/usr/bin/env python3
"""
Validate processed data quality
"""

import pandas as pd
from pathlib import Path

def validate_trial(trial_num):
    """Validate data for one trial"""

    proc_dir = Path(f'data/processed/trial_{trial_num}')

    if not proc_dir.exists():
        print(f"❌ Trial {trial_num}: Directory not found")
        return False

    unified_file = proc_dir / 'unified_timeline.csv'

    if not unified_file.exists():
        print(f"❌ Trial {trial_num}: unified_timeline.csv not found")
        return False

    df = pd.read_csv(unified_file)

    print(f"\nTrial {trial_num}:")
    print(f"  Rows: {len(df)}")
    print(f"  Expected: 136 (0-135 seconds)")

    if len(df) != 136:
        print(f"  ⚠️  WARNING: Expected 136 rows, got {len(df)}")

    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"  ⚠️  Missing values detected:")
        for col, count in missing[missing > 0].items():
            print(f"      {col}: {count}")
    else:
        print(f"  ✓ No missing values")

    # Check bitrate range
    if 'bitrate_kbps' in df.columns:
        min_br = df['bitrate_kbps'].min()
        max_br = df['bitrate_kbps'].max()
        print(f"  Bitrate range: {min_br:.0f} - {max_br:.0f} kbps")

        if max_br > 50000:
            print(f"  ⚠️  Very high bitrate detected")
        if min_br < 0:
            print(f"  ❌ Negative bitrate detected!")
            return False

    # Check buffer
    if 'buffer_seconds' in df.columns:
        min_buf = df['buffer_seconds'].min()
        max_buf = df['buffer_seconds'].max()
        print(f"  Buffer range: {min_buf:.1f} - {max_buf:.1f} seconds")

        if min_buf < -1:
            print(f"  ⚠️  Significantly negative buffer")

    print(f"  ✓ Trial {trial_num} validated")
    return True

def validate_all():
    """Validate all trials"""

    proc_dir = Path('data/processed')
    trial_dirs = sorted([d for d in proc_dir.iterdir()
                        if d.is_dir() and d.name.startswith('trial_')])

    print("=" * 60)
    print("Data Validation Report")
    print("=" * 60)

    valid_count = 0
    for trial_dir in trial_dirs:
        trial_num = trial_dir.name.split('_')[1]
        if validate_trial(trial_num):
            valid_count += 1

    print(f"\n" + "=" * 60)
    print(f"Result: {valid_count}/{len(trial_dirs)} trials passed validation")
    print("=" * 60)

if __name__ == "__main__":
    validate_all()
