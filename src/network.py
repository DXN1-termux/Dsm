import subprocess
from rich.panel import Panel

class NetworkAgent:
    def scan_full(self, target):
        """Advanced Nmap scan."""
        # -A: OS detection, version detection, script scanning, and traceroute
        cmd = ["nmap", "-A", "-T4", target]
        try:
            result = subprocess.check_output(cmd).decode()
            return Panel(result, title=f"Deep Scan: {target}", border_style="bold green")
        except:
            return Panel("[red]Nmap scan failed. Ensure nmap is installed.[/red]")

    def get_port_info(self, target, ports="1-1024"):
        cmd = ["nmap", "-p", ports, target]
        result = subprocess.check_output(cmd).decode()
        return Panel(result, title=f"Port Scan [{ports}]", border_style="yellow")
