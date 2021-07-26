"""Encapsulates trade data from input file """
from __future__ import annotations  # allows type hint list[str], dict[str, str]

import pandas as pd
from portman.labels import Labels


class Trades:
    """Process the trade data.

    Args:
        trades_file: file name with extension.
        columns: list of labels to use as columns names in the dataframe.
            if `None` assume that the `trades_file` is in a specific order.
        dayfirst: date format starts with day by default (dd/mm/yyyy), if False,
            date starts with month (mm/dd/yyyy).

    Attributes:
        labels: labels object with default strings.
        trades_file: 
    """
    def __init__(
            self,
            trades_file: str,
            columns: list[str] = None,
            date_column: str = None,
            dayfirst: bool = True,
    ) -> None:
        
        self.labels = Labels()  # composition of Labels

        self.trades_file = trades_file

        self.columns = self._set_columns(columns)

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

        def total(x):
            # positive total transaction value if buy and split
            if x[self.labels.TYPE].lower() in [self.labels.BUY, self.labels.SPLIT]:
                return x[self.labels.PURCHASE_PRICE] * x[self.labels.SHARES]
            # negative total transaction value if sell
            elif x[self.labels.TYPE].lower() in [self.labels.SELL]:
                return -x[self.labels.PURCHASE_PRICE] * x[self.labels.SHARES]
            else:
                raise(f'Invalid trade type {x.TYPE}, fix the .csv')

        transaction_total = self.history.apply(
                lambda x: total(x), axis=1,)

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

        Raises:
            If trade "type" in the .csv is not "buy", "sell" or "split".

        """
        def adjust_vol(x):
            if x[self.labels.TYPE].lower() in [self.labels.BUY, self.labels.SPLIT]:
                return x[self.labels.SHARES]
            elif x[self.labels.TYPE].lower() in [self.labels.SELL]:
                # make it negative if type is 'sell' positive otherwise
                return -x[self.labels.SHARES]
            else:
                raise(f'Invalid trade type {x.TYPE}, fix the .csv')

        self.history[self.labels.ADJUSTED_VOL] = self.history.apply(
            lambda x: adjust_vol(x), axis=1)

        return self.history
