import json
import os
import hashlib

class SecurityAgent:
    CONFIG_FILE = ".dsm_auth"

    def __init__(self):
        self.password_hash = self._load_password()

    def _load_password(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                return f.read().strip()
        return hashlib.sha256("admin123".encode()).hexdigest()

    def update_password(self, new_password):
        self.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        with open(self.CONFIG_FILE, 'w') as f:
            f.write(self.password_hash)

    def verify(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash
