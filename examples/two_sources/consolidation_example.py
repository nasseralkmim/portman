import portman.labels
import portman.trades
import portman.portfolio
import pandas as pd

pd.set_option('display.max_columns', None)

stocks_trades = portman.trades.Trades('stocks.csv')
etf_trades = portman.trades.Trades('etf.csv')
etfs = portman.portfolio.Portfolio(etf_trades)
stocks = portman.portfolio.Portfolio(stocks_trades) 

print(etfs.summary)
print(stocks.summary)
