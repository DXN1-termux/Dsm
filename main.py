import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.prompt import IntPrompt, Prompt

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from security import SecurityAgent
from system import SystemAgent
from storage import StorageAgent
from network import NetworkAgent

console = Console()

def main():
    # 1. Security First
    security = SecurityAgent()
    if not security.authenticate():
        sys.exit(1)

    # 2. Initialize Agents
    system = SystemAgent()
    storage = StorageAgent()
    network = NetworkAgent()

    # 3. Main Loop
    while True:
        console.clear()
        
        # Header
        console.print(Panel(
            "[bold blue]DXN1 STORAGE MANAGER (DSM) v3.0[/bold blue]\n[dim]High-Performance System & File Intelligence Suite[/dim]",
            border_style="cyan",
            expand=True,
            align="center"
        ))

        # Dashboard
        console.print(system.render_dashboard())
        
        # Menu
        menu = Table(show_header=False, box=None, padding=(0, 2))
        menu.add_row("[bold cyan][1][/bold cyan] Live Monitor", "[bold cyan][4][/bold cyan] Network Scan")
        menu.add_row("[bold cyan][2][/bold cyan] List Files", "[bold cyan][5][/bold cyan] IP Intelligence")
        menu.add_row("[bold cyan][3][/bold cyan] Smart Purge", "[bold cyan][7][/bold cyan] System Info")
        menu.add_row("[bold red][6][/bold red] Exit DSM")
        
        console.print(Panel(menu, title="Main Menu [DSM 4.0]", border_style="dim"))

        choice = Prompt.ask("DSM Select", choices=["1", "2", "3", "4", "5", "6", "7"], default="6")

        if choice == "1":
            system.live_monitor()
        elif choice == "2":
            path = Prompt.ask("Enter path to list", default=".")
            console.print(storage.list_files(path))
        elif choice == "3":
            console.print("[yellow]Starting Smart Purge...[/yellow]")
            purged = storage.intelligent_purge(".")
            console.print(f"[green]Cleaned {len(purged)} junk files.[/green]")
        elif choice == "4":
            target = Prompt.ask("Enter Target (IP/Domain)")
            console.print(network.quick_scan(target))
        elif choice == "5":
            console.print(network.get_ip_info())
        elif choice == "7":
            console.print(system.get_dashboard_table())
        elif choice == "6":
            console.print("[bold red]Exiting DSM. Stay safe.[/bold red]")
            break
        
        Prompt.ask("\nPress [bold]Enter[/bold] to return")

if __name__ == "__main__":
    main()
