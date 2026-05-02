import subprocess
from rich.panel import Panel

class NetworkAgent:
    # Existing methods...
    def port_knocking(self, ip, sequence):
        # Implementation for port knocking sequence
        return f"Knocking {ip} with {sequence}..."
    
    def threat_scan(self, target):
        # Implementation for deep vulnerability scanning
        return "Scanning for CVEs on " + target
    
    def netstat_monitor(self):
        # Live connection monitor
        return subprocess.check_output(["netstat", "-tuln"]).decode()
