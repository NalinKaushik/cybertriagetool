import random
import requests

# Function to generate a random alert
def generate_random_alert():
    severity = random.randint(1, 100)  # Random severity between 1 and 100
    alert_types = [
        "Suspicious login",
        "Malware detected",
        "Unusual network traffic",
        "Possible DDoS attack",
        "File integrity change"
    ]
    
    alert = {
        "severity": severity,
        "description": random.choice(alert_types),  # Random alert type
        "source_ip": f"192.168.1.{random.randint(1, 255)}",  # Random source IP
        "destination_ip": f"10.0.0.{random.randint(1, 255)}",  # Random destination IP
        "timestamp": f"2025-04-29T{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}",  # Random timestamp
    }
    return alert

# Function to send alert to prioritization API
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

# Function to generate and send multiple alerts
def generate_and_send_alerts(num_alerts=50):
    for _ in range(num_alerts):
        alert = generate_random_alert()  # Generate a random alert
        print(f"Generated alert: {alert}")  # Optionally print generated alert
        send_to_prioritization_api(alert)  # Send alert to prioritization API

# Simulate 50 alerts
generate_and_send_alerts(50)
