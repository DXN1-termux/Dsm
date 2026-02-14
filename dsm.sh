#!/data/data/com.termux/files/usr/bin/bash

# --- DESIGN AGENTS: UI Theme & Branding ---
G='\033[0;32m' # Green
B='\033[0;34m' # Blue
C='\033[0;36m' # Cyan
R='\033[0;31m' # Red
NC='\033[0m'   # No Color

# --- SECURITY AGENTS: Login Logic ---
clear
echo -e "${B}======================================${NC}"
echo -e "${B}       DSM SECURITY CHECKPOINT        ${NC}"
echo -e "${B}======================================${NC}"

# Default Password
PASS="admin123"

read -sp "Enter DSM Password: " input_pass
echo -e "\n"

if [ "$input_pass" != "$PASS" ]; then
    echo -e "${R}[!] Access Denied: Incorrect Password.${NC}"
    exit 1
fi

echo -e "${G}[+] Access Granted. Loading DSM...${NC}"
sleep 1

# --- CORE SCRIPTING AGENTS: Persistent Menu ---
while true; do
    clear
echo -e "${G}======================================${NC}"
echo -e "${B}      DANI-STORAGE-MANAGER (DSM)      ${NC}"
echo -e "${G}======================================${NC}"
echo -e "${C}  [1]${NC} Update System Resources"
echo -e "${C}  [2]${NC} List Storage Files"
echo -e "${C}  [3]${NC} Check Disk Usage"
echo -e "${C}  [4]${NC} Network Quick-Scan (Nmap)"
echo -e "${C}  [5]${NC} Check System IP Info"
echo -e "${R}  [6]  Exit DSM${NC}"
echo -e "${G}======================================${NC}"
    
    read -p " DSM Select [1-6]: " choice

    case $choice in
        1)
            echo -e "${B}[+] Running System Updates...${NC}"
            pkg update && pkg upgrade -y
            ;;
        2)
            echo -e "${B}[+] Listing Files:${NC}"
            ls -p --color=auto
            ;;
        3)
            echo -e "${B}[+] Disk Space Analysis:${NC}"
            df -h
            ;;
        4)
            read -p "Enter Target (IP/Domain): " target
            echo -e "${C}Scanning $target...${NC}"
            nmap -F "$target"
            ;;
        5)
            echo -e "${C}Local IP:${NC} $(ifconfig | grep 'inet ' | awk '{print $2}' | head -n 1)"
            echo -e "${C}Public IP:${NC} $(curl -s ifconfig.me)"
            ;;
        6)
            echo -e "${R}Exiting DSM...${NC}"
            break
            ;;
        *)
            echo -e "${R}Invalid Option.${NC}"
            ;;
    esac

    # --- CHECK AGENTS: Output Pause ---
echo -e "\n${G}Press [Enter] to return to menu...${NC}"
    read
done
