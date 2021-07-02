"""Example to create a processed portfolio"""
import portman.trades
import portman.portfolio
import pandas as pd
pd.set_option('display.max_columns', None)

trades = portman.trades.process("trade_data.csv")
por = portman.portfolio.process(trades)
print(trades)
print(por)

