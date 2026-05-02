from __future__ import annotations

import base64
import hashlib
import hmac
import os
from dataclasses import dataclass
from getpass import getpass

from .config import AppConfig, ConfigStore, LOG_FILE
from .utils import make_salt, now_iso

try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError, VerificationError
except Exception:  # pragma: no cover - optional dependency
    PasswordHasher = None
    VerifyMismatchError = Exception
    VerificationError = Exception


@dataclass
class AuthResult:
    ok: bool
    message: str = ""


def _pepper() -> bytes:
    # Optional external secret for a second layer of protection.
    return os.environ.get("DSM_PEPPER", "").encode("utf-8")


def _pbkdf2_hash(password: str, salt: str, iterations: int = 210_000) -> str:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8") + _pepper(),
        salt.encode("utf-8"),
        iterations,
    )
    return f"pbkdf2${iterations}${salt}${base64.urlsafe_b64encode(digest).decode('ascii')}"


def _pbkdf2_verify(stored: str, password: str) -> bool:
    try:
        _, iterations, salt, digest_b64 = stored.split("$", 3)
        iterations_i = int(iterations)
        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8") + _pepper(),
            salt.encode("utf-8"),
            iterations_i,
        )
        expected = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
        return hmac.compare_digest(candidate, expected)
    except Exception:
        return False


class SecurityManager:
    def __init__(self) -> None:
        self.store = ConfigStore()
        self.config = self.store.load()
        self._argon2 = None
        if PasswordHasher is not None:
            self._argon2 = PasswordHasher(
                time_cost=3,
                memory_cost=65536,
                parallelism=2,
                hash_len=32,
                salt_len=16,
            )

    def log(self, message: str) -> None:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(f"[{now_iso()}] {message}\n")

    def _hash(self, password: str, salt: str) -> str:
        if self._argon2 is not None:
            # Salt is mixed in as a pepper-like extra namespace to keep the stored
            # format explicit while still relying on Argon2id for the heavy lifting.
            return f"argon2${salt}${self._argon2.hash(password + _pepper().decode('utf-8', errors='ignore') + salt)}"
        return _pbkdf2_hash(password, salt)

    def _verify(self, stored: str, password: str, salt: str) -> bool:
        if stored.startswith("argon2$") and self._argon2 is not None:
            try:
                _, stored_salt, argon_hash = stored.split("$", 2)
                # stored_salt kept for audit compatibility; the actual Argon2 hash
                # already carries its own salt internally.
                self._argon2.verify(argon_hash, password + _pepper().decode('utf-8', errors='ignore') + stored_salt)
                return True
            except (VerifyMismatchError, VerificationError, ValueError):
                return False
            except Exception:
                return False
        if stored.startswith("pbkdf2$"):
            return _pbkdf2_verify(stored, password)
        return hmac.compare_digest(stored, self._hash(password, salt))

    def bootstrap(self) -> None:
        if self.config.password_hash and self.config.salt:
            return
        print("First run setup: create a DSM v6 password.")
        while True:
            first = getpass("New password: ")
            second = getpass("Confirm password: ")
            if not first:
                print("Password cannot be empty.")
                continue
            if first != second:
                print("Passwords do not match.")
                continue
            salt = make_salt()
            self.config.salt = salt
            self.config.password_hash = self._hash(first, salt)
            self.config.first_run = False
            self.store.save(self.config)
            self.log("Initial password configured")
            print("Password created.")
            return

    def verify(self, password: str) -> bool:
        if not self.config.password_hash or not self.config.salt:
            return False
        ok = self._verify(self.config.password_hash, password, self.config.salt)
        self.log(f"Authentication {'success' if ok else 'failure'}")
        return ok

    def rotate_password(self, old_password: str, new_password: str) -> AuthResult:
        if not self.verify(old_password):
            return AuthResult(False, "Old password did not match.")
        salt = make_salt()
        self.config.salt = salt
        self.config.password_hash = self._hash(new_password, salt)
        self.store.save(self.config)
        self.log("Password rotated")
        return AuthResult(True, "Password rotated successfully.")

    def admin_reset(self, new_password: str) -> None:
        salt = make_salt()
        self.config.salt = salt
        self.config.password_hash = self._hash(new_password, salt)
        self.store.save(self.config)
        self.log("Password reset")
