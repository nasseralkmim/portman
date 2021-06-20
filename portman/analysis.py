import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use("ggplot")
pd.options.display.float_format = "{:,.2f}".format


def allocation(portfolio_file):
    fig, ax = plt.subplots(nrows=1, ncols=2)
    portfolio = pd.read_csv(portfolio_file, index_col="ticker")
    portfolio["Current value (R$)"].plot(
        kind="pie",
        label="",
        colormap="tab20",
        figsize=fig.get_size_inches() * 1.3,
        fontsize=8,
        ax=ax[0],
    )
    portfolio.groupby("Sector").sum()["Current value (R$)"].plot(
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
    portfolio = pd.read_csv(portfolio_file, index_col="ticker").round(2)
    ax.xaxis.tick_top()
    portfolio["P/L (%)"].plot(
        kind="bar", cmap="tab20", ax=ax, xlabel="", figsize=fig.get_size_inches() * 1.3
    )
    pd.plotting.table(
        ax, portfolio[["Vol. liq.", "Avg. price (R$)", "Quote (R$)", "P/L (%)"]],
    )
    return None


def returns(returns_file):
    """Plot returns

    TODO: convert returns to anualized form after grouping by year

    """
    fig = plt.figure()
    gs = fig.add_gridspec(2, 2)
    ax = [
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1]),
        fig.add_subplot(gs[0, :]),
    ]
    returns = pd.read_csv("returns.csv", parse_dates=["date"], skiprows=[1])
    m_returns = (
        returns.groupby(returns.date.dt.to_period("M"))["hpr"].prod() - 1
    ) * 100
    m_returns.plot(
        kind="bar",
        ylabel="Return %",
        ax=ax[0],
        figsize=fig.get_size_inches() * 1.2,
        color=(m_returns > 0).map({True: "g", False: "r"}),
    )

    returns["days"] = returns["date"].groupby(returns.date.dt.to_period("Y")).diff()
    y_returns = (
        returns.groupby(returns.date.dt.to_period("Y"))["hpr"].prod() - 1
    ) * 100
    y_returns.plot(
        kind="bar",
        ax=ax[1],
        figsize=fig.get_size_inches() * 1.2,
        color=(y_returns > 0).map({True: "g", False: "r"}),
    )

    ((returns.set_index("date").hpr.cumprod() - 1) * 100).plot(
        ylabel="Return (%)",
        ax=ax[2],
        figsize=fig.get_size_inches() * 1.2,
    )
    plt.tight_layout()
    return None


def dividends(dividends_file):
    fig = plt.figure()
    gs = fig.add_gridspec(2, 2)
    ax = [
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1]),
        fig.add_subplot(gs[0, :]),
    ]
    dividends = pd.read_csv(dividends_file, parse_dates=["date_com"])

    (
        dividends.groupby("ticker")["total"]
        .sum()
        .plot(
            kind="bar",
            ylabel="Dividends R$",
            ax=ax[2],
            figsize=fig.get_size_inches() * 1.2,
        )
    )

    (
        dividends.groupby(dividends.date_com.dt.to_period("M"))["total"]
        .sum()  # group by month period and sum
        .resample("M")  # adds periods without data
        .sum()
        .plot(
            kind="bar",
            xlabel="Dates",
            ylabel="Dividends R$",
            ax=ax[0],
            figsize=fig.get_size_inches() * 1.2,
        )
    )

    (
        dividends.groupby(dividends.date_com.dt.to_period("Y"))["total"]
        .sum()
        .plot(
            kind="bar",
            xlabel="Dates",
            ylabel="Dividends R$",
            ax=ax[1],
            figsize=fig.get_size_inches() * 1.2,
        )
    )
