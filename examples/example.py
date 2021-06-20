import portman.trades
import portman.portfolio
import portman.visualize
import matplotlib.pyplot as plt

td = portman.trades.process("trade_data.csv")
por = portman.portfolio.process(td)
portman.visualize.allocation('portfolio.csv')
portman.visualize.summary('portfolio.csv')
plt.show()


