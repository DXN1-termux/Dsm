import os
import time
from rich.table import Table
from rich.console import Console

console = Console()

class StorageAgent:
    def list_files(self, path="."):
        table = Table(title=f"Files in {os.path.abspath(path)}", box=None)
        table.add_column("Name", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Modified", style="dim")

        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            stats = os.stat(full_path)
            size = f"{stats.st_size / 1024:.1f} KB"
            mtime = time.ctime(stats.st_mtime)
            table.add_row(item, size, mtime)
        
        return table

    def find_large_files(self, path=".", limit=10):
        file_list = []
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    file_list.append((fp, os.path.getsize(fp)))
                except:
                    pass
        
        file_list.sort(key=lambda x: x[1], reverse=True)
        
        table = Table(title="Top Large Files", border_style="yellow")
        table.add_column("Path", style="dim")
        table.add_column("Size", style="bold red")
        
        for fp, size in file_list[:limit]:
            table.add_row(fp, f"{size / (1024**2):.1f} MB")
            
        return table
