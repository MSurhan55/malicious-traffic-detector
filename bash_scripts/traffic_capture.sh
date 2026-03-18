#!/bin/bash

# ─────────────────────────────────────────
# Malicious Traffic Detector
# Script 1: Traffic Capture
# ─────────────────────────────────────────

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log file location
LOG_FILE=~/malicious-traffic-detector/logs/traffic.log

echo -e "${GREEN}[+] Starting Traffic Capture...${NC}"
echo -e "${YELLOW}[*] Logging to: $LOG_FILE${NC}"

# Create log file if not exists
touch $LOG_FILE

# Detect network interface automatically
INTERFACE=$(ip route | grep default | awk '{print $5}')
echo -e "${GREEN}[+] Detected Interface: $INTERFACE${NC}"

# Start capturing traffic and log it
sudo tcpdump -i $INTERFACE -n -l 2>/dev/null | while read line; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $line" >> $LOG_FILE
    echo -e "${GREEN}[CAPTURED]${NC} $line"
done

