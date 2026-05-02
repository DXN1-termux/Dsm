from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime
from pathlib import Path
from typing import Iterable


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_salt() -> str:
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    return sha256_hex(f"{salt}:{password}")


def safe_join(base: Path, target: str) -> Path:
    path = (base / target).resolve()
    return path


def human_bytes(num: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num)
    for unit in units:
        if value < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} PB"


def clip(text: str, limit: int = 120) -> str:
    text = text.replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def iter_preview(items: Iterable[str], limit: int = 8) -> list[str]:
    out: list[str] = []
    for item in items:
        out.append(item)
        if len(out) >= limit:
            break
    return out
