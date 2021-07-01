"""Process the trades data and generate a '.csv' with portfolio processed


Example:
        $python -m portman.process "trades_data.py"

"""
import argparse

import portman.portfolio
import portman.trades

parser = argparse.ArgumentParser(description='Get trades .csv data')
parser.add_argument('trades')
args = parser.parse_args()
trades_file = args.trades
trades = portman.trades.process(trades_file)
portman.portfolio.process(trades)
