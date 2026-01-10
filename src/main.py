import os
import sys
import customtkinter as ctk
from window import ReportApp


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Error: No ledger file specified\n")
        sys.stderr.write("Usage: main.py <ledger_file>\n")
        sys.exit(1)

    filename = sys.argv[1]

    # Resolve symlinks to actual file path
    try:
        filename = os.path.realpath(filename)
    except (OSError, ValueError) as e:
        sys.stderr.write(f"Error: Invalid file path: {e}\n")
        sys.exit(1)

    # Validate file exists and is a regular file
    if not os.path.exists(filename):
        sys.stderr.write(f"Error: File does not exist: {filename}\n")
        sys.exit(1)

    if not os.path.isfile(filename):
        sys.stderr.write(f"Error: Path is not a regular file: {filename}\n")
        sys.exit(1)

    # Check file is readable
    if not os.access(filename, os.R_OK):
        sys.stderr.write(f"Error: File is not readable: {filename}\n")
        sys.exit(1)

    # Create main window
    app = ReportApp(filename)
    app.mainloop()


if __name__ == '__main__':
    main()
    
