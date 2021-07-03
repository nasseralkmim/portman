"""Example to create a processed portfolio"""
import portman.trades
from portman.portfolio import Portfolio
import pandas as pd
pd.set_option('display.max_columns', None)

trades = portman.trades.process("trade_data.csv")
# print(trades)
# por = portman.portfolio.process(trades)
# print(por)
portfolio = Portfolio(trades)
print(portfolio.summary)

