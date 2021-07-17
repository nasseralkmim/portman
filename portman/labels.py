"""Define string labels for DataFrames columns and for plotting."""
from dataclasses import dataclass

@dataclass
class Labels:
    """Define labels."""
    AVG_PRICE: str = "average price ($)"  # average purchase price of an asset
    PL: str = "P/L %"  # profit and loss in a position
    MARKET_PRICE: str = "market price ($)"  # current price
    MARKET_VALUE: str = "market value ($)"  # current value of a position
    SECTOR: str = "sector"  # asset business sector
    DATE: str = "date"
    TYPE: str = "type"  # buy, sell, split from the trade data
    TICKER: str = "ticker"
    SHARES: str = "shares"
    ADJUSTED_VOL: str = "volume adjusted"  # adjusted volume based on type
    PURCHASE_PRICE: str = "purchase price"
    TOTAL: str = "total"
    FEE: str = "fee"
    BUY: str = "Buy"
    SELL: str = "Sell"
    SPLIT: str = "Split"

    def set_label(self, **kwarg: str) -> None:
        """Change or add new label."""
        self.__dict__.update(kwarg)
