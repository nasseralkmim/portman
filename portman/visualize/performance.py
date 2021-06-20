"""Plot performance of holdings over time"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use("ggplot")
pd.options.display.float_format = "{:,.2f}".format

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
