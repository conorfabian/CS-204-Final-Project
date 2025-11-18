#!/bin/bash

# YouTube ABR Project - Manual Network Control
# CS204 Fall 2025 - Standardized Network Trace
# Conor Fabian

echo "=========================================="
echo "YouTube ABR Network Controller"
echo "=========================================="
echo "Standardized Trace:"
echo "  Phase 1 (0-45s):   20 Mbps, 40ms"
echo "  Phase 2 (45-90s):  1.5 Mbps, 40ms"
echo "  Phase 3 (90-135s): 20 Mbps, 40ms"
echo "=========================================="
echo ""

apply_high() {
    echo "[$(date +%T)] Applying HIGH bandwidth..."
    sudo pfctl -E 2>/dev/null
    sudo dnctl -q flush
    sudo dnctl pipe 1 config bw 20Mbit/s delay 40ms
    echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
    echo "✓ HIGH: 20 Mbps, 40ms latency"
    echo ""
}

apply_low() {
    echo "[$(date +%T)] Applying LOW bandwidth..."
    sudo dnctl -q flush
    sudo dnctl pipe 1 config bw 1500Kbit/s delay 40ms
    echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
    echo "✓ LOW: 1.5 Mbps, 40ms latency"
    echo ""
}

show_status() {
    echo "Current Configuration:"
    echo "====================="
    sudo dnctl pipe list
    echo ""
    echo "PF Rules:"
    sudo pfctl -s rules | grep dummynet
    echo ""
}

cleanup() {
    echo "[$(date +%T)] Cleaning up..."
    sudo pfctl -d 2>/dev/null
    sudo dnctl -q flush
    echo "✓ Network restored"
    exit 0
}

while true; do
    echo "========== MENU =========="
    echo "1) HIGH (20 Mbps, 40ms)"
    echo "2) LOW (1.5 Mbps, 40ms)"
    echo "3) Show current status"
    echo "4) Cleanup & exit"
    echo "=========================="
    read -p "Select [1-4]: " choice

    case $choice in
        1) apply_high ;;
        2) apply_low ;;
        3) show_status ;;
        4) cleanup ;;
        *) echo "Invalid option" ;;
    esac
done