from __future__ import annotations

from pathlib import Path
from typing import Iterable

from rich.table import Table

from .utils import human_bytes, clip


class StorageAgent:
    def list_directory(self, root: str = ".") -> Table:
        base = Path(root).expanduser().resolve()
        table = Table(title=f"Storage View: {base}")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Size", justify="right")
        table.add_column("Modified")
        for item in sorted(base.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))[:40]:
            try:
                size = human_bytes(item.stat().st_size) if item.is_file() else "-"
                modified = item.stat().st_mtime
                import datetime

                mod = datetime.datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M")
                kind = "dir" if item.is_dir() else "file"
                table.add_row(clip(item.name, 36), kind, size, mod)
            except Exception:
                continue
        return table

    def top_files(self, root: str = ".", limit: int = 12) -> Table:
        base = Path(root).expanduser().resolve()
        entries: list[tuple[int, Path]] = []
        for path in base.rglob("*"):
            if path.is_file():
                try:
                    entries.append((path.stat().st_size, path))
                except Exception:
                    pass
        entries.sort(reverse=True, key=lambda x: x[0])
        table = Table(title=f"Largest files under {base}")
        table.add_column("Size", justify="right")
        table.add_column("Path", style="cyan")
        for size, path in entries[:limit]:
            table.add_row(human_bytes(size), clip(str(path), 80))
        return table
