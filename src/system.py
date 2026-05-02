import platform
import psutil
import socket

class SystemAgent:
    def __init__(self):
        self.os = platform.system()
        
    def get_comprehensive_stats(self):
        return {
            "platform": self.os,
            "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            "cpu_cores": psutil.cpu_count(logical=True),
            "ram": psutil.virtual_memory()._asdict(),
            "disk": psutil.disk_usage('/')._asdict(),
            "net_io": psutil.net_io_counters()._asdict()
        }

    def detect_environment(self):
        """Cross-platform environment detection."""
        return {
            "is_termux": os.environ.get("PREFIX") is not None,
            "is_wsl": "microsoft" in platform.release().lower(),
            "arch": platform.machine()
        }
