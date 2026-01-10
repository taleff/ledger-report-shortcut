# Ledger Report Shortcut

A visual dashboard for financial data stored using [ledger-cli](https://www.ledger-cli.org). This macOS application uses the Shortcuts app to quickly display your financial summary in a window.

## What You'll Need

- **macOS** - Required to use the Shortcuts app for launching the dashboard
- **Python 3.x** - Needed to run the application
- **ledger-cli** - The command-line tool that stores your financial data
  - Install using Homebrew: `brew install ledger`
  - Visit [brew.sh](https://brew.sh) to install homebrew if you don't have it already

## Installation

### Step 1: Download the Code

Clone this repository to your computer:

```zsh
git clone https://github.com/taleff/ledger-report-shortcut.git
cd ledger-report-shortcut
```

### Step 2: Install Python Dependencies

A virtual environment keeps this application's dependencies separate from other Python projects on your computer.

```zsh
# Create the virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

**Important**: After installation, note the full path to your Python executable. You'll need this in Step 4. To find it, run:

```zsh
which python3
```

This will show something like: `/Users/yourname/ledger-report-shortcut/.venv/bin/python3`

### Step 3: Configure the Application

Create your configuration files from the provided examples:

```zsh
cp config/ledger_path.conf.example config/ledger_path.conf
cp config/venv_path.conf.example config/venv_path.conf
```

Now edit these files with your specific paths:

1. **Edit `config/ledger_path.conf`**
   - Open the file in a text editor
   - Replace the example path with the actual path to your ledger file
   - Example: `/Users/yourname/ledger.dat`

2. **Edit `config/venv_path.conf`**
   - Replace the example path with the Python path you noted in Step 2
   - Example: `/Users/yourname/ledger-report-shortcut/.venv/bin/python3`

### Step 4: Create the macOS Shortcut

1. Open the **Shortcuts** app on your Mac (found in Applications or via Spotlight)
2. Click the **+** button to create a new shortcut
3. Search for "Run Shell Script" and add that action
4. Paste the following code into the script box:

```zsh
# Add Homebrew to path so ledger-cli can be found
PATH=$PATH:/opt/homebrew/bin

# Run the report generation script
source /Users/yourname/ledger-report-shortcut/src/run_report.sh
```

5. **Important**: Replace `/Users/yourname/ledger-report-shortcut` with the actual path where you cloned this repository

6. Name your shortcut (e.g., "Financial Report")
7. (Optional) Right-click the shortcut and select "Add to Dock" for easy access

**Note**: If your Homebrew is installed in a different location, update the PATH line accordingly.

## How to Use

### Running the Dashboard

Simply click your Shortcut in the Dock or run it from the Shortcuts app. A window will appear showing your financial summary with charts and data.

### Running from Command Line

You can also run the application directly from the terminal:

```bash
source src/run_report.sh
```

## Project Structure

```
.
├── config/           # Your configuration files (paths to ledger and Python)
├── src/              # Application source code
├── test/             # Sample ledger file for testing
└── requirements.txt  # List of required Python packages
```

## Built With

- [ledger-cli](https://www.ledger-cli.org/) - Double-entry accounting system
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI framework
- [Matplotlib](https://matplotlib.org/) - Data visualization

## Future Enhancements

- [ ] Automated bank statement scraping and ledger entry creation
- [ ] Savings trend analysis for recent months

## License

[Choose and specify license]
