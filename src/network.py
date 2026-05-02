import requests
import subprocess
from rich.panel import Panel

class NetworkAgent:
    def get_ip_info(self):
        try:
            public_ip = requests.get("https://api.ipify.org", timeout=5).text
        except:
            public_ip = "Offline"
            
        try:
            local_ip = subprocess.check_output(["hostname", "-I"]).decode().split()[0]
        except:
            local_ip = "Unknown"
            
        return Panel(
            f"[bold cyan]Local IP:[/bold cyan] {local_ip}\n[bold magenta]Public IP:[/bold magenta] {public_ip}",
            title="Network Info",
            border_style="cyan"
        )

    def quick_scan(self, target):
        # Basic nmap wrapper
        try:
            result = subprocess.check_output(["nmap", "-F", target]).decode()
            return Panel(result, title=f"Scan: {target}", border_style="green")
        except Exception as e:
            return Panel(f"[bold red]Error running nmap:[/bold red] {e}", border_style="red")
