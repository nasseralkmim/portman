"""Example to create a processed portfolio"""
import matplotlib.pyplot  as plt
import portman.portvis.portfolio
import portman.labels
from portman.portfolio import Portfolio
import portman.trades
import pandas as pd
pd.set_option('display.max_columns', None)

trades = portman.trades.process("trade_data.csv")
trades = portman.trades.process("acoes.csv")
portfolio = Portfolio(trades, 'acoes_portfolio.csv')
print(portfolio.portfolio)
