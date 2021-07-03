"""Process the trades DataFrame into a consolidate portfolio."""
import pandas as pd
import yahooquery as yf
from portman import labels
from portman.trades import adjusted_volume


class Portfolio:
    """Creates portfolio object"""

    def __init__(self,
                 trades: pd.DataFrame,
                 portfolio_file: str = labels.PORTFOLIO_FILE):
        self.labels = labels
        self.portfolio = pd.DataFrame()
        self.trades = trades
        self.portfolio = self._net_position()
        self.portfolio = self._average_purchase_price()
        self.portfolio = self._average_purchase_price()
        self.portfolio = self._average_purchase_price()
        self.portfolio = self._current_price()
        self.portfolio = self._profit_and_loss()
        self.portfolio = self._market_value()
        self.portfolio = self._sector()
        self.portfolio.to_csv(portfolio_file)

    def _net_position(self) -> pd.DataFrame:
        """Compute net position from trades."""
        self.trades = adjusted_volume(self.trades)
        self.portfolio[self.labels.SHARES] = self.trades.groupby(self.labels.TICKER)[
            self.labels.ADJUSTED_VOL
        ].sum()
        return self.portfolio

    def _average_purchase_price(self) -> pd.DataFrame:
        """Compute average purchase price of an asset and adds new column."""
        # naive, simple, implementation, just sum total and divide by net position
        self.portfolio[self.labels.AVG_PRICE] = (
            self.trades.groupby("ticker")[self.labels.TOTAL].sum()
            / self.portfolio[self.labels.SHARES]
        )
        # remove net 0 positions
        self.portfolio = self.portfolio[self.portfolio[self.labels.SHARES] != 0]
        return self.portfolio

    def _current_price(self) -> pd.DataFrame:
        """Get current price from Yahoo finance and add a column to summary."""
        self.portfolio[self.labels.MARKET_PRICE] = self.portfolio.apply(
            lambda x: yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"], axis=1
        )
        return self.portfolio

    def _profit_and_loss(self) -> pd.DataFrame:
        """Compute profit and loss and adds a column to summary."""
        self.portfolio[self.labels.PL] = (
            (
                self.portfolio[self.labels.MARKET_PRICE]
                - self.portfolio[self.labels.AVG_PRICE]
            )
            / self.portfolio[self.labels.AVG_PRICE]
            * 100
        )
        return self.portfolio

    def _market_value(self) -> pd.DataFrame:
        """Compute current value and add column to summary."""
        self.portfolio[self.labels.MARKET_VALUE] = (
            self.portfolio[self.labels.MARKET_PRICE] * self.portfolio[self.labels.SHARES]
        )
        return self.portfolio

    def _sector(self) -> pd.DataFrame:
        """Get asset business sector"""
        self.portfolio[self.labels.SECTOR] = self.portfolio.apply(
            lambda x: yf.Ticker(x.name).asset_profile[x.name]["sector"],
            axis=1,
        )
        return self.portfolio

