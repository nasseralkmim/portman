"""Module that process the trades data file"""
import pandas as pd
from portman import labels


def process(trades_file):
    """Process the trade data from trades_file.

    Saves the output to a '.csv' file.

    Returns:
        DataFrame
    """
    trades = pd.read_csv(
        trades_file,
        sep=",",
        names=[
            labels.DATE,
            labels.TYPE,
            labels.TICKER,
            labels.VOL,
            labels.PURCHASE_PRICE,
        ],
        decimal=",",
        parse_dates=[labels.DATE],
        infer_datetime_format=True,
    )

    trades = total_invested(trades)
    trades = adjusted_volume(trades)

    trades = trades.sort_values(labels.DATE)
    trades.to_csv("trades.csv", index=False)
    return trades

def total_invested(trades):
    """Compute total value invested

    Args:
        trades : DataFrame
    
    """
    trades[labels.TOTAL_INVESTED] = trades.apply(
        lambda x: x.price * x.volume
        if x.type in ["Buy", "Split"]
        else -x.price * x.volume,
        axis=1,
    )
    return trades

def adjusted_volume(trades):
    """Adjusted position volume based on type and add column

    Args:
        trades : DataFrame
    
    """
    trades[labels.ADJUSTED_VOL] = trades.apply(
        lambda x: x.volume
        if x.type in ["Buy", "Split"]
        else (-x.volume if x.type in ["Sell"] else 0),
        axis=1,
    )
    return trades
