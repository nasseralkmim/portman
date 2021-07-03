import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import pandas as pd
import portman as pm


pm.analysis.summary('portfolio.csv')
pm.analysis.allocation('portfolio.csv')
pm.analysis.returns('returns.csv')
pm.analysis.dividends('dividends.csv')
plt.tight_layout()
plt.show()
