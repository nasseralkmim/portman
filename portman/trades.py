"""Module that process the trades data file"""
import pandas as pd


def process(trades_file):
    """Process the trade data from trades_file.

    Saves the output to a '.csv' file.

    Returns:
        DataFrame
    """
    trades = pd.read_csv(
        trades_file,
        sep=",",
        names=["date", "type", "ticker", "volume", "price"],
        decimal=",",
        parse_dates=["date"],
        infer_datetime_format=True,
    )
    trades["total"] = trades.apply(
        lambda x: x.price * x.volume
        if x.type in ["Buy", "Split"]
        else -x.price * x.volume,
        axis=1,
    )
    trades["vol_adj"] = trades.apply(
        lambda x: x.volume
        if x.type in ["Buy", "Split"]
        else (-x.volume if x.type in ["Sell"] else 0),
        axis=1,
    )
    trades = trades.sort_values("date")
    trades.to_csv("trades.csv", index=False)
    return trades
