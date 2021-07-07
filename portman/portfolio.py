"""Process the trades DataFrame into a consolidate portfolio."""
import pandas as pd
import yahooquery as yf

from portman.trades import Trades


class Portfolio:
    """Creates portfolio object"""

    def __init__(self, trades: Trades, portfolio_file: str = "portfolio.csv"):
        self.labels = trades.labels  # aggregation of Labels object

        self.trades = trades  # aggregation of Trades object
        # adjust volume based on type
        self.trades.history = self.trades.adjusted_volume()

        self.portfolio = pd.DataFrame()
        self.portfolio = self._net_position()
        self.portfolio = self._average_purchase_price()
        self.portfolio = self._current_price()
        self.portfolio = self._profit_and_loss()
        self.portfolio = self._market_value()
        self.portfolio = self._sector()
        self.portfolio.to_csv(portfolio_file)

    def _net_position(self) -> pd.DataFrame:
        """Computes net position from trades and adds column."""
        self.portfolio[self.labels.SHARES] = self.trades.history.groupby(
            self.labels.TICKER
        )[self.labels.ADJUSTED_VOL].sum()
        return self.portfolio

    def _average_purchase_price(self) -> pd.DataFrame:
        """Computes average purchase price of assets and adds column."""
        # naive, simple, implementation, just sum total and divide by net position
        self.portfolio[self.labels.AVG_PRICE] = (
            self.trades.history.groupby("ticker")[self.labels.TOTAL].sum()
            / self.portfolio[self.labels.SHARES]
        )
        # remove net 0 positions
        self.portfolio = self.portfolio[self.portfolio[self.labels.SHARES] != 0]
        return self.portfolio

    def _current_price(self) -> pd.DataFrame:
        """Get current price from Yahoo finance and adds column."""
        self.portfolio[self.labels.MARKET_PRICE] = self.portfolio.apply(
            lambda x: yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"], axis=1
        )
        return self.portfolio

    def _profit_and_loss(self) -> pd.DataFrame:
        """Computes profit and loss and adds column."""
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
            self.portfolio[self.labels.MARKET_PRICE]
            * self.portfolio[self.labels.SHARES]
        )
        return self.portfolio

    def _sector(self) -> pd.DataFrame:
        """Get assets business sector and adds column."""
        self.portfolio[self.labels.SECTOR] = self.portfolio.apply(
            lambda x: yf.Ticker(x.name).asset_profile[x.name]["sector"],
            axis=1,
        )
        return self.portfolio
