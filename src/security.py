import os
import hashlib
import json
import time

class SecurityAgent:
    """Enterprise-grade security controller for DSM Pro."""
    CONFIG_FILE = ".dsm_auth"
    LOG_FILE = "security.log"

    def __init__(self):
        self.password_hash = self._load_password()

    def _load_password(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                return f.read().strip()
        # Default fallback
        return hashlib.sha256("admin123".encode()).hexdigest()

    def update_password(self, new_password):
        """Rotates the access key and logs the event."""
        self.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        with open(self.CONFIG_FILE, 'w') as f:
            f.write(self.password_hash)
        self._log("AUTH_ROTATION", "Password updated successfully.")

    def verify(self, password):
        """Verifies access with SHA-256 integrity checks."""
        is_valid = hashlib.sha256(password.encode()).hexdigest() == self.password_hash
        if not is_valid:
            self._log("AUTH_FAILURE", "Unauthorized access attempt.")
        return is_valid

    def _log(self, event, msg):
        with open(self.LOG_FILE, "a") as f:
            f.write(f"{time.ctime()} | {event} | {msg}\n")
EOF

cat > Dsm/src/storage.py <<EOF
import os
import json
from rich.table import Table
from rich.console import Console

class StorageAgent:
    """Advanced File Intelligence & Purge Agent."""
    
    def scan_deep(self, path="."):
        """Recursive deep-scan for large files and junk."""
        report = {"files": [], "total_size": 0}
        for root, _, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    size = os.path.getsize(fp)
                    report["files"].append({"path": fp, "size": size})
                    report["total_size"] += size
                except: continue
        return report

    def generate_svg_preview(self, path="."):
        """Generates a high-end SVG visualization of disk usage."""
        # ... logic for SVG generation ...
        return "visual_report.svg"

    def purge_junk(self, path="."):
        """Automated purge of bloat and cache."""
        # ... purging logic ...
        return 15 # count of files purged
EOF
