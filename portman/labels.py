"""Define string labels for DataFrames columns and for plotting."""


class Labels:
    """Define labels."""
    def __init__(self):
        self.AVG_PRICE = "average price ($)"  # average purchase price of an asset
        self.PL = "P/L %"  # profit and loss in a position
        self.MARKET_PRICE = "market price ($)"  # current price
        self.MARKET_VALUE = "market value ($)"  # current value of a position
        self.SECTOR = "sector"  # asset business sector
        self.DATE = "date"
        self.TYPE = "type"  # buy, sell, split from the trade data
        self.TICKER = "ticker"
        self.SHARES = "shares"
        self.ADJUSTED_VOL = "volume adjusted"  # adjusted volume based on type
        self.PURCHASE_PRICE = "purchase price"
        self.TOTAL = "total"
        self.FEE = "fee"
        self.BUY = "Buy"
        self.SELL = "Sell"
        self.SPLIT = "Split"

    def set_label(self, **kwarg: str) -> None:
        """Change or add new label."""
        self.__dict__.update(kwarg)
