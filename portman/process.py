"""Process the trades data and generate a '.csv' with portfolio processed


Example:
        $python -m portman.process "trades_data.py"

"""
import argparse

import portman.portfolio
import portman.trades

# TODO add multiple "trade_file" with asset class
parser = argparse.ArgumentParser(description='Get trades .csv data')
parser.add_argument('trades')
args = parser.parse_args()
trades_file = args.trades
# TODO changed to class.
# trades = portman.trades.process(trades_file)
# portman.portfolio.process(trades)
