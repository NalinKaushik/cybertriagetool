import psutil
import json
import time
import os
from datetime import datetime
import socket

# Suspicious process names (expand this list)
SUSPICIOUS_PROCESSES = ['powershell.exe', 'cmd.exe', 'wmic.exe', 'regsvr32.exe', 'mshta.exe']

# Critical files to watch (Windows example)
CRITICAL_FILES = ['C:\\Windows\\System32\\drivers\\etc\\hosts']

# Previously observed users
known_users = set()

# Previous file modification timestamps
file_mod_times = {}

def collect_system_data():
    """Collect system statistics (CPU, memory, disk, and network data)."""
    system_data = {
        'timestamp': str(datetime.now()),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'network_stats': get_network_info()  # Get network interface IP addresses
    }
    return system_data

def get_network_info():
    """Get network interface information, including IP addresses."""
    network_info = {}
    addrs = psutil.net_if_addrs()
    for interface, addrs_list in addrs.items():
        for addr in addrs_list:
            if addr.family == socket.AF_INET:  # IPv4 address (from the socket module)
                network_info[interface] = addr.address
    return network_info

def detect_process_anomalies():
    """Detect suspicious running processes."""
    anomalies = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            pname = proc.info['name']
            pexe = proc.info['exe']
            if pname and pname.lower() in SUSPICIOUS_PROCESSES:
                if pexe and not pexe.startswith('C:\\Windows'):
                    anomalies.append({'pid': proc.info['pid'], 'name': pname, 'exe': pexe})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return anomalies

def detect_network_anomalies():
    """Detect unusual outgoing connections."""
    anomalies = []
    for conn in psutil.net_connections(kind='inet'):
        try:
            if conn.status == 'ESTABLISHED' and conn.raddr:
                remote_ip = conn.raddr.ip
                if not (remote_ip.startswith('10.') or remote_ip.startswith('192.168.') or remote_ip.startswith('172.')):
                    anomalies.append({'pid': conn.pid, 'remote_ip': remote_ip, 'remote_port': conn.raddr.port})
        except Exception:
            continue
    return anomalies

def detect_user_activity():
    """Detect new users added to the system."""
    anomalies = []
    global known_users
    try:
        current_users = set(u.name for u in psutil.users())
        new_users = current_users - known_users
        if new_users:
            for user in new_users:
                anomalies.append({'new_user': user})
        known_users = current_users
    except Exception:
        pass
    return anomalies

def detect_file_changes():
    """Detect if critical files were modified."""
    anomalies = []
    global file_mod_times
    for filepath in CRITICAL_FILES:
        if os.path.exists(filepath):
            last_modified = os.path.getmtime(filepath)
            if filepath in file_mod_times:
                if last_modified != file_mod_times[filepath]:
                    anomalies.append({'file_changed': filepath})
            file_mod_times[filepath] = last_modified
    return anomalies

def save_data_to_file(data, filename="system_data.json"):
    """Save system data to a file."""
    with open(filename, 'a') as file:
        json.dump(data, file)
        file.write("\n")

def run_agent():
    """Collect data and save to file."""
    print("Data Collection Agent started...")
    while True:
        system_data = collect_system_data()
        print(f"Collected Data: {system_data}")
        save_data_to_file(system_data)
        time.sleep(5)  # Collect data every 5 seconds

if __name__ == '__main__':
    run_agent()
