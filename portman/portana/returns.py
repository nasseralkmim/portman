# compute performance using TWR and MWR
import yahooquery as yf
import pandas as pd


def consolidate_partial_portfolio(trades, date):
    """Consolidate partial portfolio

    partial portfolio is the holdings a day before the cash flow date

    Args:
        trades (DataFrame): trade data created with trades.process_trades()
        date (datetime.date): cash flow date
    Returns:
        DataFrame with partial portfolio 1 day before cash flow

    """
    portfolio = pd.DataFrame()
    portfolio["vol_liq"] = trades[trades.date < date].groupby("ticker")["vol_adj"].sum()
    portfolio = portfolio[portfolio.vol_liq != 0]

    def get_quote(row):
        # offset by 25 because yahoo finance missing data
        # dicided to get an approximation with previously known quote
        # close price is adjusted for splits
        quote = yf.Ticker(row.name + ".SA").history(
            start=date + pd.DateOffset(-25), end=date
        )["close"]
        return quote.values[-1]

    portfolio["quote"] = portfolio.apply(get_quote, axis=1)
    portfolio["total"] = portfolio.vol_liq * portfolio.quote
    return portfolio


def process_returns(trades):
    """Compute returns of each holding period

    Steps:
    1. for each cash flow date
    1.1. get partial portfolio on the day before the cash flow
    2. compute return (TWR) using previous ending value of
        portfolio and correct for the cash flow

    Optimization:
    1. if returns.csv file exists
    1.1 loop over cash flow dates that are not there (the newer ones)
    2. add a new returns row for each new cash flow

    Returns:
        DataFrame with returns data for each
    """
    try:
        # check if returns file exists
        returns = pd.read_csv('returns.csv', parse_dates=['date'])
        last_date = returns.date.iloc[-1] # last date registred
    except FileNotFoundError:
        returns = pd.DataFrame()
        last_date = pd.Timestamp(0)

    r = []
    for row in trades[trades.date > last_date].itertuples():
        partial_portfolio = consolidate_partial_portfolio(trades, row.date)
        # initial investment
        # the cash flow value is considered zero
        # ending value is equal the initial investment
        if partial_portfolio.total.sum() == 0:
            r.append({"date": row.date, "ending_value": row.total, "cf_value": 0})
        else:
            r.append(
                {
                    "date": row.date,
                    "ending_value": partial_portfolio.total.sum(),
                    "cf_value": row.total,
                }
            )

    new_returns = pd.DataFrame(r)

    returns = returns.append(new_returns)

    # get total cash flow for each day
    returns = returns.groupby(["date", "ending_value"], as_index=False)[
        "cf_value"
    ].sum()

    def hold_period_return(row):
        """Compute TWR"""
        index = returns.index.get_loc(row.name)  # get index of row
        if index == 0:
            return 0
        prev_row = returns.iloc[index - 1]  # get previous row
        return row.ending_value / (prev_row.ending_value + prev_row.cf_value)

    returns["hpr"] = returns.apply(hold_period_return, axis=1)
    returns.to_csv("returns.csv", index=False)
    return returns
