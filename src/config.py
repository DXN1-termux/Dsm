from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

APP_NAME = "dsm-v6"
CONFIG_DIR = Path.home() / f".{APP_NAME}"
CONFIG_FILE = CONFIG_DIR / "config.json"
LOG_FILE = CONFIG_DIR / "audit.log"


def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class AppConfig:
    password_hash: str = ""
    salt: str = ""
    first_run: bool = True
    dashboard_port: int = 8765
    last_target: str = ""
    theme: str = "midnight"
    security_mode: str = "argon2"
    plugin_dir: str = "plugins"
    report_format: str = "json"
    auto_open_dashboard: bool = True


class ConfigStore:
    def __init__(self) -> None:
        ensure_config_dir()

    def load(self) -> AppConfig:
        if not CONFIG_FILE.exists():
            return AppConfig()
        try:
            payload = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return AppConfig(**payload)
        except Exception:
            return AppConfig()

    def save(self, config: AppConfig) -> None:
        ensure_config_dir()
        CONFIG_FILE.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")

    def update(self, **kwargs: Any) -> AppConfig:
        config = self.load()
        for key, value in kwargs.items():
            setattr(config, key, value)
        self.save(config)
        return config
