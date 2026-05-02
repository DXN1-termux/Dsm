from __future__ import annotations

import os
import platform
from dataclasses import dataclass
from pathlib import Path

import psutil
from rich.table import Table

from .utils import human_bytes


@dataclass
class SystemSnapshot:
    platform: str
    cpu_percent: float
    memory_percent: float
    memory_used: str
    memory_total: str
    disk_percent: float
    disk_used: str
    disk_total: str
    uptime_hours: float


class SystemAgent:
    def snapshot(self) -> SystemSnapshot:
        vm = psutil.virtual_memory()
        du = psutil.disk_usage(str(Path.home()))
        uptime = (psutil.boot_time())
        import time

        uptime_hours = (time.time() - uptime) / 3600.0
        return SystemSnapshot(
            platform=f"{platform.system()} {platform.release()}",
            cpu_percent=psutil.cpu_percent(interval=0.2),
            memory_percent=vm.percent,
            memory_used=human_bytes(vm.used),
            memory_total=human_bytes(vm.total),
            disk_percent=du.percent,
            disk_used=human_bytes(du.used),
            disk_total=human_bytes(du.total),
            uptime_hours=uptime_hours,
        )

    def render_table(self) -> Table:
        snap = self.snapshot()
        table = Table(title="System Pulse", show_lines=False)
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        table.add_row("Platform", snap.platform)
        table.add_row("CPU", f"{snap.cpu_percent:.1f}%")
        table.add_row("Memory", f"{snap.memory_percent:.1f}% ({snap.memory_used} / {snap.memory_total})")
        table.add_row("Disk", f"{snap.disk_percent:.1f}% ({snap.disk_used} / {snap.disk_total})")
        table.add_row("Uptime", f"{snap.uptime_hours:.1f} hours")
        table.add_row("Python", platform.python_version())
        return table
