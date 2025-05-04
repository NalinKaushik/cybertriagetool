import tkinter as tk
from tkinter import ttk
import psutil
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Playbooks for different alert types
playbooks = {
    'malware': [
        "Step 1: Isolate the infected system from the network.",
        "Step 2: Run an antivirus/anti-malware scan to identify malicious files.",
        "Step 3: Quarantine any suspicious files identified by the scanner.",
        "Step 4: Analyze the malware using a sandbox or reverse engineering tools.",
        "Step 5: Report findings to the security operations team."
    ],
    'phishing': [
        "Step 1: Identify the phishing email sender and assess the damage.",
        "Step 2: Block the sender’s domain and any linked URLs in the email.",
        "Step 3: Alert other users to be cautious of similar phishing emails.",
        "Step 4: Check if any sensitive information was accessed or leaked.",
        "Step 5: Investigate the phishing attack's vector (email, social media, etc.)."
    ],
    'ransomware': [
        "Step 1: Isolate all affected systems from the network immediately.",
        "Step 2: Identify the ransom note and analyze any files encrypted.",
        "Step 3: Report the attack to relevant authorities, if applicable.",
        "Step 4: Attempt decryption using known methods or recovery keys.",
        "Step 5: Restore from backups and strengthen network security to prevent future attacks."
    ],
    # Additional alert types can be added here
}

# Main application class
class CyberTriageTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cyber Triage Tool")
        self.geometry("1000x600")

        # Create a notebook widget (for tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.alert_frame = ttk.Frame(self.notebook)
        self.graph_frame = ttk.Frame(self.notebook)
        self.playbook_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.alert_frame, text="Alerts")
        self.notebook.add(self.graph_frame, text="Graphs")
        self.notebook.add(self.playbook_frame, text="Playbooks")

        # Initialize alert and graph sections
        self.alerts = []
        self.cpu_data = []
        self.memory_data = []

        # Playbook display section
        self.display_playbook_tabs()

        # Set up graph for CPU and Memory
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.cpu_line, = self.ax.plot([], [], label="CPU Usage (%)")
        self.memory_line, = self.ax.plot([], [], label="Memory Usage (%)")
        self.ax.set_xlim(0, 10)  # Show the last 10 seconds
        self.ax.set_ylim(0, 100)
        self.ax.set_title("System CPU and Memory Usage")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Usage (%)")
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Start the update loop for graphs, alerts, and playbooks
        self.update_graphs()
        self.update_alerts()

    def collect_system_data(self):
        """Collect system statistics (CPU, memory, disk)."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        return cpu_percent, memory_percent

    def update_graphs(self):
        """Update the CPU and Memory usage graphs."""
        cpu_percent, memory_percent = self.collect_system_data()

        # Update the graph data
        self.cpu_data.append(cpu_percent)
        self.memory_data.append(memory_percent)

        # Limit data to the last 10 values
        if len(self.cpu_data) > 10:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)

        # Update the graph
        self.cpu_line.set_data(range(len(self.cpu_data)), self.cpu_data)
        self.memory_line.set_data(range(len(self.memory_data)), self.memory_data)

        # Redraw the canvas
        self.canvas.draw()

        # Call this function again after 1 second
        self.after(1000, self.update_graphs)  # Update every 1 second

    def update_alerts(self):
        """Simulate alert updates."""
        new_alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "High CPU Usage",
            "severity": "Critical",
        }
        self.alerts.append(new_alert)
        self.display_alerts()

        # Call this function again after 5 seconds to simulate alert updates
        self.after(5000, self.update_alerts)  # Update every 5 seconds

    def display_alerts(self):
        """Display alerts in the GUI."""
        for widget in self.alert_frame.winfo_children():
            widget.destroy()

        for alert in self.alerts:
            alert_label = tk.Label(self.alert_frame, text=f"{alert['timestamp']} - {alert['type']} - {alert['severity']}")
            alert_label.pack()

    def display_playbook_tabs(self):
        """Display all playbooks in the playbook tab."""
        for widget in self.playbook_frame.winfo_children():
            widget.destroy()

        # Add a label and buttons for each playbook
        for playbook_type, steps in playbooks.items():
            # Add a button to open the playbook
            button = tk.Button(self.playbook_frame, text=f"Playbook for {playbook_type.capitalize()}",
                               command=lambda playbook=steps: self.display_playbook_steps(playbook))
            button.pack(pady=5)

    def display_playbook_steps(self, steps):
        """Display the steps of a selected playbook."""
        # Clear the current playbook steps if any
        for widget in self.playbook_frame.winfo_children():
            widget.destroy()

        # Display the steps of the selected playbook
        tk.Label(self.playbook_frame, text="Playbook Steps:", font=("Arial", 14)).pack(pady=5)
        for step in steps:
            tk.Label(self.playbook_frame, text=step).pack(pady=2)


if __name__ == "__main__":
    app = CyberTriageTool()
    app.mainloop()
