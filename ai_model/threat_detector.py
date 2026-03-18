# ─────────────────────────────────────────
# Malicious Traffic Detector
# AI Layer: Threat Detector
# ─────────────────────────────────────────

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Paths
MODEL_PATH = os.path.expanduser('~/malicious-traffic-detector/ai_model/threat_model.pkl')
SCALER_PATH = os.path.expanduser('~/malicious-traffic-detector/ai_model/scaler.pkl')

# High risk ports
HIGH_RISK_PORTS = [22, 23, 3389, 445, 135, 139, 4444, 5555, 6666, 7777]
MEDIUM_RISK_PORTS = [80, 8080, 8888, 3306, 5432, 27017]

# ─────────────────────────────────────────
# Extract features from an IP/connection
# ─────────────────────────────────────────
def extract_features(ip, port=80, protocol='TCP'):
    features = []

    octets = ip.split('.')
    if len(octets) == 4:
        try:
            features.extend([int(o) for o in octets])
        except:
            features.extend([0, 0, 0, 0])
    else:
        features.extend([0, 0, 0, 0])

    if port in HIGH_RISK_PORTS:
        port_risk = 3
    elif port in MEDIUM_RISK_PORTS:
        port_risk = 2
    else:
        port_risk = 1
    features.append(port_risk)

    protocol_score = {'TCP': 1, 'UDP': 2, 'ICMP': 3}.get(protocol, 1)
    features.append(protocol_score)

    try:
        first_octet = int(octets[0])
    except:
        first_octet = 0

    if first_octet in [185, 194, 45, 91]:
        ip_risk = 3
    elif first_octet in [103, 104, 107]:
        ip_risk = 2
    else:
        ip_risk = 1
    features.append(ip_risk)

    return features

# ─────────────────────────────────────────
# Train the AI model
# ─────────────────────────────────────────
def train_model():
    print("[*] Training AI model...")

    normal_data = []
    for _ in range(500):
        ip = f"8.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}"
        port = np.random.choice([80, 443, 53, 123])
        normal_data.append(extract_features(ip, port, 'TCP'))

    malicious_data = []
    for _ in range(100):
        ip = f"185.{np.random.randint(0,255)}.{np.random.randint(0,255)}.{np.random.randint(0,255)}"
        port = np.random.choice(HIGH_RISK_PORTS)
        malicious_data.append(extract_features(ip, port, 'TCP'))

    X = np.array(normal_data + malicious_data)
    y = np.array([0] * 500 + [1] * 100)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    os.makedirs(os.path.expanduser('~/malicious-traffic-detector/ai_model'), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print("[+] AI model trained and saved!")
    return model, scaler

# ─────────────────────────────────────────
# Load existing model or train new one
# ─────────────────────────────────────────
def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        print("[+] Loading existing AI model...")
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    else:
        return train_model()

# ─────────────────────────────────────────
# Predict threat score for an IP
# ─────────────────────────────────────────
def predict_threat(ip, port=80, protocol='TCP'):
    model, scaler = load_model()

    features = extract_features(ip, port, protocol)
    features_scaled = scaler.transform([features])

    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0]

    threat_score = int(probability[1] * 100)

    return {
        "ip": ip,
        "port": port,
        "protocol": protocol,
        "threat_score": threat_score,
        "is_malicious": bool(prediction == 1),
        "risk_level": "HIGH" if threat_score >= 70 else "MEDIUM" if threat_score >= 40 else "LOW"
    }

# ─────────────────────────────────────────
# Test the model
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   AI Threat Detector - Test Mode   ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    model, scaler = load_model()

    test_ips = [
        ("8.8.8.8", 80, "TCP"),
        ("185.220.101.47", 22, "TCP"),
        ("192.168.1.1", 80, "TCP"),
        ("45.33.32.156", 4444, "TCP"),
    ]

    print("\n[*] Testing threat detection:\n")
    for ip, port, protocol in test_ips:
        result = predict_threat(ip, port, protocol)
        emoji = "🔴" if result['risk_level'] == 'HIGH' else "🟡" if result['risk_level'] == 'MEDIUM' else "🟢"
        print(f"{emoji} IP: {result['ip']:<20} Port: {port:<6} Score: {result['threat_score']}/100  Risk: {result['risk_level']}")
