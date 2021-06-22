"""Plots information about the portfolio snapshot"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from portman import labels

matplotlib.style.use("ggplot")
pd.options.display.float_format = "{:,.2f}".format


def allocation(portfolio_file):
    fig, ax = plt.subplots(nrows=1, ncols=2)
    portfolio = pd.read_csv(portfolio_file, index_col=labels.TICKER)
    portfolio[labels.CURRENT_VALUE].plot(
        kind="pie",
        label="",
        colormap="tab20",
        figsize=fig.get_size_inches() * 1.3,
        fontsize=8,
        ax=ax[0],
    )
    portfolio.groupby(labels.SECTOR).sum()[labels.CURRENT_VALUE].plot(
        kind="pie",
        label="",
        figsize=fig.get_size_inches() * 1.3,
        fontsize=8,
        colormap="tab20",
        ax=ax[1],
    )
    plt.tight_layout()
    return None


def summary(portfolio_file):
    fig, ax = plt.subplots()
    portfolio = pd.read_csv(portfolio_file, index_col=labels.TICKER).round(2)
    ax.xaxis.tick_top()
    portfolio[labels.PL].plot(
        kind="bar", cmap="tab20", ax=ax, xlabel="", figsize=fig.get_size_inches() * 1.3
    )
    pd.plotting.table(
        ax, portfolio[[labels.NET_POS, labels.AVG_PRICE, labels.QUOTE, labels.PL]],
    )
    return None
