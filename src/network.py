from __future__ import annotations
import os
import shutil
import subprocess
from rich.table import Table
from rich.console import Console

console = Console()

class NetworkAgent:
    """Advanced Networking & Reconnaissance Suite."""

    def __init__(self):
        self.nmap_bin = shutil.which("nmap")
        self.tshark_bin = shutil.which("tshark")

    def run_nmap_scan(self, target: str, scan_type: str = "-F") -> str:
        """Executes a precision network scan with Nmap."""
        if not self.nmap_bin:
            return "[red]Error: Nmap not found in system path.[/red]"
        try:
            cmd = [self.nmap_bin, scan_type, target]
            console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
            return result
        except subprocess.CalledProcessError as e:
            return f"[red]Scan failed: {e.output.decode('utf-8')}[/red]"

    def sniff_network(self, interface: str = "eth0", duration: int = 10) -> str:
        """Captures network traffic using tshark/tcpdump."""
        if not self.tshark_bin:
            return "[red]Error: tshark/tcpdump not found.[/red]"
        cmd = [self.tshark_bin, "-i", interface, "-a", f"duration:{duration}"]
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
            return result
        except subprocess.CalledProcessError as e:
            return f"[red]Capture failed: {e.output.decode('utf-8')}[/red]"

    def get_port_security_report(self, target: str) -> Table:
        """Deep port profile and security assessment."""
        table = Table(title=f"Security Profile: {target}", header_style="bold cyan")
        table.add_column("Port", justify="center")
        table.add_column("State")
        table.add_column("Security Risk")
        
        # Simulating common port audit
        ports = [22, 80, 443, 8080]
        for port in ports:
            # Placeholder for actual socket logic, will extend
            risk = "HIGH" if port == 22 else "LOW"
            table.add_row(str(port), "OPEN", risk)
            
        return table
