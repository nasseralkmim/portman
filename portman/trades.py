"""Encapsulates trade data from input file """
from __future__ import annotations  # allows type hint list[str], dict[str, str]

import pandas as pd
from portman.labels import Labels


class Trades:
    """Process the trade data.

    Args:
        dayfirst: date format starts with day by default.
        columns: list of labels to use as columns names in the dataframe.
            if `None` assume that the `trades_file` is in a specific order.
            
        dayfirst: date format starts with day or month.

    """

    def __init__(
            self,
            trades_file: str,
            columns: list[str] = None,
            date_column: str = None,
            dayfirst: bool = True,
            asset_class: str = None,
    ) -> None:
        
        self.labels = Labels()  # composition of Labels

        self.trades_file = trades_file

        self.columns = self._set_columns(columns)

        if asset_class is None:
            self.asset_class = trades_file.rsplit('.')[0]
        else:
            self.asset_class = asset_class

        # label of the column with dates
        if date_column is None:
            self.date_column = self.labels.DATE
        else:
            self.date_column = date_column

        self.history = self._get_trade_history(trades_file, dayfirst)
        self.history[self.labels.TOTAL] = self._set_transaction_total()

    def _get_trade_history(self, trades_file: str, dayfirst: bool) -> pd.DataFrame:
        """Parse trades file into a data frame."""
        trades = pd.read_csv(
            trades_file,
            sep=",",
            names=self.columns,
            parse_dates=[self.date_column],
            infer_datetime_format=True,
            dayfirst=dayfirst,
        )
        return trades

    def _set_transaction_total(self) -> pd.DataFrame:
        """Compute total transaction value into a new DF column."""
        transaction_total = self.history.apply(
            lambda x: x[self.labels.PURCHASE_PRICE] * x[self.labels.SHARES]
            if x[self.labels.TYPE] in [self.labels.BUY, self.labels.SPLIT]
            else -x[self.labels.PURCHASE_PRICE]
            * x[self.labels.SHARES],  # negative sell
            axis=1,
        )
        return transaction_total

    def _set_columns(self, columns: list[str] = None) -> list[str]:
        """Set columns labels."""
        if columns is None:
            col = [
                self.labels.DATE,
                self.labels.TYPE,
                self.labels.TICKER,
                self.labels.SHARES,
                self.labels.PURCHASE_PRICE,
                self.labels.FEE,
            ]
        else:
            col = columns
        return col

    def adjusted_volume(self) -> pd.DataFrame:
        """Adjusted position volume based on type and add column.

        The type of the trade defines it the shares will add or subtract.

        """
        self.history[self.labels.ADJUSTED_VOL] = self.history.apply(
            lambda x: x[self.labels.SHARES]
            if x[self.labels.TYPE] in [self.labels.BUY, self.labels.SPLIT]
            # make it negative if type is 'sell' positive otherwise
            else (
                -x[self.labels.SHARES]
                if x[self.labels.TYPE].lower() in [self.labels.SELL]
                else 0
            ),
            axis=1,
        )
        return self.history
