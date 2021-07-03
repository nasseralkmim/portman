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
        self.summary = pd.DataFrame()
        self.trades = trades
        self.summary = self._net_position()
        self.summary = self._average_purchase_price()
        self.summary = self._average_purchase_price()
        self.summary = self._average_purchase_price()
        self.summary = self._current_price()
        self.summary = self._profit_and_loss()
        self.summary = self._market_value()
        self.summary = self._sector()
        self.summary.to_csv(portfolio_file)

    def _net_position(self) -> pd.DataFrame:
        """Compute net position from trades."""
        self.trades = adjusted_volume(self.trades)
        self.summary[self.labels.SHARES] = self.trades.groupby(self.labels.TICKER)[
            self.labels.ADJUSTED_VOL
        ].sum()
        return self.summary

    def _average_purchase_price(self) -> pd.DataFrame:
        """Compute average purchase price of an asset and adds new column."""
        # naive, simple, implementation, just sum total and divide by net position
        self.summary[self.labels.AVG_PRICE] = (
            self.trades.groupby("ticker")[self.labels.TOTAL].sum()
            / self.summary[self.labels.SHARES]
        )
        # remove net 0 positions
        self.summary = self.summary[self.summary[self.labels.SHARES] != 0]
        return self.summary

    def _current_price(self) -> pd.DataFrame:
        """Get current price from Yahoo finance and add a column to summary."""
        self.summary[self.labels.MARKET_PRICE] = self.summary.apply(
            lambda x: yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"], axis=1
        )
        return self.summary

    def _profit_and_loss(self) -> pd.DataFrame:
        """Compute profit and loss and adds a column to summary."""
        self.summary[self.labels.PL] = (
            (
                self.summary[self.labels.MARKET_PRICE]
                - self.summary[self.labels.AVG_PRICE]
            )
            / self.summary[self.labels.AVG_PRICE]
            * 100
        )
        return self.summary

    def _market_value(self) -> pd.DataFrame:
        """Compute current value and add column to summary."""
        self.summary[self.labels.MARKET_VALUE] = (
            self.summary[self.labels.MARKET_PRICE] * self.summary[self.labels.SHARES]
        )
        return self.summary

    def _sector(self) -> pd.DataFrame:
        """Get asset business sector"""
        self.summary[self.labels.SECTOR] = self.summary.apply(
            lambda x: yf.Ticker(x.name).asset_profile[x.name]["sector"],
            axis=1,
        )
        return self.summary

