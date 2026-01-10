import os
import subprocess
import datetime as dt

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Get absolute path to the style sheet relative to this file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_SHEET = os.path.join(
    os.path.dirname(SCRIPT_DIR), 'config', 'default_chart.mplstyle'
)


def _parse_ledger_command(command):
    """Execute a ledger command and return decoded output."""
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Check if command succeeded
    if result.returncode != 0:
        raise RuntimeError(
            f"Ledger command failed with exit code {result.returncode}. "
            f"Please check your ledger file syntax."
        )

    # Validate we have output
    if not result.stdout:
        raise ValueError(
            "Ledger command returned no data. "
            "Please verify your ledger file contains valid transactions."
        )

    # Parse output
    result = result.stdout.replace('$', '').replace(',', '').split(';')
    result = [x for x in result if x]

    if not result:
        raise ValueError(
            "Ledger command returned empty data. "
            "Please verify your ledger file has matching transactions."
        )

    return result


def _get_year_ago_date():
    """Return date string for one year ago in ledger format."""
    today = dt.datetime.today()
    return f'{today.year - 1}/{today.month}/{today.day}'


def get_net_worth_data(filename):
    """Returns a list of dates and net worths over time."""
    command = [
        'ledger', '-f', filename, 'reg', 'assets', 'liabilities',
        '--weekly', '-V', '-n', '-F', '%(date);%(T);'
    ]

    data = _parse_ledger_command(command)

    dates = np.array(data[::2])
    amounts = np.array(data[1::2]).astype(float)

    return dates, amounts


def gen_net_worth_graph(filename):
    """Generates a graph displaying net worth over time."""
    dates, amounts = get_net_worth_data(filename)
    x_vals = [dt.datetime.strptime(d, '%Y/%m/%d').date() for d in dates]
    amounts_k = amounts / 1000

    mpl.style.use(STYLE_SHEET)
    fig, ax = plt.subplots()

    ax.plot(x_vals, amounts_k)
    ax.fill_between(x_vals, amounts_k, alpha=0.15)

    ax.set_xlabel('Time')
    ax.set_ylabel('Net Worth ($K)')
    ax.set_ylim(0, np.max(amounts_k) * 1.1)
    ax.xaxis.set_major_locator(mpl.dates.YearLocator())
    ax.xaxis.set_minor_locator(mpl.dates.MonthLocator(list(range(1, 13))))
    
    return fig


def get_expenses_data(filename):
    """Returns a dict of expense accounts and their balances in thousands."""
    command = [
        'ledger', '-f', filename, 'bal', 'expenses', '--flat', '-F',
        '%(T);%(account);'
    ]

    data = _parse_ledger_command(command)

    amounts = np.array(data[::2]).astype(float) / 1000
    accounts = [entry.split(':')[1:] for entry in data[1::2]]

    # Aggregate by top-level expense category
    accounts_struct = {}
    for i, entry in enumerate(accounts):
        category = entry[0]
        accounts_struct[category] = accounts_struct.get(category, 0) + amounts[i]

    return accounts_struct


def gen_expenses_bar_chart(filename):
    """Generates a horizontal bar chart of expense categories."""
    breakdown = get_expenses_data(filename)
    labels = [f'{name:.5}.' if len(name) > 5 else name
              for name in breakdown.keys()]
    values = list(breakdown.values())

    fig, ax = plt.subplots()
    bars = ax.barh(labels, values, height=0.5, alpha=0.85)

    for bar in bars:
        bar.set_edgecolor('white')
        bar.set_linewidth(0.5)

    ax.set_xlabel('Spending ($K)')

    return fig


def get_subscriptions(filename):
    """Returns lists of subscription names and amounts from the past year."""
    start_date = _get_year_ago_date()
    command = [
        'ledger', '-f', filename, 'reg', '-b', start_date,
        '--by-payee', '--format', '%P;%(abs(display_amount));',
        '%subscription'
    ]

    data = _parse_ledger_command(command)

    accounts = data[:-1:2]
    balances = [float(i) if i else 0.0 for i in data[1::2]]

    return accounts, balances


def get_top_expenses(filename):
    """Returns top N payees by expense amount from the past year."""
    PAYEE_NUM = 5
    
    start_date = _get_year_ago_date()
    command = [
        'ledger', '-f', filename, 'reg', '-b', start_date,
        '--by-payee', '-S', '-T', '--head', str(PAYEE_NUM),
        '--format', '%P;%(abs(display_amount));',
        '^Expenses'
    ]

    data = _parse_ledger_command(command)

    accounts = data[:-1:2]
    balances = [float(i) if i else 0.0 for i in data[1::2]]

    return accounts, balances


def get_savings_rate(filename):
    """Returns savings rate as percentage of income over the past year."""
    start_date = _get_year_ago_date()

    stats = {'income': 0, 'expenses': 0}
    for account in stats.keys():
        command = [
            'ledger', '-f', filename, 'reg', account,
            '-b', start_date, '-V', '-n', '-F', '%(date);%(T);'
        ]
        data = _parse_ledger_command(command)
        try:
            stats[account] = -float(data[-1])
        except (IndexError, ValueError):
            stats[account] = 0
            
    # Calculate the savings percent
    if stats['income'] == 0:
        return -np.inf

    savings_percent = int((stats['income'] + stats['expenses']) / stats['income'] * 100)
    
    return savings_percent

