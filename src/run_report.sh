#!/bin/zsh

# Financial Report Generator
# This script generates a financial report and displays it in a window

# Configuration
readonly SCRIPT_DIR="${${(%):-%x}:A:h}"
readonly PROJECT_DIR="${SCRIPT_DIR:h}"
readonly LEDGER_CONFIG_FILE="${PROJECT_DIR}/config/ledger_path.conf"
readonly VENV_CONFIG_FILE="${PROJECT_DIR}/config/venv_path.conf"
readonly PYTHON_SCRIPT="${SCRIPT_DIR}/main.py"

# Function to raise an error in MacOS
raise_error() {
    osascript -e "display dialog \"$1\" buttons {\"OK\"} default button \"OK\" with icon stop"
}

# Function to load ledger file path from config
load_ledger_path() {
    if [ -f "$LEDGER_CONFIG_FILE" ]; then
        cat "$LEDGER_CONFIG_FILE"
    else
	raise_error "Ledger file not found.\n\nSpecify file name in /config/ledger_path.conf"
	exit 1
    fi
}

# Function to load venv path from config
load_venv_path() {
    if [ -f "$VENV_CONFIG_FILE" ]; then
        local venv_path=$(cat "$VENV_CONFIG_FILE")
	# Check to see if path exists, default is system python
	if [ -f "$venv_path" ]; then
	    echo "$venv_path"
	else
	    echo "python3"
	fi
    else
	echo "python3"
    fi
}

# Load venv path from config
PYTHON_CMD=$(load_venv_path)

# Check if ledger is installed
if ! command -v ledger &> /dev/null; then
    raise_error "Error: ledger command not found. Please install ledger-cli first:\n\nbrew install ledger"
    exit 1
fi

# Load previously saved ledger file path
LEDGER_FILE=$(load_ledger_path)

# Check if ledger file exists
if [ ! -f "$LEDGER_FILE" ]; then
    raise_error "Ledger file not found.\n\nPlease configure the file path of the ledger in /config/ledger_path.conf"
    exit 1
fi

# Check if required Python packages are installed
"$PYTHON_CMD" -c "import numpy, matplotlib, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    raise_error "Error: Required Python packages not found.\n\nPlease install:\npip3 install numpy matplotlib pillow"
    exit 1
fi

# Run the Python script
"$PYTHON_CMD" "$PYTHON_SCRIPT" "$LEDGER_FILE" 2>&1

# Check exit code
if [ $? -eq 0 ]; then
    # Success notification will be implicit as window appears
    exit 0
else
    raise_error "Error generating report. Check terminal for details."
    exit 1
fi
