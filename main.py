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
            "[bold blue]DANI STORAGE MANAGER (DSM) v2.0[/bold blue]\n[dim]High-Performance Termux Utility Suite[/dim]",
            border_style="cyan",
            expand=True,
            align="center"
        ))

        # Dashboard
        console.print(system.render_dashboard())
        
        # Menu
        menu = Table(show_header=False, box=None, padding=(0, 2))
        menu.add_row("[bold cyan][1][/bold cyan] System Updates", "[bold cyan][4][/bold cyan] Network Scan")
        menu.add_row("[bold cyan][2][/bold cyan] List Files", "[bold cyan][5][/bold cyan] IP Intelligence")
        menu.add_row("[bold cyan][3][/bold cyan] Big File Finder", "[bold cyan][7][/bold cyan] Visual Disk SVG")
        menu.add_row("[bold red][6][/bold red] Exit DSM")
        
        console.print(Panel(menu, title="Main Menu", border_style="dim"))

        choice = Prompt.ask("DSM Select", choices=["1", "2", "3", "4", "5", "6", "7"], default="6")

        if choice == "1":
            console.print("[yellow]Updating System Resources...[/yellow]")
            os.system("pkg update && pkg upgrade -y")
        elif choice == "2":
            path = Prompt.ask("Enter path to list", default=".")
            console.print(storage.list_files(path))
        elif choice == "3":
            path = Prompt.ask("Enter path to analyze", default=".")
            console.print(storage.find_large_files(path))
        elif choice == "4":
            target = Prompt.ask("Enter Target (IP/Domain)")
            console.print(network.quick_scan(target))
        elif choice == "5":
            console.print(network.get_ip_info())
        elif choice == "7":
            console.print(system.generate_visual_report())
        elif choice == "6":
            console.print("[bold red]Exiting DSM. Stay safe.[/bold red]")
            break
        
        Prompt.ask("\nPress [bold]Enter[/bold] to return")

if __name__ == "__main__":
    main()
