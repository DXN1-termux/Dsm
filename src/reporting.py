from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from .config import CONFIG_DIR, AppConfig, ConfigStore
from .network import NetworkAgent
from .storage import StorageAgent
from .system import SystemAgent
from .utils import now_iso


REPORT_DIR = CONFIG_DIR / "reports"


@dataclass
class ReportBundle:
    created_at: str
    title: str
    system: dict
    storage: dict
    network: dict
    config: dict


class ReportingAgent:
    def __init__(self) -> None:
        self.store = ConfigStore()
        self.system = SystemAgent()
        self.storage = StorageAgent()
        self.network = NetworkAgent()
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

    def build_bundle(self, title: str = "DSM snapshot") -> ReportBundle:
        cfg = self.store.load()
        snap = self.system.snapshot()
        system = asdict(snap)
        storage = {
            "root": str(Path.cwd()),
            "largest_files": [],
        }
        try:
            table = self.storage.top_files(str(Path.cwd()), limit=8)
            storage["largest_files"] = [tuple(row.cells) for row in table.rows]  # type: ignore[attr-defined]
        except Exception:
            pass
        network = self.network.system_status_payload()
        return ReportBundle(
            created_at=now_iso(),
            title=title,
            system=system,
            storage=storage,
            network=network,
            config=cfg.__dict__,
        )

    def export_json(self, title: str = "DSM snapshot") -> Path:
        bundle = self.build_bundle(title=title)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = REPORT_DIR / f"report-{stamp}.json"
        path.write_text(json.dumps(asdict(bundle), indent=2), encoding="utf-8")
        return path

    def export_text(self, title: str = "DSM snapshot") -> Path:
        bundle = self.build_bundle(title=title)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = REPORT_DIR / f"report-{stamp}.txt"
        lines = [
            f"Title: {bundle.title}",
            f"Created: {bundle.created_at}",
            "",
            "SYSTEM",
            json.dumps(bundle.system, indent=2),
            "",
            "NETWORK",
            json.dumps(bundle.network, indent=2),
            "",
            "CONFIG",
            json.dumps(bundle.config, indent=2),
        ]
        path.write_text("\n".join(lines), encoding="utf-8")
        return path
