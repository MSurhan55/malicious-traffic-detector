#!/bin/bash

# ─────────────────────────────────────────
# Malicious Traffic Detector
# Script 4: Auto IP Blocker
# ─────────────────────────────────────────

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Paths
ALERT_LOG=/root/malicious-traffic-detector/logs/alerts.log
BLOCKED_LOG=/root/malicious-traffic-detector/logs/blocked.log

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}      Auto IP Blocker Active         ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Function to block an IP
block_ip() {
    local ip=$1

    # Check if already blocked
    if iptables -L INPUT -n | grep -q "$ip"; then
        echo -e "${YELLOW}[!] Already blocked: $ip${NC}"
        return
    fi

    # Block incoming traffic from IP
    sudo iptables -A INPUT -s $ip -j DROP

    # Block outgoing traffic to IP
    sudo iptables -A OUTPUT -d $ip -j DROP

    echo -e "${RED}[🚫 BLOCKED] $ip${NC}"
    echo "$(date '+%Y-%m-%d %H:%M:%S') | BLOCKED | $ip" >> $BLOCKED_LOG
}

# Function to unblock an IP
unblock_ip() {
    local ip=$1

    sudo iptables -D INPUT -s $ip -j DROP
    sudo iptables -D OUTPUT -d $ip -j DROP

    echo -e "${GREEN}[✓ UNBLOCKED] $ip${NC}"
}

# Function to show all blocked IPs
show_blocked() {
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}       Currently Blocked IPs         ${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    if [ -f "$BLOCKED_LOG" ]; then
        cat $BLOCKED_LOG
    else
        echo -e "${GREEN}No IPs blocked yet${NC}"
    fi
}

# Auto block all malicious IPs from alert log
auto_block() {
    echo -e "${YELLOW}[*] Reading alerts and blocking malicious IPs...${NC}"

    if [ ! -f "$ALERT_LOG" ]; then
        echo -e "${RED}[!] No alert log found. Run live monitor first.${NC}"
        exit 1
    fi

    # Extract malicious IPs from alert log
    grep "MALICIOUS" $ALERT_LOG | awk '{print $NF}' | sort -u | while read ip; do
        block_ip $ip
    done

    echo -e "${GREEN}[+] Auto blocking complete!${NC}"
}

# Menu
echo -e "${YELLOW}Choose an option:${NC}"
echo "1) Auto block all malicious IPs from alerts"
echo "2) Block a specific IP"
echo "3) Unblock a specific IP"
echo "4) Show all blocked IPs"

read -p "Enter choice [1-4]: " choice

case $choice in
    1) auto_block ;;
    2)
        read -p "Enter IP to block: " ip
        block_ip $ip
        ;;
    3)
        read -p "Enter IP to unblock: " ip
        unblock_ip $ip
        ;;
    4) show_blocked ;;
    *) echo -e "${RED}Invalid choice${NC}" ;;
esac