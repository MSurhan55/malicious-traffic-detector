# ─────────────────────────────────────────
# Malicious Traffic Detector
# Gemini API: Threat Explainer
# ─────────────────────────────────────────

from google import genai

# ─────────────────────────────────────────
# Configure Gemini API
# ─────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyCw3etV0rNwGZCBUmsGaVWadIbh9cv6Ms0"
client = genai.Client(api_key=GEMINI_API_KEY)

# ─────────────────────────────────────────
# Explain a threat in plain English
# ─────────────────────────────────────────
def explain_threat(ip, port, risk_level, threat_score):
    prompt = f"""
    You are a cybersecurity expert. Explain this network threat 
    briefly in 2-3 sentences in simple English:
    
    - IP Address: {ip}
    - Port: {port}
    - Risk Level: {risk_level}
    - Threat Score: {threat_score}/100
    
    Tell what this threat might be, why it is dangerous, 
    and what action to take. Keep it simple and short.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Unable to get explanation: {str(e)}"

# ─────────────────────────────────────────
# Test the explainer
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("   Gemini Threat Explainer Test     ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    explanation = explain_threat(
        ip="185.220.101.47",
        port=22,
        risk_level="HIGH",
        threat_score=100
    )

    print(f"IP: 185.220.101.47")
    print(f"Explanation:\n{explanation}")