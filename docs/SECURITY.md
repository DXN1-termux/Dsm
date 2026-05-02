# Security Notes

- Passwords are hashed with Argon2id when available.
- If Argon2 is unavailable, DSM falls back to PBKDF2-HMAC-SHA256.
- A `DSM_PEPPER` environment variable can be set to add an external secret.
- Audit logs are stored under `~/.dsm-v6/audit.log`.
- The localhost panel binds to `127.0.0.1` only.
- Nmap execution is user-triggered and does not run in the background.
