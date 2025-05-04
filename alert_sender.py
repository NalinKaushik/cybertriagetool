# alert_sender.py
import requests

def send_to_prioritization_api(alert):
    try:
        response = requests.post("http://127.0.0.1:5000/prioritize", json=alert)
        if response.status_code == 200:
            result = response.json()
            print(f"🛡️ Alert Result -> {result['priority']} | {result['message']}")
        else:
            print(f"❌ Failed to prioritize alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"❗ Error connecting to prioritization API: {e}")

# Example Alert
alert = {
    "severity": 85,
    "description": "Suspicious login detected",
    "source_ip": "192.168.1.100"
}

send_to_prioritization_api(alert)
