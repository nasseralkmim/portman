import matplotlib.pyplot  as plt
import portvis.portfolio
import portman.labels

portvis.portfolio.allocation("portfolio.csv", portman.labels)
plt.show()
