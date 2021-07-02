"""Labels for DataFrames

Centralize labels for columns in data frames
"""

AVG_PRICE = 'average price ($)'           # average purchase price of an asset
PL = 'P/L %'                    # profit and loss in a position
MARKET_PRICE = 'market price ($)'             # current price
MARKET_VALUE = 'market value ($)' # current value of a position
SECTOR = 'sector'               # asset business sector

PORTFOLIO_FILE = 'portfolio.csv'
TRADES_FILE = 'trades.csv'      # processed trades files

DATE = 'date'
TYPE = 'type'                   # buy, sell, split from the trade data
TICKER = 'ticker'
SHARES = 'shares'
ADJUSTED_VOL = 'volume adjusted'      # adjusted volume based on type 
PURCHASE_PRICE = 'purchase price'
TOTAL = 'total'
FEE = 'fee'

BUY = 'Buy'
SELL = 'Sell'
SPLIT = 'Split'
