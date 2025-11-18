# Data Collection Protocol

Complete procedure for running one experimental trial.

## Pre-Experiment Setup (5 minutes)

### 1. System Preparation
- [ ] Computer plugged in or fully charged
- [ ] Do Not Disturb mode enabled
- [ ] All unnecessary applications closed
- [ ] Background downloads/updates paused

### 2. Browser Setup
- [ ] Clear Chrome cache
- [ ] Launch Chrome: `./scripts/collection/launch_chrome.sh`
- [ ] Open your selected YouTube video (PAUSED)
- [ ] Open `chrome://media-internals` in separate tab
- [ ] Open DevTools (Cmd+Option+I) > Network tab

### 3. Network Setup
- [ ] Start network control: `./scripts/network/manual_control.sh`
- [ ] Select option 1 (HIGH - 20 Mbps)
- [ ] Verify with `./scripts/network/verify_shaping.sh`

### 4. Data Collection Setup
- [ ] Create trial directory: `mkdir -p data/raw/trial_XXX`
- [ ] Open text editor for observations
- [ ] Have stopwatch/timer ready

## Experiment Execution (135 seconds)

### T=0: Start
1. Click play on YouTube video
2. Start stopwatch
3. Note exact time in observations

### T=0-45: Phase 1 (HIGH Bandwidth)
- Monitor chrome://media-internals continuously
- Note initial quality selected
- Watch buffer level build up
- Record any interesting behavior

### T=45: Bandwidth Drop
1. Switch to LOW bandwidth (option 2 in control script)
2. Note exact time in observations
3. Watch carefully for quality changes

### T=45-90: Phase 2 (LOW Bandwidth)
- Watch for quality switches (note times)
- Monitor buffer level (is it draining?)
- Note final quality in this phase
- Record any stalls

### T=90: Recovery
1. Switch back to HIGH bandwidth (option 1)
2. Note exact time in observations
3. Watch for quality increases

### T=90-135: Phase 3 (Recovery)
- Watch how quality recovers
- Does it return to original quality?
- Monitor buffer recovery
- Note final quality at end

### T=135: Stop
1. Stop video playback
2. Stop stopwatch
3. Stop network control (option 4)

## Post-Experiment (Immediately After)

### 1. Export Data
- [ ] chrome://media-internals: Copy all player data
- [ ] Save as `data/raw/trial_XXX/media_internals.txt`
- [ ] DevTools: Right-click > "Save all as HAR"
- [ ] Save as `data/raw/trial_XXX/network_log.har`

### 2. Screenshots
- [ ] Take screenshots of any interesting views
- [ ] Save to `data/raw/trial_XXX/screenshots/`

### 3. Write Observations
- [ ] Complete `observations.txt` (use template)
- [ ] Complete `summary.txt`
- [ ] Complete `metadata.txt`

### 4. Cleanup
```bash
./scripts/network/cleanup.sh
```

### 5. Backup
```bash
tar -czf data/raw/trial_XXX_backup.tar.gz data/raw/trial_XXX
```

## Data Entry

After experiment, create processed data:

1. Copy templates:
```bash
mkdir -p data/processed/trial_XXX
cp data/templates/quality_timeline_template.csv data/processed/trial_XXX/quality_timeline.csv
cp data/templates/buffer_timeline_template.csv data/processed/trial_XXX/buffer_timeline.csv
```

2. Fill in actual observed values from your notes

3. Process the trial:
```bash
python3 scripts/analysis/process_trial.py XXX
```

## Quality Checklist

Before moving to next trial:
- [ ] All data files saved
- [ ] Observations documented
- [ ] Network cleaned up
- [ ] Data backed up
- [ ] Ready for next trial

## Common Issues

**Video won't play:**
- Check internet connection
- Try different video
- Clear browser cache

**Can't export media-internals:**
- Copy visible data manually
- Take screenshots as backup

**Network shaping not working:**
- Verify with speedtest
- Check pfctl status
- Force reload with cleanup then reapply

## Tips for Success

- Take detailed notes during playback
- Use a visible timer
- Be ready to switch network at exactly 45s and 90s
- Don't rush - accuracy is more important than speed
- If something goes wrong, start over

## Trial Schedule

Recommended:
- Trial 001-002: Baseline (no network shaping)
- Trial 003-005: Full experimental trace
- Optional: Additional trials for validation
