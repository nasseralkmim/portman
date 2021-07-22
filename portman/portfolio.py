"""Process the trades DataFrame into a consolidate portfolio."""
import warnings
import pandas as pd
import numpy as np
import yahooquery as yf

from portman.trades import Trades


class Portfolio:
    """Creates portfolio object."""

    def __init__(self, trades: Trades,
                 portfolio_file: str = "portfolio.csv") -> None:
        self.labels = trades.labels  # aggregation of Labels object

        self.trades = trades  # aggregation of Trades object

        self.portfolio = pd.DataFrame()
        self.portfolio[self.labels.SHARES] = self._compute_net_shares()
        self.portfolio[self.labels.AVG_PRICE] = self._compute_average_purchase_price()
        # remove net 0 positions
        self.portfolio = self.portfolio[self.portfolio[self.labels.SHARES] != 0]
        self.portfolio[self.labels.MARKET_PRICE] = self._get_current_price()
        self.portfolio[self.labels.PL] = self._compute_profit_and_loss()
        self.portfolio[self.labels.MARKET_VALUE] = self._compute_market_value()
        self.portfolio[self.labels.SECTOR] = self._get_sector()
        self.portfolio[self.labels.NAME] = self._get_long_name()
        self.portfolio[self.labels.CURRENCY] = self._get_currency()
        self.portfolio[self.labels.ASSET_CLASS] = self.trades.asset_class
        self.portfolio.to_csv(portfolio_file)

    def _compute_net_shares(self) -> pd.DataFrame:
        """Computes net position from trades."""
        # adjust volume based on type
        self.trades.history = self.trades.adjusted_volume()
        net_shares = self.trades.history.groupby(self.labels.TICKER)[
            self.labels.ADJUSTED_VOL
        ].sum()
        return net_shares

    def _compute_average_purchase_price(self) -> pd.DataFrame:
        """Computes average purchase price of assets."""
        # sum total and divide by net position
        avg_price = (
            self.trades.history.groupby("ticker")[self.labels.TOTAL].sum()
            / self.portfolio[self.labels.SHARES]
        )
        return avg_price

    def _compute_profit_and_loss(self) -> pd.DataFrame:
        """Computes profit or loss from market price."""
        profit_loss = (
            (
                self.portfolio[self.labels.MARKET_PRICE]
                - self.portfolio[self.labels.AVG_PRICE]
            )
            / self.portfolio[self.labels.AVG_PRICE]
            * 100
        )
        return profit_loss

    def _compute_market_value(self) -> pd.DataFrame:
        """Compute current value from number of shares and market price."""
        market_value = (
            self.portfolio[self.labels.MARKET_PRICE]
            * self.portfolio[self.labels.SHARES]
        )
        return market_value

    def _get_current_price(self) -> pd.DataFrame:
        """Get current price from Yahoo finance."""

        def yahoo_market_price(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"]
            except (KeyError, TypeError):
                warnings.warn(
                    f"Quote not found for ticker symbol: {x.name}"
                )
                return np.nan

        market_price = self.portfolio.apply(lambda x: yahoo_market_price(x), axis=1)

        return market_price

    def _get_sector(self) -> pd.DataFrame:
        """Get assets business sector from Yahoo finance."""

        def yahoo_sector(x):
            try:
                return yf.Ticker(x.name).asset_profile[x.name]["sector"]
            except (KeyError, TypeError):
                return np.nan

        sector = self.portfolio.apply(
            lambda x: yahoo_sector(x),
            axis=1)
        return sector

    def _get_long_name(self) -> pd.DataFrame:
        """Get long name of security from Yahoo finance."""

        def yahoo_long_name(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["longName"]
            except (KeyError, TypeError):
                return np.nan

        long_name = self.portfolio.apply(
            lambda x: yahoo_long_name(x),
            axis=1)
        return long_name

    def _get_currency(self) -> pd.DataFrame:
        """Get currency of security from Yahoo finance."""

        def yahoo_currency(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["currency"]
            except (KeyError, TypeError):
                return np.nan

        currency = self.portfolio.apply(
            lambda x: yahoo_currency(x),
            axis=1)
                
        return currency
