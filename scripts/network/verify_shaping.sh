#!/bin/bash

echo "Network Shaping Verification"
echo "=============================="
echo ""

echo "Packet Filter Status:"
sudo pfctl -s info
echo ""

echo "Dummynet Pipes:"
sudo dnctl pipe list
echo ""

echo "Active Rules:"
sudo pfctl -s rules | grep dummynet
echo ""

echo "To test bandwidth:"
echo "  Visit speedtest.net or fast.com"
echo ""