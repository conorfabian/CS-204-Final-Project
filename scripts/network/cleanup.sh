#!/bin/bash
sudo pfctl -d 2>/dev/null
sudo dnctl -q flush
echo "Network restored"
