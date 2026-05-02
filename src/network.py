from __future__ import annotations

import json
import shutil
import socket
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from rich.table import Table

from .utils import clip


@dataclass
class ScanResult:
    target: str
    command: str
    output: str
    nmap_found: bool


class NetworkAgent:
    def has_nmap(self) -> bool:
        return shutil.which("nmap") is not None

    def has_tshark(self) -> bool:
        return shutil.which("tshark") is not None or shutil.which("tcpdump") is not None

    def quick_services(self, target: str, ports: list[int] | None = None) -> Table:
        ports = ports or [22, 80, 443, 445, 8080, 8443]
        table = Table(title=f"Quick port check: {target}")
        table.add_column("Port")
        table.add_column("Status")
        table.add_column("Banner")
        for port in ports:
            status, banner = self._probe(target, port)
            table.add_row(str(port), status, clip(banner, 46))
        return table

    def _probe(self, host: str, port: int, timeout: float = 0.35) -> tuple[str, str]:
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                try:
                    sock.settimeout(timeout)
                    sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                    data = sock.recv(128)
                    return "open", data.decode("utf-8", errors="ignore").strip().replace("\n", " ")
                except Exception:
                    return "open", ""
        except Exception:
            return "closed", ""

    def nmap_scan(self, target: str, mode: str = "intense") -> ScanResult:
        nmap = shutil.which("nmap")
        if not nmap:
            return ScanResult(target, "nmap not installed", "Install nmap for full scanning.", False)
        if mode == "quick":
            args = [nmap, "-Pn", "-F", target]
        elif mode == "service":
            args = [nmap, "-Pn", "-sV", target]
        elif mode == "os":
            args = [nmap, "-Pn", "-O", target]
        else:
            args = [nmap, "-Pn", "-A", "--top-ports", "100", target]
        completed = subprocess.run(args, capture_output=True, text=True, timeout=900)
        return ScanResult(target, " ".join(args), completed.stdout + completed.stderr, True)

    def service_tools_table(self) -> Table:
        table = Table(title="Service tools")
        table.add_column("Tool")
        table.add_column("Detected")
        for tool in ["nmap", "tshark", "tcpdump", "wireshark", "python3"]:
            table.add_row(tool, "yes" if shutil.which(tool) else "no")
        return table

    def system_status_payload(self) -> dict:
        import psutil

        vm = psutil.virtual_memory()
        du = psutil.disk_usage(str(Path.home()))
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.05),
            "memory_percent": vm.percent,
            "disk_percent": du.percent,
            "net": {"connections": len(psutil.net_connections(kind="inet"))},
            "tools": {
                "nmap": self.has_nmap(),
                "tshark": self.has_tshark(),
                "wireshark": shutil.which("wireshark") is not None,
            },
        }
