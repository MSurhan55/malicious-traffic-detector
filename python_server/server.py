# ─────────────────────────────────────────
# Malicious Traffic Detector
# Flask API Server
# ─────────────────────────────────────────
import sys
sys.path.append('/home/kali/malicious-traffic-detector/ai_model')
from gemini_explainer import explain_threat
from flask import Flask, jsonify, request
import subprocess
import os

app = Flask(__name__)

# File paths
ALERT_LOG = '/root/malicious-traffic-detector/logs/alerts.log'
BLOCKED_LOG = '/root/malicious-traffic-detector/logs/blocked.log'
TRAFFIC_LOG = '/root/malicious-traffic-detector/logs/traffic.log'

# ─────────────────────────────────────────
# Route 1: Check server status
# ─────────────────────────────────────────
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "running",
        "message": "Malicious Traffic Detector is active"
    })

# ─────────────────────────────────────────
# Route 2: Get latest alerts
# ─────────────────────────────────────────
@app.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        if not os.path.exists(ALERT_LOG):
            return jsonify({"alerts": [], "total": 0})

        with open(ALERT_LOG, 'r') as f:
            lines = f.readlines()

        alerts = []
        for line in lines:
            parts = line.strip().split(' | ')
            if len(parts) == 3:
                alerts.append({
                    "timestamp": parts[0],
                    "type": parts[1],
                    "ip": parts[2]
                })

        return jsonify({
            "alerts": alerts[-10:],  # Last 10 alerts
            "total": len(alerts)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# Route 3: Get blocked IPs
# ─────────────────────────────────────────
@app.route('/blocked', methods=['GET'])
def get_blocked():
    try:
        if not os.path.exists(BLOCKED_LOG):
            return jsonify({"blocked_ips": [], "total": 0})

        with open(BLOCKED_LOG, 'r') as f:
            lines = f.readlines()

        blocked = []
        for line in lines:
            parts = line.strip().split(' | ')
            if len(parts) == 3:
                blocked.append({
                    "timestamp": parts[0],
                    "action": parts[1],
                    "ip": parts[2]
                })

        return jsonify({
            "blocked_ips": blocked,
            "total": len(blocked)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# Route 4: Block a specific IP
# ─────────────────────────────────────────
@app.route('/block/<ip>', methods=['POST'])
def block_ip(ip):
    try:
        subprocess.run(
            ['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'],
            check=True
        )
        subprocess.run(
            ['sudo', 'iptables', '-A', 'OUTPUT', '-d', ip, '-j', 'DROP'],
            check=True
        )

        # Log it
        with open(BLOCKED_LOG, 'a') as f:
            from datetime import datetime
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BLOCKED | {ip}\n")

        return jsonify({
            "success": True,
            "message": f"IP {ip} has been blocked"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# Route 5: Unblock a specific IP
# ─────────────────────────────────────────
@app.route('/unblock/<ip>', methods=['POST'])
def unblock_ip(ip):
    try:
        subprocess.run(
            ['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'],
            check=True
        )
        subprocess.run(
            ['sudo', 'iptables', '-D', 'OUTPUT', '-d', ip, '-j', 'DROP'],
            check=True
        )

        return jsonify({
            "success": True,
            "message": f"IP {ip} has been unblocked"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# Route 6: Explain threat using Gemini
# ─────────────────────────────────────────
@app.route('/explain/<ip>', methods=['GET'])
def explain(ip):
    try:
        explanation = explain_threat(
            ip=ip,
            port=22,
            risk_level="HIGH",
            threat_score=100
        )
        return jsonify({
            "ip": ip,
            "explanation": explanation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# Run server
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("🚀 Starting Malicious Traffic Detector API...")
    print("📡 Running on http://localhost:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
