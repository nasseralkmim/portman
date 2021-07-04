import portman.labels
import portman.trades
import portman.portfolio
import pandas as pd
pd.set_option('display.max_columns', None)

labels = portman.labels.Labels()
trades = portman.trades.Trades('trade_data.csv',
                               columns=[labels.DATE,
                                        labels.TYPE,
                                        labels.TICKER,
                                        labels.SHARES,
                                        labels.PURCHASE_PRICE,
                                        labels.FEE],
                               date_column=labels.DATE,
                               labels=labels)
print(trades.history.dtypes)
print(trades.history)
port = portman.portfolio.Portfolio(trades, 'simple_portfolio.csv')
print(port.portfolio)
