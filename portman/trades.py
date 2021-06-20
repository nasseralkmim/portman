import pandas as pd


def process_trades(trades_file):
    """process the trade data

    Goal is to get:
    
    """
    trades = pd.read_csv(trades_file, sep=',',
                         names=['date', 'type',
                                'ticker', 'volume',
                                'price'],
                         decimal=',',
                         parse_dates=['date'], infer_datetime_format=True)
    trades['total'] = trades.apply(lambda x: x.price * x.volume
					    if x.type in ['Buy', 'Split']
					    else - x.price * x.volume, axis=1)
    trades['vol_adj'] = trades.apply(lambda x: x.volume
					    if x.type in ['Buy', 'Split']
					    else
					    (-x.volume if x.type in ['Sell'] else 0), axis=1)
    trades = trades.sort_values('date')
    trades.to_csv('trades.csv', index=False)
    return trades


# td = process_trades('../tests/trade_data.csv')
