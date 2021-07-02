"""Plots information about the portfolio snapshot"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px

matplotlib.style.use("ggplot")
pd.options.display.float_format = "{:,.2f}".format


def allocation(portfolio_file: str, labels):
    """Plot allocation of the portfolio in a pie chart with matplotlib

    Allocation of portfolio based on value and sector.

    Args:
        portfolio_file (str): file name with portfolio data.
        labels (module 'portman.labels'): contains the labels for the
            columns in portfolio file.

    """
    fig, ax = plt.subplots(nrows=1, ncols=2)
    portfolio = pd.read_csv(portfolio_file, index_col=labels.TICKER)
    portfolio[labels.MARKET_VALUE].plot(
        kind="pie",
        label="",
        colormap="tab20",
        figsize=fig.get_size_inches() * 1.3,
        fontsize=8,
        ax=ax[0],
    )
    portfolio.groupby(labels.SECTOR).sum()[labels.MARKET_VALUE].plot(
        kind="pie",
        label="",
        figsize=fig.get_size_inches() * 1.3,
        fontsize=8,
        colormap="tab20",
        ax=ax[1],
    )
    plt.tight_layout()
    return fig


def summary(portfolio_file, labels):
    """Plot portolio summary with P/L distribution with matplotlib"""
    fig, ax = plt.subplots()
    portfolio = pd.read_csv(portfolio_file, index_col=labels.TICKER).round(2)
    ax.xaxis.tick_top()
    portfolio[labels.PL].plot(
        kind="bar", cmap="tab20", ax=ax, xlabel="", figsize=fig.get_size_inches() * 1.3
    )
    pd.plotting.table(
        ax,
        portfolio[[labels.SHARES, labels.AVG_PRICE, labels.QUOTE, labels.PL]],
    )
    return fig


def allocation_sunburst(portfolio_file: str, labels):
    """Plot allocation with sector in a "sunburst" graph with plotly"""
    portfolio = pd.read_csv(portfolio_file)
    fig = px.sunburst(
        portfolio, path=[labels.SECTOR, labels.TICKER], values=labels.MARKET_VALUE
    )
    return fig


def profit_loss_asset(portfolio_file: str, labels):
    """Plot P/L per asset as bar chart with plotly"""
    portfolio = pd.read_csv(portfolio_file)
    fig = px.bar(portfolio, x=labels.TICKER, y=labels.PL)

    return fig
