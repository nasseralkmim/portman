"""Encapsulates trade data from input file """
from __future__ import annotations  # allows type hint "list[str]"

import pandas as pd
from portman.labels import Labels


class Trades:
    """Process the trade data.

    Args:
        dayfirst: date format starts with day by default.

    """

    def __init__(
        self,
        trades_file: str,
        columns: list[str],
        date_column: str,
        labels: Labels,
        dayfirst: bool = True,
    ):
        self.columns = columns
        self.date_column = date_column
        self.labels = labels  # aggregation of Labels object
        self.history = self._parse_trades_file(trades_file, dayfirst)
        self.history = self._transation_total()

    def _parse_trades_file(self, trades_file: str, dayfirst: bool) -> pd.DataFrame:
        """Parse trades file into a data frame."""
        trades = pd.read_csv(
            trades_file,
            sep=",",
            names=self.columns,
            parse_dates=[self.date_column],
            infer_datetime_format=True,
            dayfirst=dayfirst
        )
        return trades

    def _transation_total(self) -> pd.DataFrame:
        """Compute total transaction value."""
        self.history[self.labels.TOTAL] = self.history.apply(
            lambda x: x[self.labels.PURCHASE_PRICE] * x[self.labels.SHARES]
            if x[self.labels.TYPE] in [self.labels.BUY, self.labels.SPLIT]
            else -x[self.labels.PURCHASE_PRICE]
            * x[self.labels.SHARES],  # negative sell
            axis=1,
        )
        return self.history

    def adjusted_volume(self) -> pd.DataFrame:
        """Adjusted position volume based on type and add column.

        The type of the trade defines it the shares will add or subtract.

        """
        self.history[self.labels.ADJUSTED_VOL] = self.history.apply(
            lambda x: x[self.labels.SHARES]
            if x[self.labels.TYPE] in [self.labels.BUY, self.labels.SPLIT]
            # make it negative if type is 'sell'
            else (
                -x[self.labels.SHARES]
                if x[self.labels.TYPE] in [self.labels.SELL]
                else 0
            ),
            axis=1,
        )
        return self.history
