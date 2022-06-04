"""Process the trades DataFrame into a consolidated portfolio.

The transaction history is processed into a partfolio by combining trades that
refer to the same asset.

"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame
    from portman.trades import Trades

import warnings
import pandas as pd
import numpy as np
import yahooquery as yf


class Portfolio:
    """Creates portfolio object.

    Parameters
    ----------
    trades
        Object with transactions data or list of those.
    portfolio_file

    Attributes
    ----------
    summary
        Consolidate all trades processed into single data frame.

    """

    def __init__(
        self, trades: Trades | list[Trades], portfolio_file: str = None
    ) -> None:

        # process one or a list of trades
        self.trades_processed_collection = []
        if isinstance(trades, list):
            for t in trades:
                self.trades_processed_collection.append(self._consolidate_trades(t))
        else:
            self.trades_processed_collection.append(self._consolidate_trades(trades))

        # stack each trade consolidation on top of each other
        self.summary = pd.concat(self.trades_processed_collection)

        if portfolio_file is None:
            portfolio_file = f"portfolio.csv"
        self.summary.to_csv(portfolio_file, float_format="%.2f")

    def _consolidate_trades(self, trades: Trades) -> DataFrame:
        """Combine the transactions to get net position information."""
        trades_processed = pd.DataFrame()

        trades_processed[trades.labels.SHARES] = self._compute_net_shares(trades)
        trades_processed[trades.labels.AVG_PRICE] = self._compute_average_price(
            trades, trades_processed
        )

        # remove net 0 positions
        trades_processed = trades_processed[trades_processed[trades.labels.SHARES] != 0]

        trades_processed[trades.labels.MARKET_PRICE] = self._get_current_price(
            trades_processed
        )
        trades_processed[trades.labels.PL] = self._compute_profit_and_loss(
            trades, trades_processed
        )
        trades_processed[trades.labels.MARKET_VALUE] = self._compute_market_value(
            trades, trades_processed
        )
        trades_processed[trades.labels.SECTOR] = self._get_sector(trades_processed)
        trades_processed[trades.labels.NAME] = self._get_long_name(trades_processed)
        trades_processed[trades.labels.CURRENCY] = self._get_currency(trades_processed)
        trades_processed[trades.labels.ASSET_CLASS] = self._get_asset_type(
            trades_processed
        )
        return trades_processed

    def _compute_net_shares(self, trades: Trades) -> DataFrame:
        """Computes net position from trades."""
        # adjust volume based on type
        trades.history = trades.adjusted_volume()
        net_shares = trades.history.groupby(trades.labels.TICKER)[
            trades.labels.ADJUSTED_VOL
        ].sum()
        return net_shares

    def _compute_average_price(self, trades: Trades, summary: DataFrame) -> DataFrame:
        """Computes average purchase price of assets."""
        # sum total and divide by net position
        avg_price = (
            trades.history.groupby("ticker")[trades.labels.TOTAL].sum()
            / summary[trades.labels.SHARES]
        )
        return avg_price

    def _compute_profit_and_loss(self, trades: Trades, summary: DataFrame) -> DataFrame:
        """Computes profit or loss from market price."""
        profit_loss = (
            (summary[trades.labels.MARKET_PRICE] - summary[trades.labels.AVG_PRICE])
            / summary[trades.labels.AVG_PRICE]
            * 100
        )
        return profit_loss

    def _compute_market_value(
        self, trades: Trades, trades_processed: DataFrame
    ) -> DataFrame:
        """Compute current value from number of shares and market price."""
        market_value = (
            trades_processed[trades.labels.MARKET_PRICE]
            * trades_processed[trades.labels.SHARES]
        )
        return market_value

    def _get_current_price(self, trades_processed: DataFrame) -> DataFrame:
        """Get current price from Yahoo finance."""

        def yahoo_market_price(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"]
            except (KeyError, TypeError):
                warnings.warn(f"Quote not found for ticker symbol: {x.name}")
                return np.nan

        market_price = trades_processed.apply(lambda x: yahoo_market_price(x), axis=1)

        return market_price

    def _get_sector(self, summary: DataFrame) -> DataFrame:
        """Get assets business sector from Yahoo finance."""

        def yahoo_sector(x):
            try:
                return yf.Ticker(x.name).asset_profile[x.name]["sector"]
            except (KeyError, TypeError):
                return None

        sector = summary.apply(lambda x: yahoo_sector(x), axis=1)
        return sector

    def _get_long_name(self, trades_processed: DataFrame) -> DataFrame:
        """Get long name of security from Yahoo finance."""

        def yahoo_long_name(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["longName"]
            except (KeyError, TypeError):
                return np.nan

        long_name = trades_processed.apply(lambda x: yahoo_long_name(x), axis=1)
        return long_name

    def _get_currency(self, trades_processed: DataFrame) -> DataFrame:
        """Get currency of security from Yahoo finance."""

        def yahoo_currency(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["currency"]
            except (KeyError, TypeError):
                return np.nan

        currency = trades_processed.apply(lambda x: yahoo_currency(x), axis=1)

        return currency

    def _get_asset_type(self, trades_processed: DataFrame) -> DataFrame:
        """Get currency of security from Yahoo finance."""

        def yahoo_asset_type(x):
            try:
                return yf.Ticker(x.name).quotes[x.name]["quoteType"]
            except (KeyError, TypeError):
                return None

        currency = trades_processed.apply(lambda x: yahoo_asset_type(x), axis=1)

        return currency
