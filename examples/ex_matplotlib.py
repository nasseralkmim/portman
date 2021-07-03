import matplotlib.pyplot  as plt
import portman.portvis.portfolio
import portman.labels

portman.portvis.portfolio.allocation("portfolio.csv", portman.labels)
plt.show()
