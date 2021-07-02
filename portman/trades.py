"""Module that process the raw trades data file"""
import pandas as pd
from portman import labels


def process(trades_file: str) -> pd.DataFrame:
    """Process the trade data from trades_file and save it to a file."""
    trades = pd.read_csv(
        trades_file,
        sep=",",
        names=[
            labels.DATE,
            labels.TYPE,
            labels.TICKER,
            labels.VOL,
            labels.PURCHASE_PRICE,
            labels.FEE
        ],
        # decimal=",",
        parse_dates=[labels.DATE],
        infer_datetime_format=True,
    )
    trades = total_invested(trades)
    trades = adjusted_volume(trades)

    trades = trades.sort_values(labels.DATE)
    trades.to_csv("trades.csv", index=False)
    return trades

def total_invested(trades: pd.DataFrame) -> pd.DataFrame:
    """Compute total value invested."""
    trades[labels.TOTAL_INVESTED] = trades.apply(
        lambda x: x.price * x.volume
        if x.type in ["Buy", "Split"]
        else -x.price * x.volume,
        axis=1,
    )
    return trades

def adjusted_volume(trades: pd.DataFrame) -> pd.DataFrame:
    """Adjusted position volume based on type and add column."""
    trades[labels.ADJUSTED_VOL] = trades.apply(
        lambda x: x.volume
        if x.type in ["Buy", "Split"]
        else (-x.volume if x.type in ["Sell"] else 0),
        axis=1,
    )
    return trades
