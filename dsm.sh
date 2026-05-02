#!/data/data/com.termux/files/usr/bin/bash

# --- DSM 2.0 Launcher ---
# High-speed bootstrap for the Python-powered Storage Manager

RESET='\033[0m'
BOLD='\033[1m'
BLUE='\033[38;5;33m'
CYAN='\033[38;5;51m'
GREEN='\033[38;5;82m'
RED='\033[38;5;196m'

_print() { printf "${GREEN}⚡${RESET} %s\n" "$*"; }
_error() { printf "${RED}✗${RESET}  %s\n" "$*" >&2; exit 1; }

clear
printf "${BLUE}${BOLD}"
cat << 'EOF'
  ____  ____  __  __ 
 |  _ \/ ___||  \/  |
 | | | \___ \| |\/| |
 | |_| |___) | |  | |
 |____/|____/|_|  |_|
EOF
printf "${RESET}${CYAN}  Dani Storage Manager v2.0${RESET}\n\n"

# 1. Environment Check
_print "Verifying environment..."
if ! command -v python3 &>/dev/null; then
    _error "Python 3 is required. Run: pkg install python"
fi

# 2. Dependency Check (Auto-install missing)
if [[ ! -d "venv" ]]; then
    _print "Initializing core components..."
    python3 -m pip install -r requirements.txt --quiet || _print "Proceeding with existing packages..."
fi

# 3. Launch Engine
_print "Engaging Python Engine..."
exec python3 main.py "$@"
