#!/bin/bash
echo "PF status:"
sudo pfctl -s info | grep Status
echo ""
echo "Pipes:"
sudo dnctl pipe list
echo ""
echo "Rules:"
sudo pfctl -s rules | grep dummynet
