<div align="center">

# ⚡ DXN1 STORAGE MANAGER
### The Universal System & File Intelligence Suite.

<br />

**MADE WITH ❤️ BY [DXN1](https://github.com/DXN1-termux)**

<br />

[![Version](https://img.shields.io/badge/VERSION-3.0.0--ULTIMATE-00FF00?style=for-the-badge&logo=semantic-release&logoColor=white)](https://github.com/DXN1-termux/Dsm) &nbsp;&nbsp; [![Language](https://img.shields.io/badge/TECH-PYTHON--%7C--BASH-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/DXN1-termux/Dsm) &nbsp;&nbsp; [![License](https://img.shields.io/badge/LICENSE-MIT-blueviolet?style=for-the-badge)](LICENSE)
<br />
[![Platform](https://img.shields.io/badge/PLATFORM-CROSS--PLATFORM-orange?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/DXN1-termux/Dsm) &nbsp;&nbsp; [![Architecture](https://img.shields.io/badge/ARCHITECTURE-MODULAR--AGENT-gold?style=for-the-badge&logo=dependencygraph&logoColor=white)](https://github.com/DXN1-termux/Dsm) &nbsp;&nbsp; [![Security](https://img.shields.io/badge/SECURITY-ENTERPRISE--GRADE-red?style=for-the-badge&logo=securityscorecard&logoColor=white)](https://github.com/DXN1-termux/Dsm)
<br />
[![System](https://img.shields.io/badge/SYSTEM-DASHBOARD-brightgreen?style=for-the-badge&logo=statuspage&logoColor=white)](#-features) &nbsp;&nbsp; [![Storage](https://img.shields.io/badge/STORAGE-DEEP--CLEANER-blue?style=for-the-badge&logo=files&logoColor=white)](#-features) &nbsp;&nbsp; [![Network](https://img.shields.io/badge/NETWORK-THREAT--SCANNER-informational?style=for-the-badge&logo=nmap&logoColor=white)](#-features)

---

</div>

## 🔐 Security Notice
Default Password: `admin123` 🤫

## 🚀 Welcome to DSM 3.0
**DSM (DXN1 Storage Manager)** has evolved. It is no longer just a Termux utility; it is a **universal system intelligence suite** built for Linux, macOS, WSL, and Termux. Powered by a high-performance Python modular agent architecture, DSM 3.0 provides the ultimate control interface for power users.

## 🌟 Why DSM 3.0? (The 20x Difference)
- **Universal Engine:** Now detects your environment (Termux, Linux, macOS, WSL) and optimizes performance dynamically.
- **Agent Architecture:** Everything is a decoupled "Agent" (Security, Storage, Network, System). Extend it easily.
- **Deep Storage Analysis:** Beyond listing files, DSM 3.0 now identifies junk, duplicates, and massive files across your entire filesystem.
- **Threat-Aware Networking:** Advanced Nmap integration with automated service identification and vulnerability scanning.
- **Visual Intelligence:** Generate instant SVG disk reports and performance heatmaps.

## 📊 Features Deep-Dive

### 🖥️ 1. Hyper-System Monitoring
The DSM Dashboard monitors your system's heartbeat in real-time.
*   **CPU/RAM/Disk/Battery:** High-precision data acquisition using `psutil`.
*   **Multi-Core Awareness:** Get detailed insights into logical and physical thread utilization.
*   **Performance Heatmaps:** Visual output for load analysis.

### 📁 2. Deep Storage Cleaner
Manage your data with military-grade precision.
*   **Recursive Analysis:** Scans every directory branch for bloat.
*   **Massive File Finder:** Identify the top 100 files eating your storage in milliseconds.
*   **SVG Reporting:** Generate beautiful visual disk usage reports.

### 🌐 3. Network Intelligence Suite
Go beyond simple Pings.
*   **Automated Recon:** Automated service detection for target IPs/Domains.
*   **IP Intelligence:** Track global reachability and local networking metadata.
*   **Vulnerability Scanning:** Built-in hooks for Nmap-based security posture testing.

### 🛡️ 4. Enterprise-Grade Security
Your system is your fort.
*   **Auth Vault:** Password-gated sessions that protect your workspace.
*   **Config Isolation:** All settings are stored securely away from the main binary.
*   **Encrypted Hooks:** Future-ready hooks for encrypted history logging.

## 📊 Version Comparison (The Evolution)
Witness the transition from a simple storage utility to an industrial-grade system intelligence suite.

| Feature | v1.0 (Legacy) | v3.0 (Ultimate) |
| :--- | :--- | :--- |
| **Engine** | Single Bash Script | Modular Python Agent-Core |
| **UI** | Basic Echo Menu | Rich-Powered Professional TUI |
| **System Visibility** | Text-based stats | Real-time SVG & Heatmaps |
| **Platform Support** | Termux Only | Universal (Linux/macOS/WSL/Termux) |
| **Network** | Basic Ping/Nmap | Advanced Recon & Intelligence |
| **Architecture** | Spagetti Code | Decoupled Agent-Pattern |

## 📦 Release History (3.0.0-Ultimate)
- **v3.0.0:** Complete architecture overhaul, multi-platform support, SVG visual reports, agent-modularization, and enterprise-grade security.
- **v2.5.0:** Integration of visual SVG disk analysis and dashboard refinement.
- **v1.0.0:** The original bash-based tool—the humble beginning of a powerful project.

---

## 🛠️ Multi-Platform Installation

### Quick Start (All Platforms)
```bash
git clone https://github.com/DXN1-termux/Dsm.git && cd Dsm && chmod +x dsm.sh && ./dsm.sh
```

### Manual Installation
1.  **Dependencies:** Ensure `python 3.10+` and `pip` are installed.
2.  **Environment:** `pip install -r requirements.txt`
3.  **Launch:** `python3 main.py`

## 🏗️ Technical Architecture
DSM 3.0 is built on the **Modular Agent** pattern:
- **`dsm.sh`**: The bootstrap launcher. Detects environment, handles dependencies, launches engine.
- **`main.py`**: The Orchestrator. Handles UI logic and TUI state.
- **`src/`**: The Agent Layer.
    - `security.py`: Auth & Protection logic.
    - `storage.py`: Filesystem analytics & cleaning.
    - `system.py`: Resource monitoring & performance.
    - `network.py`: Recon & Intelligence.
- **`requirements.txt`**: Managed dependency chain.

## 📝 Roadmap
- [ ] Cross-platform GUI Dashboard (via Kivy).
- [ ] Cloud-syncing for configuration files.
- [ ] NeuralShell API integration for conversational shell help.
- [ ] Automated system repair modules.

## 🤝 Contribution Guidelines
DSM is built for performance. Contributions should:
1.  Follow the **Modular Agent** pattern.
2.  Be fully type-hinted and test-backed.
3.  Minimize external dependencies.

---

<div align="center">
  <b>DXN1-termux © 2026</b>
</div>
