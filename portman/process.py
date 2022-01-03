"""This modulue performs the processing with a command line interface

The processing consists of reading the trades files passed as arguments and
generating the portfolio with the consolidated data.

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

trades = []
for tf in trades_file:
    trades.append(portman.trades.Trades(trades_file=tf))

port = portman.portfolio.Portfolio(trades)
