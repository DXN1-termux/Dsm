import psutil
from rich.table import Table
from rich.panel import Panel
from svg_utils import SVGGenerator

class SystemAgent:
    def get_stats(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "cpu": cpu_usage,
            "ram_percent": ram.percent,
            "ram_used": f"{ram.used / (1024**3):.1f}GB",
            "ram_total": f"{ram.total / (1024**3):.1f}GB",
            "disk_percent": disk.percent,
            "disk_free": f"{disk.free / (1024**3):.1f}GB",
            "battery": getattr(psutil.sensors_battery(), 'percent', 'N/A')
        }

    def generate_visual_report(self):
        stats = self.get_stats()
        path = SVGGenerator.generate_disk_pie(stats['disk_percent'])
        return f"[bold green]✓ Visual report generated at:[/bold green] {path}"

    def render_dashboard(self):
        stats = self.get_stats()
        table = Table(show_header=False, border_style="dim", box=None)
        table.add_row("CPU Usage", f"[bold cyan]{stats['cpu']}%[/bold cyan]")
        table.add_row("RAM Usage", f"[bold green]{stats['ram_percent']}%[/bold green] ({stats['ram_used']}/{stats['ram_total']})")
        table.add_row("Disk Free", f"[bold yellow]{stats['disk_free']}[/bold yellow] ({stats['disk_percent']}% full)")
        table.add_row("Battery", f"[bold magenta]{stats['battery']}%[/bold magenta]")
        
        return Panel(table, title="[bold]System Dashboard[/bold] • [dim]MADE WITH ❤️ BY DXN1[/dim]", border_style="blue")
