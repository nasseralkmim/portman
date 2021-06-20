"""Process the trades DataFrame."""
import pandas as pd
import yahooquery as yf


def process(trades):
    """Consolidates trade data into a portfolio with current holdings.

    Args:
        trades : DataFrame

    """
    portfolio = pd.DataFrame()
    portfolio["Vol. liq."] = trades.groupby("ticker")["vol_adj"].sum()
    portfolio["Avg. price (R$)"] = (
        trades.groupby("ticker")["total"].sum() / portfolio["Vol. liq."]
    )
    portfolio = portfolio[portfolio["Vol. liq."] != 0]
    portfolio["Quote (R$)"] = portfolio.apply(
        lambda x: yf.Ticker(x.name + ".SA").quotes[x.name + ".SA"]["bid"], axis=1
    )
    portfolio["P/L (%)"] = (
        (portfolio["Quote (R$)"] - portfolio["Avg. price (R$)"])
        / portfolio["Avg. price (R$)"]
        * 100
    )
    portfolio["Current value (R$)"] = portfolio["Quote (R$)"] * portfolio["Vol. liq."]
    portfolio["Sector"] = portfolio.apply(
        lambda x: yf.Ticker(x.name + ".SA").asset_profile[x.name + ".SA"]["sector"],
        axis=1,
    )
    portfolio.to_csv("portfolio.csv")
    return portfolio
