import os
import pytest
import pandas as pd
from pandas._testing import assert_frame_equal
import portman.trades
import portman.labels


def test_trades():
    labels = portman.labels.Labels()
    file_name = os.path.join(os.path.dirname(__file__),
                         'test_trades.csv')
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
        labels=labels,
    )
    df = pd.DataFrame(
        {
            labels.DATE: pd.to_datetime(["01-01-2020", "03-01-2020"], dayfirst=True),
            labels.TYPE: ["Buy", "Sell"],
            labels.TICKER: ["GOOG", "GOOG"],
            labels.SHARES: [40, 25],
            labels.PURCHASE_PRICE: [20., 40.],
            labels.FEE: [0, 0],
            labels.TOTAL: [800., -1000.]
        }
    )
    assert_frame_equal(df, trades.history)
