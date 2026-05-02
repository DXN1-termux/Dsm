# DSM Architecture

DSM v6 is organized as a small, composable terminal suite:

- `main.py` handles authentication and menu orchestration.
- `src/security.py` manages password creation, verification, and rotation.
- `src/system.py` renders live host metrics.
- `src/storage.py` lists directories and surfaces large files.
- `src/network.py` handles quick probes and nmap wrappers.
- `src/dashboard.py` exposes the localhost web panel.
- `src/reporting.py` exports snapshots to JSON or text.

The design goal is simple: keep the core runnable in Termux while leaving room for a larger plugin system later.
