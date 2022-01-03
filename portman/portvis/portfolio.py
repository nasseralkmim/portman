"""Plots information about the portfolio snapshot"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from portman.labels import Labels

matplotlib.style.use("ggplot")
pd.options.display.float_format = "{:,.2f}".format


labels = Labels()       # default labels

def allocation(portfolio_file: str) -> plt.Figure:
    """Plot allocation of the portfolio in a pie chart with matplotlib """

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


def summary(portfolio_file: str) -> plt.Figure:
    """Plot portolio summary with P/L distribution with matplotlib"""
    fig, ax = plt.subplots()
    portfolio = pd.read_csv(portfolio_file, index_col=labels.TICKER).round(2)
    ax.xaxis.tick_top()
    portfolio[labels.PL].plot(
        kind="bar", cmap="tab20", ax=ax, xlabel="", figsize=fig.get_size_inches() * 1.3
    )
    pd.plotting.table(
        ax,
        portfolio[[labels.SHARES,
                   labels.AVG_PRICE,
                   labels.MARKET_PRICE,
                   labels.PL]],
    )
    return fig


def allocation_sunburst(portfolio_file: str) -> plt.Figure:
    """Plot allocation with sector in a "sunburst" graph with plotly"""
    portfolio = pd.read_csv(portfolio_file)
    fig = px.sunburst(
        portfolio,
        path=[labels.ASSET_CLASS,
              labels.TICKER],
        values=labels.MARKET_VALUE
    )
    return fig


def profit_loss_asset(portfolio_file: str) -> plt.Figure:
    """Plot P/L per asset as bar chart with plotly"""
    portfolio = pd.read_csv(portfolio_file)
    fig = px.bar(portfolio, x=labels.TICKER, y=labels.PL)

    return fig

def summary_table(portfolio_file: str) -> plt.Figure:
    """Create summary table of portfolio."""
    portfolio = pd.read_csv(portfolio_file)
    fig = go.Figure(data=[
        go.Table(
            header=dict(values=portfolio.columns),
            cells=dict(values=[i for i in portfolio.to_numpy().T]))
    ])
    return fig
