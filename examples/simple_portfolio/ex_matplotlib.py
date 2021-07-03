import matplotlib.pyplot  as plt
import portman.portvis.portfolio
import portman.labels

portman.portvis.portfolio.allocation("simple_portfolio.csv", portman.labels)
plt.show()
