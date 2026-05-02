import getpass
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class SecurityAgent:
    def __init__(self, password="admin123"):
        self.password = password

    def authenticate(self):
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]DSM SECURITY CHECKPOINT[/bold cyan]\n[dim]Please verify your identity to continue[/dim]",
            border_style="blue"
        ))
        
        # We use standard getpass for secure input, or rich.prompt if we want visible but masked
        input_pass = getpass.getpass("  Enter DSM Password: ")
        
        if input_pass == self.password:
            console.print("[bold green]✓ Access Granted.[/bold green]")
            return True
        else:
            console.print("[bold red]✗ Access Denied: Incorrect Password.[/bold red]")
            return False
