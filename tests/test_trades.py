import os
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
import portman.trades
import portman.labels

labels = portman.labels.Labels()
file_name = os.path.join(os.path.dirname(__file__), "test_trades.csv")
trades = portman.trades.Trades(
    file_name,
    columns=[
        labels.DATE,
        labels.TYPE,
        labels.TICKER,
        labels.SHARES,
        labels.PURCHASE_PRICE,
        labels.FEE,
    ],
    date_column=labels.DATE,
)


def test_column_labels():
    assert list(trades.history.columns) == [
        labels.DATE,
        labels.TYPE,
        labels.TICKER,
        labels.SHARES,
        labels.PURCHASE_PRICE,
        labels.FEE,
        labels.TOTAL]


def test_dates_type():
    assert np.issubdtype(trades.history[labels.DATE].dtypes, np.datetime64)


def test_trades():
    df = pd.DataFrame(
        {
            labels.DATE: pd.to_datetime(["01-01-2020", "03-01-2020"],
                                        dayfirst=True),
            labels.TYPE: ["Buy", "Sell"],  # from file
            labels.TICKER: ["GOOG", "GOOG"],  # from file
            labels.SHARES: [40, 25],  # from file
            labels.PURCHASE_PRICE: [20.0, 40.0],  # from file
            labels.FEE: [0, 0],  # from file
            labels.TOTAL: [800.0, -1000.0],  # computed
        }
    )
    assert_frame_equal(df, trades.history)
