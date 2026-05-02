import psutil
import platform
import os
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn

class SystemAgent:
    def get_stats(self):
        # CPU
        cpu_usage = psutil.cpu_percent(interval=None)
        
        # RAM
        ram = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        # Battery (if available)
        try:
            battery = psutil.sensors_battery()
            bat_str = f"{battery.percent}%" if battery else "N/A"
        except:
            bat_str = "N/A"

        return {
            "cpu": cpu_usage,
            "ram_percent": ram.percent,
            "ram_used": f"{ram.used / (1024**3):.1f}GB",
            "ram_total": f"{ram.total / (1024**3):.1f}GB",
            "disk_percent": disk.percent,
            "disk_free": f"{disk.free / (1024**3):.1f}GB",
            "battery": bat_str
        }

    def render_dashboard(self):
        stats = self.get_stats()
        
        table = Table(show_header=False, border_style="dim")
        table.add_row("CPU Usage", f"[bold cyan]{stats['cpu']}%[/bold cyan]")
        table.add_row("RAM Usage", f"[bold green]{stats['ram_percent']}%[/bold green] ({stats['ram_used']}/{stats['ram_total']})")
        table.add_row("Disk Free", f"[bold yellow]{stats['disk_free']}[/bold yellow] ({stats['disk_percent']}% full)")
        table.add_row("Battery", f"[bold magenta]{stats['battery']}[/bold magenta]")
        
        return Panel(table, title="[bold]System Dashboard[/bold]", border_style="blue")
