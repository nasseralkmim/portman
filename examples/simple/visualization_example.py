import matplotlib.pyplot  as plt
import portman.portvis.portfolio

portman.portvis.portfolio.allocation("simple_portfolio.csv")
portman.portvis.portfolio.summary("simple_portfolio.csv")

allocation = portman.portvis.portfolio.allocation_sunburst("simple_portfolio.csv")
profit_loss = portman.portvis.portfolio.profit_loss_asset("simple_portfolio.csv")
allocation.show()
profit_loss.show()
plt.show()
