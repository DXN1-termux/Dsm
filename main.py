from __future__ import annotations

import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from src.config import AppConfig, ConfigStore, LOG_FILE
from src.dashboard import DashboardServer
from src.network import NetworkAgent
from src.reporting import ReportingAgent
from src.security import SecurityManager
from src.storage import StorageAgent
from src.system import SystemAgent
from src.utils import clip

console = Console()


def center_title() -> Panel:
    body = Text()
    body.append("DXN1 Storage Manager", style="bold cyan")
    body.append("\n")
    body.append("DSM v6 Pro Suite", style="bold white")
    body.append("\n")
    body.append("terminal control, localhost dashboard, security, storage, and recon", style="dim")
    return Panel(body, border_style="cyan", box=box.DOUBLE)


class DSMApp:
    def __init__(self) -> None:
        self.store = ConfigStore()
        self.config = self.store.load()
        self.security = SecurityManager()
        self.system = SystemAgent()
        self.storage = StorageAgent()
        self.network = NetworkAgent()
        self.reports = ReportingAgent()
        self.dashboard: DashboardServer | None = None

    def authenticate(self) -> bool:
        self.security.bootstrap()
        for _ in range(3):
            password = Prompt.ask("Master password", password=True)
            if self.security.verify(password):
                return True
            console.print("[red]Wrong password.[/red]")
        return False

    def menu(self) -> None:
        table = Table(box=box.SIMPLE_HEAVY, expand=True, show_header=False)
        table.add_column("Key")
        table.add_column("Action")
        table.add_row("1", "System pulse")
        table.add_row("2", "Directory view")
        table.add_row("3", "Largest files")
        table.add_row("4", "Quick port check")
        table.add_row("5", "Nmap recon")
        table.add_row("6", "Rotate password")
        table.add_row("7", "Start localhost dashboard")
        table.add_row("8", "Service toolbox")
        table.add_row("9", "Audit log")
        table.add_row("10", "Export snapshot")
        table.add_row("0", "Exit")
        console.print(Panel(table, title="COMMAND CENTER", border_style="blue"))

    def show_log(self) -> None:
        if not LOG_FILE.exists():
            console.print("[dim]No audit log yet.[/dim]")
            return
        text = LOG_FILE.read_text(encoding="utf-8")[-6000:]
        console.print(Panel(text or "[empty]", title="Audit log", border_style="green"))

    def start_dashboard(self) -> None:
        port = int(self.config.dashboard_port or 8765)
        self.dashboard = DashboardServer(port=port)
        url = self.dashboard.start()
        console.print(Panel(f"Dashboard running at [bold]{url}[/bold]", title="Localhost", border_style="green"))
        if Confirm.ask("Open in browser", default=self.config.auto_open_dashboard):
            try:
                webbrowser.open(url)
            except Exception:
                pass

    def rotate_password(self) -> None:
        old = Prompt.ask("Current password", password=True)
        new = Prompt.ask("New password", password=True)
        confirm = Prompt.ask("Confirm new password", password=True)
        if new != confirm:
            console.print("[red]Passwords do not match.[/red]")
            return
        result = self.security.rotate_password(old, new)
        console.print(f"[green]{result.message}[/green]" if result.ok else f"[red]{result.message}[/red]")

    def nmap_scan(self) -> None:
        target = Prompt.ask("Target IP/host")
        mode = Prompt.ask("Mode", choices=["quick", "service", "os", "intense"], default="intense")
        self.config = self.store.update(last_target=target)
        result = self.network.nmap_scan(target, mode)
        console.print(Panel(result.command, title="Command", border_style="cyan"))
        console.print(Panel(result.output[-12000:] or "No output.", title="Scan result", border_style="magenta"))

    def export_snapshot(self) -> None:
        fmt = Prompt.ask("Format", choices=["json", "txt"], default=self.config.report_format)
        title = Prompt.ask("Title", default="DSM snapshot")
        path = self.reports.export_json(title) if fmt == "json" else self.reports.export_text(title)
        self.store.update(report_format=fmt)
        console.print(Panel(str(path), title="Exported report", border_style="green"))

    def run(self) -> None:
        console.clear()
        console.print(center_title())
        if not self.authenticate():
            console.print("[red]Access denied.[/red]")
            return

        while True:
            console.clear()
            console.print(center_title())
            self.menu()
            choice = Prompt.ask("Select", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

            try:
                if choice == "0":
                    break
                if choice == "1":
                    console.print(Panel(self.system.render_table(), title="Live system pulse"))
                    Prompt.ask("Enter to continue")
                elif choice == "2":
                    root = Prompt.ask("Path", default=str(Path.cwd()))
                    console.print(Panel(self.storage.list_directory(root), title="Directory view"))
                    Prompt.ask("Enter to continue")
                elif choice == "3":
                    root = Prompt.ask("Search root", default=str(Path.cwd()))
                    console.print(Panel(self.storage.top_files(root), title="Largest files"))
                    Prompt.ask("Enter to continue")
                elif choice == "4":
                    target = Prompt.ask("Target host")
                    console.print(Panel(self.network.quick_services(target), title="Quick port check"))
                    Prompt.ask("Enter to continue")
                elif choice == "5":
                    self.nmap_scan()
                    Prompt.ask("Enter to continue")
                elif choice == "6":
                    self.rotate_password()
                    Prompt.ask("Enter to continue")
                elif choice == "7":
                    self.start_dashboard()
                    Prompt.ask("Enter to continue")
                elif choice == "8":
                    console.print(Panel(self.network.service_tools_table(), title="Service toolbox"))
                    Prompt.ask("Enter to continue")
                elif choice == "9":
                    self.show_log()
                    Prompt.ask("Enter to continue")
                elif choice == "10":
                    self.export_snapshot()
                    Prompt.ask("Enter to continue")
            except Exception as exc:
                console.print(f"[red]Error:[/red] {exc}")
                Prompt.ask("Enter to continue")

        console.print("[bold green]Bye.[/bold green]")


def main() -> None:
    DSMApp().run()


if __name__ == "__main__":
    main()
