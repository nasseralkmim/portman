import portman.portvis.portfolio

portfolio_file = 'portfolio.csv'
allocation = portman.portvis.portfolio.allocation_sunburst(portfolio_file)
profit_loss = portman.portvis.portfolio.profit_loss_asset(portfolio_file)
summary = portman.portvis.portfolio.summary_table(portfolio_file)
allocation.show()
profit_loss.show()
