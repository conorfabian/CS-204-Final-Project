#!/bin/bash

echo "=========================================="
echo "AUTOMATED Network Trace"
echo "=========================================="
echo "Will automatically switch at:"
echo "  0s:   HIGH (20 Mbps)"
echo "  45s:  LOW (1.5 Mbps)"
echo "  90s:  HIGH (20 Mbps)"
echo "  135s: Complete"
echo "=========================================="
echo ""
read -p "Press Enter to start. Then immediately play video!"

LOG="network_trace_$(date +%Y%m%d_%H%M%S).log"

log() {
    echo "[$(date +%T)] $1" | tee -a "$LOG"
}

# Phase 1: HIGH
log "Phase 1: HIGH (20 Mbps)"
sudo pfctl -E 2>/dev/null
sudo dnctl -q flush
sudo dnctl pipe 1 config bw 20Mbit/s delay 40ms
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
log "✓ HIGH applied - START VIDEO NOW!"
echo "Waiting 45 seconds..."
sleep 45

# Phase 2: LOW
log "Phase 2: LOW (1.5 Mbps)"
sudo dnctl -q flush
sudo dnctl pipe 1 config bw 1500Kbit/s delay 40ms
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
log "✓ LOW applied"
echo "Waiting 45 seconds..."
sleep 45

# Phase 3: HIGH
log "Phase 3: HIGH (20 Mbps) - Recovery"
sudo dnctl -q flush
sudo dnctl pipe 1 config bw 20Mbit/s delay 40ms
echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
log "✓ HIGH applied"
echo "Waiting 45 seconds..."
sleep 45

log "COMPLETE! Stop video now."
echo ""
echo "Network still shaped. Run cleanup.sh to restore."
echo "Log: $LOG"