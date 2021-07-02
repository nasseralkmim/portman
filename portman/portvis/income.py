"""Plot income over time"""
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.style.use("ggplot")
pd.options.display.float_format = "{:,.2f}".format


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
