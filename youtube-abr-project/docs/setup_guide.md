# Setup Guide

Complete installation and configuration instructions.

## System Requirements

- **OS:** macOS 10.14 or later (pfctl/dnctl required)
- **Python:** 3.8 or higher
- **Browser:** Google Chrome (latest stable)
- **Privileges:** sudo/admin access (for network shaping)
- **Storage:** ~1GB for data and figures

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/[username]/youtube-abr-project
cd youtube-abr-project
```

### 2. Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate (do this every time you work)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Make Scripts Executable

```bash
chmod +x scripts/network/*.sh
chmod +x scripts/collection/*.sh
chmod +x scripts/analysis/*.py
chmod +x scripts/visualization/*.py
```

### 4. Create Chrome Profile

```bash
mkdir -p ~/chrome-test-profile
```

### 5. Verify Network Shaping

```bash
# Test basic shaping
sudo pfctl -E
sudo dnctl pipe 1 config bw 10Mbit/s
sudo dnctl pipe list

# Should show pipe configuration

# Cleanup
sudo pfctl -d
sudo dnctl -q flush
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Scripts are executable
- [ ] Can run `sudo` commands
- [ ] Chrome installed
- [ ] Network shaping tested

## Troubleshooting

**Python not found:**
```bash
which python3
# Install from python.org if needed
```

**Permission denied on scripts:**
```bash
chmod +x scripts/**/*.sh
chmod +x scripts/**/*.py
```

**Network shaping fails:**
```bash
# Check if pfctl exists
which pfctl

# Should be at /sbin/pfctl (standard on macOS)
```

## Next Steps

See `docs/data_collection_protocol.md` for experiment procedure.
