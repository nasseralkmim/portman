import portvis.portfolio
import portman.labels

fig = portvis.portfolio.allocation_sunburst("portfolio.csv", portman.labels)
fig.show()

fig2 = portvis.portfolio.profit_loss_asset("portfolio.csv", portman.labels)
fig2.show()
