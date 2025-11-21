#!/bin/bash

PROFILE_DIR="$HOME/chrome-test-profile"
DEBUG_PORT=9222

echo "Launching Chrome for ABR testing..."
echo "Profile: $PROFILE_DIR"
echo "Debug port: $DEBUG_PORT"
echo ""

# Close existing Chrome
pkill -f "Google Chrome" 2>/dev/null
sleep 2

# Launch with debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --user-data-dir="$PROFILE_DIR" \
    --remote-debugging-port=$DEBUG_PORT \
    --enable-logging \
    &

echo "✓ Chrome launched"
echo ""
echo "Next steps:"
echo "  1. Open your YouTube video"
echo "  2. Open chrome://media-internals in another tab"
echo "  3. Open DevTools (Cmd+Option+I) > Network tab"
echo ""
