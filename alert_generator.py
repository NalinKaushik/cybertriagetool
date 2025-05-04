import psutil
import os
import json
import random
import time
from datetime import datetime
from playbooks import playbooks
from data_collection import collect_system_data

SUSPICIOUS_PROCESSES = ['powershell.exe', 'cmd.exe', 'wmic.exe', 'regsvr32.exe', 'mshta.exe']
CRITICAL_FILES = ['C:\\Windows\\System32\\drivers\\etc\\hosts']
known_users = set()
file_mod_times = {}

def detect_anomalies(cpu_usage, memory_usage):
    # Example: Basic threshold-based anomaly detection
    if cpu_usage > 85 or memory_usage > 85:
        return "Anomaly Detected"
    return "Normal"

def get_threat_intelligence():
    # Example: Integrating with AlienVault OTX (or any other threat intelligence API)
    # You can replace this with real Threat Intelligence API integration
    return [{'indicator': '192.168.1.100'}, {'indicator': '10.0.0.100'}]

def check_for_threats(event_data):
    threats = get_threat_intelligence()
    for threat in threats:
        if 'indicator' in threat:
            if threat['indicator'] == event_data['ip']:
                print(f"Threat detected: {event_data['ip']} matches a known threat intelligence IOC!")
                send_email_alert("Malicious IP detected from threat intelligence.", "Threat Intelligence Alert")

def send_email_alert(subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    sender_email = "your_email@example.com"
    receiver_email = "receiver_email@example.com"
    password = "your_email_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def generate_alerts(system_data):
    alerts = []

    # 1. AI Anomaly Detection
    cpu_usage = system_data['cpu_percent']
    memory_usage = system_data['memory_percent']
    anomaly = detect_anomalies(cpu_usage, memory_usage)
    if anomaly == "Anomaly Detected":
        alerts.append({"alert": "System anomaly detected", "severity": 90})

    # 2. Threat Intelligence Matching
    network_ip = system_data['network_stats']['ip']
    check_for_threats({'ip': network_ip})

    return alerts
