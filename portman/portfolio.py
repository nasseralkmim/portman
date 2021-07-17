"""Process the trades DataFrame into a consolidate portfolio."""
import pandas as pd
import yahooquery as yf

from portman.trades import Trades


class Portfolio:
    """Creates portfolio object."""

    def __init__(self, trades: Trades, portfolio_file: str = "portfolio.csv"):
        self.labels = trades.labels  # aggregation of Labels object

        self.trades = trades  # aggregation of Trades object
        # adjust volume based on type
        self.trades.history = self.trades.adjusted_volume()

        self.portfolio = pd.DataFrame()
        self.portfolio[self.labels.SHARES] = self._net_shares()
        self.portfolio[self.labels.AVG_PRICE] = self._average_purchase_price()
        # remove net 0 positions
        self.portfolio = self.portfolio[self.portfolio[self.labels.SHARES] != 0]
        self.portfolio[self.labels.MARKET_PRICE] = self._current_price()
        self.portfolio[self.labels.PL] = self._profit_and_loss()
        self.portfolio[self.labels.MARKET_VALUE] = self._market_value()
        self.portfolio[self.labels.SECTOR] = self._sector()
        self.portfolio.to_csv(portfolio_file)

    def _net_shares(self) -> pd.DataFrame:
        """Computes net position from trades."""
        net_shares = self.trades.history.groupby(
            self.labels.TICKER
        )[self.labels.ADJUSTED_VOL].sum()
        return net_shares

    def _average_purchase_price(self) -> pd.DataFrame:
        """Computes average purchase price of assets."""
        # naive, simple, implementation, just sum total and divide by net position
        avg_price = (
            self.trades.history.groupby("ticker")[self.labels.TOTAL].sum()
            / self.portfolio[self.labels.SHARES]
        )
        return avg_price

    def _current_price(self) -> pd.DataFrame:
        """Get current price from Yahoo finance."""
        market_price = self.portfolio.apply(
            lambda x: yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"], axis=1
        )
        return market_price

    def _profit_and_loss(self) -> pd.DataFrame:
        """Computes profit and loss."""
        profit_loss = (
            (
                self.portfolio[self.labels.MARKET_PRICE]
                - self.portfolio[self.labels.AVG_PRICE]
            )
            / self.portfolio[self.labels.AVG_PRICE]
            * 100
        )
        return profit_loss 

    def _market_value(self) -> pd.DataFrame:
        """Compute current value from number of shares and market price."""
        market_value = (
            self.portfolio[self.labels.MARKET_PRICE]
            * self.portfolio[self.labels.SHARES]
        )
        return market_value

    def _sector(self) -> pd.DataFrame:
        """Get assets business sector."""
        sector = self.portfolio.apply(
            lambda x: yf.Ticker(x.name).asset_profile[x.name]["sector"],
            axis=1,
        )
        return sector
