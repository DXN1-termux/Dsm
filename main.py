import sys
import logging
import signal
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Initialize Global Components
console = Console()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DSM")

# Add Pro-Modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from security import SecurityAgent
from system import SystemAgent
from storage import StorageAgent
from network import NetworkAgent
from pro_agents import IntegrityAgent, AutomationAgent

class DSMDispatcher:
    """The central orchestration engine for DSM Pro-Suite."""
    def __init__(self):
        self.security = SecurityAgent()
        self.system = SystemAgent()
        self.storage = StorageAgent()
        self.network = NetworkAgent()
        self.integrity = IntegrityAgent()
        self.automation = AutomationAgent()
        self.is_running = True

    def setup_interrupts(self):
        signal.signal(signal.SIGINT, self.handle_exit)

    def handle_exit(self, signum, frame):
        self.is_running = False
        console.print("\n[bold red]Interrupt detected. Safely shutting down...[/bold red]")
        sys.exit(0)

    def render_menu(self):
        console.clear()
        console.print(Panel("[bold cyan]DXN1 STORAGE MANAGER :: PRO-SUITE 5.0[/bold cyan]", border_style="blue"))
        table = Table(box=None, show_header=False)
        table.add_row("[bold]1.[/bold] System Pulse", "[bold]4.[/bold] Network Recon")
        table.add_row("[bold]2.[/bold] File Intelligence", "[bold]5.[/bold] Auth Settings")
        table.add_row("[bold]3.[/bold] Integrity Audit", "[bold]6.[/bold] Exit")
        console.print(Panel(table, title="COMMAND DISPATCHER"))

    def run(self):
        self.setup_interrupts()
        if not self.security.verify(Prompt.ask("Enter Auth-Key", password=True)):
            logger.error("Authentication Failure")
            return

        while self.is_running:
            self.render_menu()
            choice = Prompt.ask("Action", choices=["1", "2", "3", "4", "5", "6"])
            
            try:
                if choice == "1": self.system.live_monitor()
                elif choice == "2": console.print(self.storage.list_files())
                elif choice == "3": console.print(self.integrity.calculate_hash("main.py"))
                elif choice == "4": console.print(self.network.scan_full(Prompt.ask("Target")))
                elif choice == "5": self.security.update_password(Prompt.ask("New Key", password=True))
                elif choice == "6": self.is_running = False
            except Exception as e:
                logger.error(f"Dispatch Error: {e}")
                console.print(f"[bold red]Critical Error:[/bold red] {e}")
            
            Prompt.ask("\n[dim]Press Enter to continue[/dim]")

if __name__ == "__main__":
    DSMDispatcher().run()
