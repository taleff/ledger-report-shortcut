# Ledger Report Shortcut

A visual dashboard for financial data stored using [ledger-cli](https://www.ledger-cli.org). This macOS application uses the Shortcuts app to quickly display your financial summary in a window.

![Example dashboard](/assets/example_dashboard.png?raw=true)

## Dependencies

- **Python 3.x** - Needed to run the application
- **ledger-cli** - Command line tool for storing and manipulating financial data
  - Install using Homebrew: `brew install ledger`

## Installation

Clone this repository to your computer:

```zsh
git clone https://github.com/taleff/ledger-report-shortcut.git
cd ledger-report-shortcut
```

I use a virtual environment to keep this application's dependencies separate from other Python projects.

```zsh
# Create the virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

Note the full path to your Python executable.

```zsh
which python3
```

This will show something like: `/Users/yourname/ledger-report-shortcut/.venv/bin/python3`

Create your configuration files from the provided examples:

```zsh
cp config/ledger_path.conf.example config/ledger_path.conf
cp config/venv_path.conf.example config/venv_path.conf
```

Now edit these files with your specific paths:

1. **Edit `config/ledger_path.conf`**
   - Replace the example path with the actual path to your ledger file
   - Example: `/Users/yourname/ledger.dat`

2. **Edit `config/venv_path.conf`**
   - Replace the example path with the Python path you found earlier
   - Example: `/Users/yourname/ledger-report-shortcut/.venv/bin/python3`

If you would like to attach this to a MacOS shortcut, paste the following into a "Run Shell Script" block.

```zsh
# Add Homebrew to path so ledger-cli can be found
PATH=$PATH:/opt/homebrew/bin

# Run the report generation script
source /Users/yourname/ledger-report-shortcut/src/run_report.sh
```
**Note**: If your Homebrew is installed in a different location, update the PATH line accordingly.

## How to Use

You can run the application directly from the terminal or use a shortcut using the script above.

```zsh
source src/run_report.sh
```

Edit your ledger file as normal. When adding subscriptions, add a subscription tag to the ledger entry.

```zsh
2026/02/11 Example Payee
    Expenses:Example			$5.00
    Liabilities:Credit Card
    ; :subscription:
```

## Future Enhancements

- [ ] Automated bank statement scraping and ledger entry creation
- [ ] Savings trend analysis for recent months
