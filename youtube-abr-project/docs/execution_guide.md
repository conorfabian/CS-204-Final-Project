# End-to-End Execution Guide

This guide walks you through the complete process from running experiments to generating figures. Follow this step-by-step.

---

## Overview

**What you'll do:**
1. Run 5 experiments (2 baseline + 3 experimental)
2. Enter data from observations into CSV files
3. Process data using automated scripts
4. Generate publication-quality figures

**Time required:**
- Experiments: 30-40 minutes (5 trials × ~7 minutes each)
- Data entry: 45-60 minutes (5 trials × ~10 minutes each)
- Processing & figures: 10 minutes (automated)

**Total: ~2 hours**

---

## Before You Start

### Verify Environment

```bash
cd youtube-abr-project
source venv/bin/activate

# Check Python
python3 --version  # Should be 3.8+

# Check dependencies
python3 -c "import pandas; import matplotlib; print('OK')"
```

### Select Your Test Video

Choose a YouTube video that:
- Is 5-10 minutes long
- Has multiple quality levels (360p, 480p, 720p, 1080p)
- Is not copyrighted music (may have restrictions)

**Document your video:**
- URL: _______________
- Video ID: _______________

---

## PHASE A: Run Experiments

### Terminal Setup

Open **3 terminal windows**:
- **Terminal 1:** Network control
- **Terminal 2:** Timer/notes
- **Terminal 3:** Commands

In all terminals:
```bash
cd youtube-abr-project
source venv/bin/activate
```

---

### Trial 001: Baseline (No Network Shaping)

**Purpose:** Understand normal YouTube behavior without interference.

#### Step 1: Setup
```bash
# Terminal 3: Create directory
mkdir -p data/raw/trial_001

# Terminal 3: Launch Chrome
./scripts/collection/launch_chrome.sh
```

#### Step 2: Prepare Browser
1. Open your YouTube video (PAUSE it)
2. Open `chrome://media-internals` in new tab
3. Find your video in the player list

#### Step 3: Run Experiment
1. Start your timer
2. Click play on video
3. Watch chrome://media-internals for 135 seconds
4. Note these observations:
   - Initial quality: ______
   - Time to max quality: ______ seconds
   - Steady-state quality: ______
   - Buffer level at end: ______ seconds

#### Step 4: Export Data
1. In chrome://media-internals, click on your player
2. Copy all the text
3. Save to `data/raw/trial_001/media_internals.txt`

#### Step 5: Record Observations
Copy template and fill in:
```bash
cp data/templates/observations_template.txt data/raw/trial_001/observations.txt
```

---

### Trial 002: Baseline (Repeat)

Repeat Trial 001 exactly. This confirms baseline consistency.

```bash
mkdir -p data/raw/trial_002
```

---

### Trial 003-005: Experimental (With Network Shaping)

**Purpose:** Observe YouTube's adaptation to bandwidth changes.

#### Step 1: Setup
```bash
# Terminal 3: Create directory
mkdir -p data/raw/trial_003

# Terminal 3: Launch Chrome
./scripts/collection/launch_chrome.sh

# Terminal 1: Start network control
./scripts/network/manual_control.sh
```

#### Step 2: Prepare
1. Open YouTube video (PAUSED)
2. Open chrome://media-internals
3. In Terminal 1: Select option 1 (HIGH - 20 Mbps)

#### Step 3: Run 135-Second Experiment

**T=0 (Start):**
- Start timer
- Click play on video
- Note initial quality

**T=0 to T=45 (Phase 1 - HIGH):**
- Watch quality stabilize
- Note buffer building
- Record steady-state quality

**T=45 (Switch to LOW):**
- In Terminal 1: Select option 2 (LOW - 1.5 Mbps)
- Note exact time
- Watch for quality changes

**T=45 to T=90 (Phase 2 - LOW):**
- Record when quality drops
- Note new quality level
- Watch buffer drain
- Record any stalls

**T=90 (Switch to HIGH):**
- In Terminal 1: Select option 1 (HIGH - 20 Mbps)
- Note exact time
- Watch for recovery

**T=90 to T=135 (Phase 3 - Recovery):**
- Record when quality increases
- Note final quality
- Watch buffer rebuild

**T=135 (Stop):**
- Stop video
- In Terminal 1: Select option 4 (Cleanup & exit)

#### Step 4: Export and Document
```bash
# Export media-internals data
# Save to: data/raw/trial_003/media_internals.txt

# Copy observation template
cp data/templates/observations_template.txt data/raw/trial_003/observations.txt

# Fill in your observations immediately while fresh!
```

#### Step 5: Repeat for Trials 004 and 005
```bash
mkdir -p data/raw/trial_004
mkdir -p data/raw/trial_005
```

---

## PHASE B: Data Entry

For each trial, you need to create two CSV files from your observations.

### Understanding chrome://media-internals

The media-internals page shows:
- **kVideoResolution:** Current resolution (e.g., "1920x1080")
- **kBitrate:** Current bitrate in bps (divide by 1000 for kbps)
- **kBufferedRange:** Buffer information

### Creating quality_timeline.csv

```bash
# Create processed directory
mkdir -p data/processed/trial_003

# Copy template
cp data/templates/quality_timeline_template.csv data/processed/trial_003/quality_timeline.csv
```

**Edit the file** with your observations:

```csv
time_seconds,resolution_width,resolution_height,bitrate_kbps,notes
0,1920,1080,4500,initial_startup
5,1920,1080,5000,quality_stabilized
45,1920,1080,5000,before_drop
52,1280,720,2500,first_switch
60,854,480,1200,second_switch
90,854,480,1200,before_recovery
98,1280,720,2500,first_recovery
110,1920,1080,4500,second_recovery
135,1920,1080,5000,end
```

**Tips:**
- Include time points where quality changed
- Use exact times from your observations
- Convert resolution to width/height (1080p = 1920x1080)

### Creating buffer_timeline.csv

```bash
cp data/templates/buffer_timeline_template.csv data/processed/trial_003/buffer_timeline.csv
```

**Edit with your observations:**

```csv
time_seconds,buffer_seconds,notes
0,0,playback_start
10,15,building
30,22,stable
45,25,before_drop
60,12,draining
75,8,low_point
90,6,before_recovery
105,12,rebuilding
120,18,recovering
135,22,end
```

### Repeat for All Trials

Create these files for trials 001-005:
- `data/processed/trial_001/quality_timeline.csv`
- `data/processed/trial_001/buffer_timeline.csv`
- `data/processed/trial_002/quality_timeline.csv`
- ... and so on

---

## PHASE C: Process Data

Now run the automated scripts to process your data.

### Step 1: Process Each Trial

```bash
# Process trial 001
python3 scripts/analysis/process_trial.py 001

# Expected output:
# Processing trial 001...
#   Loaded 7 quality observations
#   Loaded 8 buffer observations
# ✓ Created unified timeline: data/processed/trial_001/unified_timeline.csv
#   136 time points (0-135 seconds)
```

Repeat for all trials:
```bash
python3 scripts/analysis/process_trial.py 002
python3 scripts/analysis/process_trial.py 003
python3 scripts/analysis/process_trial.py 004
python3 scripts/analysis/process_trial.py 005
```

### Step 2: Calculate Metrics

```bash
python3 scripts/analysis/calculate_metrics.py

# Expected output:
# Calculating metrics for 5 trials...
# ✓ Trial 001
# ✓ Trial 002
# ✓ Trial 003
# ✓ Trial 004
# ✓ Trial 005
#
# ✓ Metrics summary saved: data/processed/metrics_summary.csv
#
# Summary Statistics:
# ============================================================
#  trial  avg_bitrate_kbps  quality_switches  avg_buffer_seconds
#    001          4500.00                 2               18.50
#    002          4450.00                 2               19.20
#    003          2850.00                 6               12.30
#    004          2900.00                 5               11.80
#    005          2780.00                 7               12.50
# ============================================================
```

### Step 3: Validate Data

```bash
python3 scripts/analysis/validate_data.py

# Expected output:
# ============================================================
# Data Validation Report
# ============================================================
#
# Trial 001:
#   Rows: 136
#   Expected: 136 (0-135 seconds)
#   ✓ No missing values
#   Bitrate range: 4000 - 5000 kbps
#   Buffer range: 0.0 - 25.0 seconds
#   ✓ Trial 001 validated
# ...
# ============================================================
# Result: 5/5 trials passed validation
# ============================================================
```

---

## PHASE D: Generate Figures

### Step 1: Timeline Plots

Generate a timeline plot for each experimental trial:

```bash
# Baseline
python3 scripts/visualization/plot_timeline.py 001

# Experimental
python3 scripts/visualization/plot_timeline.py 003
python3 scripts/visualization/plot_timeline.py 004
python3 scripts/visualization/plot_timeline.py 005
```

**Output files:**
- `figures/trial_001_timeline.png`
- `figures/trial_003_timeline.png`
- `figures/trial_004_timeline.png`
- `figures/trial_005_timeline.png`

### Step 2: Comparison Plots

```bash
python3 scripts/visualization/plot_comparison.py

# Output:
# Creating comparison plots...
# ✓ Metrics comparison plot created
# ✓ Bitrate overlay plot created
#
# All comparison plots complete!
```

**Output files:**
- `figures/metrics_comparison.png`
- `figures/bitrate_overlay.png`

### Step 3: Verify Figures

Open each figure and verify:
- [ ] Labels are readable
- [ ] Colors are distinguishable
- [ ] Phase markers visible at T=45 and T=90
- [ ] Data looks correct

---

## Troubleshooting

### Problem: "File not found" when processing

**Cause:** CSV files not in correct location
**Solution:** Check file paths:
```bash
ls data/processed/trial_003/
# Should show: quality_timeline.csv, buffer_timeline.csv
```

### Problem: Validation shows missing values

**Cause:** Incomplete data entry
**Solution:** Check your CSV files have all required columns and values

### Problem: Plots look wrong

**Cause:** Data entry errors
**Solution:** Review your CSV files for typos or incorrect values

### Problem: Network shaping not working

**Cause:** pfctl not enabled
**Solution:**
```bash
./scripts/network/cleanup.sh
./scripts/network/manual_control.sh
# Select option 3 to check status
```

---

## Final Checklist

After completing all phases, you should have:

### Raw Data (data/raw/)
- [ ] trial_001/media_internals.txt
- [ ] trial_001/observations.txt
- [ ] trial_002/... (same files)
- [ ] trial_003/...
- [ ] trial_004/...
- [ ] trial_005/...

### Processed Data (data/processed/)
- [ ] trial_001/quality_timeline.csv
- [ ] trial_001/buffer_timeline.csv
- [ ] trial_001/unified_timeline.csv
- [ ] ... (same for trials 002-005)
- [ ] metrics_summary.csv

### Figures (figures/)
- [ ] trial_001_timeline.png
- [ ] trial_003_timeline.png
- [ ] trial_004_timeline.png
- [ ] trial_005_timeline.png
- [ ] metrics_comparison.png
- [ ] bitrate_overlay.png

---

## Next Steps

1. **Review your figures** - Do they tell a clear story?
2. **Write your report** - Use `report/report_template.md`
3. **Push to GitHub** - Follow instructions in README.md
4. **Submit** - Upload report and repository link

**Congratulations!** You've completed the YouTube ABR analysis experiments.
