"""Process the trades data and generate a '.csv' with portfolio processed


Example:
        $python -m portman.process "trades_file(s).csv"

"""
import argparse

import portman.portfolio
import portman.trades

parser = argparse.ArgumentParser(description='Get trades .csv data')
parser.add_argument('trades')
args = parser.parse_args()
trades_file = args.trades

trades = portman.trades.Trades(trades_file=trades_file)
port = portman.portfolio.Portfolio(trades, f'portfolio_{trades_file}')
