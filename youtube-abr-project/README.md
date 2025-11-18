# YouTube Adaptive Bitrate Streaming Analysis

**CS204 Final Project | Fall 2025**
**Student:** Conor Fabian (cfabi0@ucr.edu)
**Institution:** University of California, Riverside

## Project Overview

This project analyzes YouTube's adaptive bitrate (ABR) streaming behavior under controlled network conditions. By applying a standardized network trace and collecting detailed playback metrics, we characterize YouTube's quality selection algorithm and adaptation timing.

## Network Trace Specification

All experiments use this standardized network trace:

- **Phase 1 (0-45s):** 20 Mbps bandwidth, 40ms latency
- **Phase 2 (45-90s):** 1.5 Mbps bandwidth, 40ms latency (drop)
- **Phase 3 (90-135s):** 20 Mbps bandwidth, 40ms latency (recovery)

**Total Duration:** 135 seconds

## Repository Structure

```
youtube-abr-project/
├── scripts/          # All automation scripts
│   ├── network/     # Network shaping
│   ├── collection/  # Data collection
│   ├── analysis/    # Data processing
│   └── visualization/ # Plotting
├── data/            # Experimental data
│   ├── raw/        # Raw trial data
│   ├── processed/  # Processed timelines
│   └── templates/  # Data entry templates
├── figures/         # Generated plots
├── report/          # Final report
└── docs/           # Documentation
```

## Quick Start

### Prerequisites

- macOS 10.14 or later (required for pfctl/dnctl)
- Python 3.8+
- Google Chrome
- sudo/admin privileges

### Installation

```bash
# Clone repository
git clone https://github.com/[username]/youtube-abr-project
cd youtube-abr-project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running an Experiment

1. **Launch Chrome:**
   ```bash
   ./scripts/collection/launch_chrome.sh
   ```

2. **Open YouTube video** (your selected test video)

3. **Open chrome://media-internals** in another tab

4. **Start network control:**
   ```bash
   ./scripts/network/manual_control.sh
   ```

5. **Run experiment** (135 seconds):
   - T=0: Start HIGH (20 Mbps), play video
   - T=45: Switch to LOW (1.5 Mbps)
   - T=90: Switch to HIGH (20 Mbps)
   - T=135: Stop video

6. **Export data** from chrome://media-internals

7. **Cleanup:**
   ```bash
   ./scripts/network/cleanup.sh
   ```

## Processing Data

```bash
# Process a trial
python3 scripts/analysis/process_trial.py 003

# Calculate metrics for all trials
python3 scripts/analysis/calculate_metrics.py

# Validate data
python3 scripts/analysis/validate_data.py
```

## Generating Figures

```bash
# Timeline plot for specific trial
python3 scripts/visualization/plot_timeline.py 003

# Comparison plots across all trials
python3 scripts/visualization/plot_comparison.py
```

## Data Collection

Manual data entry is required due to TLS encryption. For each trial:

1. Fill in `data/processed/trial_XXX/quality_timeline.csv`
2. Fill in `data/processed/trial_XXX/buffer_timeline.csv`
3. Write observations in `data/raw/trial_XXX/observations.txt`

Templates are provided in `data/templates/`.

## Results

See `report/final_report.pdf` for complete analysis.

**Key Findings:**
- [To be filled after experiments]

## Reproducibility

All experiments can be reproduced by following the procedures in `docs/data_collection_protocol.md`. The standardized network trace ensures consistent conditions across trials.

## Citation

```bibtex
@techreport{fabian2025youtube,
  author = {Fabian, Conor},
  title = {Understanding Video on Demand Streaming: YouTube ABR Analysis},
  institution = {University of California, Riverside},
  year = {2025},
  type = {CS204 Final Project}
}
```

## License

MIT License

## Acknowledgments

- CS204 instructors and TAs
- Related work by Stockhammer (2011), Akhshabi et al. (2012)

## Contact

Conor Fabian - cfabi0@ucr.edu

Project Link: https://github.com/[username]/youtube-abr-project
