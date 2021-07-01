"""Process the trades DataFrame into a consolidate portfolio."""
import pandas as pd
import yahooquery as yf
from portman import labels


def process(trades):
    """Consolidates trade data into a portfolio DataFrame with current holdings.

    Note:
        Saves into a '.csv' file.

    Args:
        trades (DataFrame): processed trades data.

    """
    portfolio = pd.DataFrame()
    portfolio = net_position(trades, portfolio)
    portfolio = average_purchase_price(trades, portfolio)
    portfolio = current_price(portfolio)
    portfolio = profit_and_loss(portfolio)
    portfolio = current_value(portfolio)
    portfolio = sector(portfolio)
    portfolio.to_csv(labels.PORTFOLIO_FILE)
    return portfolio


def net_position(trades, portfolio):
    """Compute net position from trades.

    Introduces a new column into the portfolio DataFrame

    Args:
        trades (DataFrame): processed trades.
        portfolio (DataFrame): processed portfolio.

    """
    portfolio[labels.NET_POS] = trades.groupby("ticker")[labels.ADJUSTED_VOL].sum()
    return portfolio



def average_purchase_price(trades, portfolio):
    """Compute average purchase price of an asset and adds new column

    Args:
        trades (DataFrame): processed trades.

    """
    # naive implementation, just sum total and divide by net position
    # TODO need to accounts for 
    portfolio[labels.AVG_PRICE] = (
        trades.groupby("ticker")[labels.TOTAL_INVESTED].sum() / portfolio[labels.NET_POS]
    )
    # remove net 0 positions
    portfolio = portfolio[portfolio[labels.NET_POS] != 0]
    return portfolio


def current_price(portfolio):
    """Get current price from Yahoo finance and add a column to portfolio

    Introduces a new column into the portfolio DataFrame

    Args:
        portfolio (DataFrame): processed portfolio.
    """
    portfolio[labels.QUOTE] = portfolio.apply(
        lambda x: yf.Ticker(x.name + ".SA").quotes[x.name + ".SA"]["bid"], axis=1
    )
    return portfolio

def profit_and_loss(portfolio):
    """Compute profit and loss and adds a columns to the DataFrame

    Args:
        portfolio (DataFrame): processed portfolio.

    """
    portfolio[labels.PL] = (
        (portfolio[labels.QUOTE] - portfolio[labels.AVG_PRICE])
        / portfolio[labels.AVG_PRICE]
        * 100
    )
    return portfolio


def current_value(portfolio):
    """Compute current value and add column to DataFrame

    Args:
        portfolio (DataFrame): processed portfolio.

    """
    portfolio[labels.CURRENT_VALUE] = portfolio[labels.QUOTE] * portfolio[labels.NET_POS]
    return portfolio


def sector(portfolio):
    """Get asset business sector"""
    portfolio["Sector"] = portfolio.apply(
        lambda x: yf.Ticker(x.name + ".SA").asset_profile[x.name + ".SA"]["sector"],
        axis=1,
    )
    return portfolio
