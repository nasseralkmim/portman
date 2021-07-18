import portman.labels
import portman.trades
import portman.portfolio
import pandas as pd

pd.set_option("display.max_columns", None)

trades = portman.trades.Trades(
    trades_file="trade_data.csv",
)
print(trades.history)

port = portman.portfolio.Portfolio(trades, 'simple_portfolio.csv')
print(port.portfolio)
