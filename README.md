# 🔒 Malicious Traffic Detector

An AI-powered real-time network traffic monitoring tool that detects malicious connections, scores threats, explains them in plain English using Gemini AI, and alerts users through a Chromium browser extension.

Built as my portfolio project combining cybersecurity, machine learning, and web technologies.

---

## 🚀 Features

- **Real-time traffic monitoring** using tcpdump
- **Blacklist-based detection** against known malicious IPs
- **AI threat scoring** using Random Forest classifier (0-100 risk score)
- **Plain English explanations** powered by Google Gemini AI
- **Auto IP blocking** using iptables
- **Browser extension** showing live alerts in Chromium
- **REST API** built with Python Flask connecting all components

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Traffic Capture | Bash + tcpdump |
| Threat Detection | Python + Scikit-learn |
| AI Explanations | Google Gemini API |
| Backend API | Python Flask |
| IP Blocking | iptables |
| Browser Extension | HTML + JavaScript |
| Platform | Kali Linux |

---

## 📁 Project Structure
```
malicious-traffic-detector/
├── bash_scripts/
│   ├── traffic_capture.sh      # Captures live network traffic
│   ├── blacklist_checker.sh    # Checks IPs against blacklist
│   ├── live_monitor.sh         # Real-time live monitoring
│   └── ip_blocker.sh           # Auto blocks malicious IPs
├── python_server/
│   └── server.py               # Flask REST API server
├── ai_model/
│   ├── threat_detector.py      # ML threat scoring model
│   └── gemini_explainer.py     # Gemini AI explanations
├── browser_extension/
│   ├── manifest.json           # Extension config
│   ├── popup.html              # Extension UI
│   ├── popup.js                # Extension logic
│   └── background.js           # Background service worker
├── logs/                       # Traffic and alert logs
└── data/                       # Blacklist data
```

---

## ⚙️ Installation

### Requirements
- Kali Linux (or any Debian-based Linux)
- Python 3.x
- Chromium browser

### Step 1 — Clone the repository
```bash
git clone https://github.com/MSurhan55/malicious-traffic-detector.git
cd malicious-traffic-detector
```

### Step 2 — Install Python dependencies
```bash
pip3 install flask scikit-learn pandas numpy requests google-genai joblib --break-system-packages
```

### Step 3 — Add your Gemini API key
Open `ai_model/gemini_explainer.py` and replace:
```python
GEMINI_API_KEY = "your_api_key_here"
```
Get a free key at: https://aistudio.google.com

### Step 4 — Set up log directories
```bash
sudo mkdir -p /root/malicious-traffic-detector/logs
sudo touch /root/malicious-traffic-detector/logs/traffic.log
sudo touch /root/malicious-traffic-detector/logs/alerts.log
sudo touch /root/malicious-traffic-detector/logs/blocked.log
```

---

## 🚦 Usage

### Step 1 — Start live traffic monitor
```bash
sudo ~/malicious-traffic-detector/bash_scripts/live_monitor.sh
```

### Step 2 — Start Flask API server
```bash
cd ~/malicious-traffic-detector/python_server
python3 server.py
```

### Step 3 — Train AI model
```bash
cd ~/malicious-traffic-detector/ai_model
python3 threat_detector.py
```

### Step 4 — Load browser extension
1. Open Chromium → `chromium://extensions`
2. Enable Developer Mode
3. Click Load Unpacked
4. Select `browser_extension/` folder

### Step 5 — Block malicious IPs
```bash
sudo ~/malicious-traffic-detector/bash_scripts/ip_blocker.sh
```

---

## 🔄 How It Works
```
Network Traffic
      ↓
Bash Script (tcpdump captures live traffic)
      ↓
Blacklist Check (known malicious IPs)
      ↓
AI Layer (Random Forest threat scoring)
      ↓
Flask API (serves results to extension)
      ↓
Browser Extension (shows live alerts)
      ↓
Gemini AI (explains threats in plain English)
      ↓
Auto Block (iptables blocks malicious IPs)
```

---

## 🤖 AI Model

The threat detection uses a **Random Forest Classifier** trained on network traffic features:

- IP address octets
- Port risk scoring
- Protocol analysis
- IP range reputation

Risk levels: 🟢 LOW (0-39) | 🟡 MEDIUM (40-69) | 🔴 HIGH (70-100)

---

## 📌 Future Improvements

- Train on real captured traffic for higher accuracy
- Add deep learning (LSTM) for pattern detection
- Integrate with VirusTotal API for IP reputation
- Docker support for cross-platform deployment
- Dashboard with traffic visualization charts

---

## 👨‍💻 Author

**Muhammad Surhan**
Computer Systems Engineering — MUET, Jamshoro
IEEE Computer Society Member

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).