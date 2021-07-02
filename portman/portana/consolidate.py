# consolidade portfolio
from .trades import process_trades
from .returns import process_returns
from .portfolio import process_portfolio
from .dividends import process_dividends


def consolidate(trade_file):
    """consolidate portfolio """
    trades = process_trades(trade_file)
    portfolio = process_portfolio(trades)
    returns = process_returns(trades)
    dividends = process_dividends(portfolio, trades)
    return None


# consolidate('../tests/trade_data.csv')
