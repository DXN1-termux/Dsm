# Installation

## Termux

```bash
pkg update && pkg upgrade -y
pkg install python nmap -y
pip install -r requirements.txt
chmod +x dsm.sh
./dsm.sh
```

## Linux

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```
