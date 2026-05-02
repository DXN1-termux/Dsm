import os
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class StorageAgent:
    def list_files(self, path="."):
        table = Table(title=f"Directory: {os.path.abspath(path)}", box=None)
        table.add_column("Name", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Type", style="dim")
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            size = f"{os.path.getsize(full_path) / 1024:.1f} KB" if not is_dir else "DIR"
            table.add_row(item, size, "Folder" if is_dir else "File")
        return table

    def intelligent_purge(self, path="."):
        """Deep scan for common junk file patterns."""
        junk_patterns = ['.tmp', '.log', '.cache', '.bak', 'Thumbs.db']
        purged = []
        for root, dirs, files in os.walk(path):
            for f in files:
                if any(f.endswith(p) for p in junk_patterns):
                    os.remove(os.path.join(root, f))
                    purged.append(f)
        return purged
