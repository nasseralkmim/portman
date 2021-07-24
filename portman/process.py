"""Process the trades data and generate a '.csv' with portfolio processed


Example:
        $python -m portman.process "trades_file(s).csv"

"""
import argparse

import portman.portfolio
import portman.trades

parser = argparse.ArgumentParser(description='Consolidate trade data.')
parser.add_argument('trades',
                    help='`.csv` files with trade data',
                    nargs='+')
args = parser.parse_args()
trades_file = args.trades

for tf in trades_file:
    trades = portman.trades.Trades(trades_file=tf)
    port = portman.portfolio.Portfolio(trades, 'portfolio.csv')
