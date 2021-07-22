import portman.labels
import portman.trades
import portman.portfolio
import pandas as pd

pd.set_option('display.max_columns', None)

stocks_trades = portman.trades.Trades('stocks.csv')
etf_trades = portman.trades.Trades('etf.csv')
portfolio = portman.portfolio.Portfolio([etf_trades, stocks_trades])

print(portfolio.summary)
