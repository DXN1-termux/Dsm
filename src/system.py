import time
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
import psutil

class SystemAgent:
    def get_dashboard_table(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        table = Table(box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_row("CPU", f"{cpu}%")
        table.add_row("RAM", f"{ram}%")
        return table

    def live_monitor(self):
        """Native terminal live-refresh dashboard."""
        with Live(self.get_dashboard_table(), refresh_per_second=2, transient=True) as live:
            for _ in range(20):
                time.sleep(0.5)
                live.update(self.get_dashboard_table())
