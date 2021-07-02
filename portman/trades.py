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
            labels.SHARES,
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
    trades.to_csv(labels.TRADES_FILE, index=False)
    return trades

def total_invested(trades: pd.DataFrame) -> pd.DataFrame:
    """Compute total value invested."""
    trades[labels.TOTAL] = trades.apply(
        lambda x: x[labels.PURCHASE_PRICE] * x[labels.SHARES]
        if x[labels.TYPE] in [labels.BUY, labels.SPLIT]
        else -x[labels.PURCHASE_PRICE] * x[labels.SHARES], # negative sell
        axis=1,
    )
    return trades

def adjusted_volume(trades: pd.DataFrame) -> pd.DataFrame:
    """Adjusted position volume based on type and add column. """
    trades[labels.ADJUSTED_VOL] = trades.apply(
        lambda x: x[labels.SHARES]
        if x[labels.TYPE] in [labels.BUY, labels.SPLIT]
        # make it negative if type is 'sell'
        else (-x[labels.SHARES] if x[labels.TYPE] in [labels.SELL] else 0),
        axis=1,
    )
    return trades
