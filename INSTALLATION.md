# Installation Instructions

## Prerequisites
- Ensure you have Termux installed on your mobile device.
- Make sure your device has internet access.

## Installation Steps
1. **Update package list:**
   ```bash
   pkg update
   ```
2. **Install required packages:**
   ```bash
   pkg install git
   pkg install python
   pkg install python-dev
   pkg install clang
   ```
3. **Clone the repository:**
   ```bash
   git clone https://github.com/DXN1-termux/dsm.git
   ```
4. **Navigate to the project directory:**
   ```bash
   cd dsm
   ```
5. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Run the application:**
   ```bash
   python app.py
   ```

## Additional Setup
- Follow any further configuration instructions provided in the project documentation.

## Troubleshooting
- If you encounter issues, please refer to the GitHub issues page or open a new issue for assistance.