"""Example to create a processed portfolio"""
import portman.trades
import portman.portfolio

trades = portman.trades.process("trade_data.csv")
por = portman.portfolio.process(trades)


