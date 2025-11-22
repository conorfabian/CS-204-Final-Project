#!/bin/bash

# Automated 135s network trace: 20Mbps -> 1.5Mbps -> 20Mbps

read -p "Press Enter to start, then play video immediately"

sudo pfctl -E 2>/dev/null

# Phase 1: HIGH (0-45s)
echo "[$(date +%T)] Phase 1: 20 Mbps"
sudo dnctl -q flush
sudo dnctl pipe 1 config bw 20Mbit/s delay 40ms
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
sleep 45

# Phase 2: LOW (45-90s)
echo "[$(date +%T)] Phase 2: 1.5 Mbps"
sudo dnctl -q flush
sudo dnctl pipe 1 config bw 1500Kbit/s delay 40ms
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
sleep 45

# Phase 3: HIGH (90-135s)
echo "[$(date +%T)] Phase 3: 20 Mbps"
sudo dnctl -q flush
sudo dnctl pipe 1 config bw 20Mbit/s delay 40ms
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
sleep 45

echo "[$(date +%T)] Done. Run cleanup.sh to restore network."
