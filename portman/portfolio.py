"""Process the trades DataFrame into a consolidate portfolio."""
import pandas as pd
import yahooquery as yf
from portman import labels


def process(trades: pd.DataFrame) -> pd.DataFrame:
    """Consolidates trade data into a portfolio DataFrame with current holdings."""
    portfolio = pd.DataFrame()
    portfolio = net_position(trades, portfolio)
    portfolio = average_purchase_price(trades, portfolio)
    portfolio = current_price(portfolio)
    portfolio = profit_and_loss(portfolio)
    portfolio = current_value(portfolio)
    portfolio = sector(portfolio)
    portfolio.to_csv(labels.PORTFOLIO_FILE)
    return portfolio


def net_position(
    trades: pd.DataFrame, portfolio: pd.DataFrame) -> pd.DataFrame:
    """Compute net position from trades."""
    portfolio[labels.NET_POS] = trades.groupby("ticker")[labels.ADJUSTED_VOL].sum()
    return portfolio


def average_purchase_price(
    trades: pd.DataFrame, portfolio: pd.DataFrame) -> pd.DataFrame:
    """Compute average purchase price of an asset and adds new column."""
    # naive, simple, implementation, just sum total and divide by net position
    portfolio[labels.AVG_PRICE] = (
        trades.groupby("ticker")[labels.TOTAL_INVESTED].sum()
        / portfolio[labels.NET_POS]
    )
    # remove net 0 positions
    portfolio = portfolio[portfolio[labels.NET_POS] != 0]
    return portfolio


def current_price(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Get current price from Yahoo finance and add a column to portfolio."""
    portfolio[labels.QUOTE] = portfolio.apply(
        lambda x: yf.Ticker(x.name).quotes[x.name]["regularMarketPrice"], axis=1
    )
    return portfolio


def profit_and_loss(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Compute profit and loss and adds a columns to the DataFrame."""
    portfolio[labels.PL] = (
        (portfolio[labels.QUOTE] - portfolio[labels.AVG_PRICE])
        / portfolio[labels.AVG_PRICE]
        * 100
    )
    return portfolio


def current_value(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Compute current value and add column to DataFrame."""
    portfolio[labels.CURRENT_VALUE] = (
        portfolio[labels.QUOTE] * portfolio[labels.NET_POS]
    )
    return portfolio


def sector(portfolio: pd.DataFrame) -> pd.DataFrame:
    """Get asset business sector"""
    portfolio["Sector"] = portfolio.apply(
        lambda x: yf.Ticker(x.name).asset_profile[x.name]["sector"],
        axis=1,
    )
    return portfolio
