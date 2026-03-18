#!/bin/bash

# ─────────────────────────────────────────
# Malicious Traffic Detector
# Script 3: Live Monitor (Real Time)
# ─────────────────────────────────────────

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Paths
BLACKLIST=~/malicious-traffic-detector/data/blacklist.txt
ALERT_LOG=/root/malicious-traffic-detector/logs/alerts.log
CHECKED_IPS=/tmp/checked_ips.txt

# Create temp file for already checked IPs
touch $CHECKED_IPS

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}   Malicious Traffic Detector LIVE   ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Download blacklist if not exists
if [ ! -f "$BLACKLIST" ]; then
    echo -e "${YELLOW}[*] Downloading blacklist...${NC}"
    curl -s https://rules.emergingthreats.net/blockrules/compromised-ips.txt -o $BLACKLIST
    echo -e "${GREEN}[+] Blacklist ready!${NC}"
fi

# Detect interface
INTERFACE=$(ip route | grep default | awk '{print $5}')
echo -e "${GREEN}[+] Monitoring Interface: $INTERFACE${NC}"
echo -e "${GREEN}[+] Live monitoring started...${NC}"
echo -e "${YELLOW}[*] Press Ctrl+C to stop${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Live capture and check
sudo tcpdump -i $INTERFACE -n -l 2>/dev/null | while read line; do

    # Extract IPs from each line
    echo "$line" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | while read ip; do

        # Skip private/local IPs
        if [[ $ip == 192.168.* ]] || [[ $ip == 10.* ]] || [[ $ip == 127.* ]] || [[ $ip == 0.* ]]; then
            continue
        fi

        # Skip already checked IPs
        if grep -q "$ip" $CHECKED_IPS; then
            continue
        fi

        # Mark IP as checked
        echo "$ip" >> $CHECKED_IPS

        # Check against blacklist
        if grep -q "$ip" $BLACKLIST; then
            echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo -e "${RED}[🚨 ALERT!] MALICIOUS IP: $ip${NC}"
            echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
            echo "$(date '+%Y-%m-%d %H:%M:%S') | MALICIOUS | $ip" >> $ALERT_LOG
        else
            echo -e "${GREEN}[✓ SAFE] $ip${NC}"
        fi

    done
done