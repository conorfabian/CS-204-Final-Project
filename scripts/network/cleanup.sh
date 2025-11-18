#!/bin/bash

echo "Cleaning up network configuration..."
sudo pfctl -d 2>/dev/null
sudo dnctl -q flush
echo "✓ Network restored to normal"