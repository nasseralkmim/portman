import matplotlib.pyplot  as plt
import portman.portvis.portfolio
import portman.labels
from portman.portfolio import Portfolio
import portman.trades
import pandas as pd
pd.set_option('display.max_columns', None)

trades = portman.trades.process("trade_data.csv")
port = Portfolio(trades, 'simple_portfolio.csv')
print(port.portfolio)
