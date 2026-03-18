#!/bin/bash

# ─────────────────────────────────────────
# Malicious Traffic Detector
# Script 2: Blacklist Checker
# ─────────────────────────────────────────

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# File paths
LOG_FILE=~/malicious-traffic-detector/logs/traffic.log
BLACKLIST=~/malicious-traffic-detector/data/blacklist.txt
ALERT_LOG=~/malicious-traffic-detector/logs/alerts.log

echo -e "${GREEN}[+] Starting Blacklist Checker...${NC}"

# Download fresh blacklist if not exists
if [ ! -f "$BLACKLIST" ]; then
    echo -e "${YELLOW}[*] Downloading malicious IP blacklist...${NC}"
    curl -s https://rules.emergingthreats.net/blockrules/compromised-ips.txt -o $BLACKLIST
    echo -e "${GREEN}[+] Blacklist downloaded!${NC}"
else
    echo -e "${GREEN}[+] Blacklist already exists${NC}"
fi

echo -e "${YELLOW}[*] Checking traffic log against blacklist...${NC}"

# Extract IPs from traffic log
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' $LOG_FILE | sort -u | while read ip; do

    # Skip private/local IPs
    if [[ $ip == 192.168.* ]] || [[ $ip == 10.* ]] || [[ $ip == 127.* ]]; then
        continue
    fi

    # Check if IP is in blacklist
    if grep -q "$ip" $BLACKLIST; then
        echo -e "${RED}[ALERT!] Malicious IP Detected: $ip${NC}"
        echo "$(date '+%Y-%m-%d %H:%M:%S') | MALICIOUS | $ip" >> $ALERT_LOG
    else
        echo -e "${GREEN}[SAFE] $ip${NC}"
    fi

done

echo -e "${GREEN}[+] Check Complete! Alerts saved to: $ALERT_LOG${NC}"


