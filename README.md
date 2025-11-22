# YouTube ABR Streaming Analysis

This project looks at how YouTube handles video quality when network conditions change. We throttle bandwidth and see how the player responds.

CS204 Final Project - UCR Fall 2025

## Network Trace

```
Phase 1 (0-45s):   20 Mbps, 40ms latency   (baseline)
Phase 2 (45-90s):  1.5 Mbps, 40ms latency  (bandwidth drop)
Phase 3 (90-135s): 20 Mbps, 40ms latency   (recovery)
```

## Repository Structure

```
├── scripts/
│   ├── analysis/        # Data processing (process_trial.py, calculate_metrics.py)
│   ├── collection/      # Chrome launcher, experiment checklist
│   └── visualization/   # Timeline and comparison plots
├── data/
│   ├── raw/             # 5 trials: quality/buffer CSVs, observations
│   └── processed/       # Unified timelines, metrics_summary.csv
└── figures/             # Generated analysis plots
```

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/youtube-abr-project
cd youtube-abr-project
pip install -r requirements.txt
```

## Reproducing the Experiment

### 1. Data Collection (macOS required)

Network shaping uses `pfctl`/`dnctl`:
```bash
# Enable packet filter
sudo pfctl -e

# Create dummynet pipes
sudo dnctl pipe 1 config bw 20Mbit/s delay 20ms    # HIGH bandwidth
sudo dnctl pipe 2 config bw 1.5Mbit/s delay 20ms   # LOW bandwidth

# Apply to all traffic
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
```

Run experiment:
1. Launch Chrome: `./scripts/collection/launch_chrome.sh`
2. Open YouTube video and `chrome://media-internals`
3. At T=0: Start with HIGH pipe, begin playback
4. At T=45: Switch to LOW pipe
5. At T=90: Switch back to HIGH pipe
6. At T=135: Stop, export media-internals data
7. Cleanup: `sudo pfctl -d && sudo dnctl flush`

### 2. Process Data

```bash
python3 scripts/analysis/process_trial.py 003       # Process single trial
python3 scripts/analysis/calculate_metrics.py       # Generate metrics summary
python3 scripts/analysis/validate_data.py           # Validate all trials
```

### 3. Generate Figures

```bash
python3 scripts/visualization/plot_timeline.py 003  # Single trial timeline
python3 scripts/visualization/plot_comparison.py    # Cross-trial comparison
```

## Results Summary

| Metric | Baseline | Experimental | Change |
|---|---|---|---|
| Avg Bitrate | 4800 kbps | 2300 kbps | -52% |
| Quality Switches | 10-11 | 13-16 | +45% |
| Avg Buffer | 28s | 16s | -43% |

**What we found:**
- theres about a 5-13 second delay before YouTube drops quality after bandwidth goes down
- quality usually drops when buffer gets below 20 seconds or so
- we never got any rebuffering even with the big bandwidth drop which was interesting
- YouTube is pretty conservative about going back up to high quality - didn't get back to 1080p in our recovery window