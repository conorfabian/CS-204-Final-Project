#!/bin/bash

# Manual network control for ABR testing

apply_high() {
    sudo pfctl -E 2>/dev/null
    sudo dnctl -q flush
    sudo dnctl pipe 1 config bw 20Mbit/s delay 40ms
    echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
    echo "Applied: 20 Mbps, 40ms"
}

apply_low() {
    sudo dnctl -q flush
    sudo dnctl pipe 1 config bw 1500Kbit/s delay 40ms
    echo "dummynet out proto tcp from any to any pipe 1" | sudo pfctl -f -
    echo "Applied: 1.5 Mbps, 40ms"
}

cleanup() {
    sudo pfctl -d 2>/dev/null
    sudo dnctl -q flush
    echo "Network restored"
    exit 0
}

while true; do
    echo ""
    echo "1) HIGH (20 Mbps)  2) LOW (1.5 Mbps)  3) Status  4) Exit"
    read -p "> " choice
    case $choice in
        1) apply_high ;;
        2) apply_low ;;
        3) sudo dnctl pipe list ;;
        4) cleanup ;;
    esac
done
