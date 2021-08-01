"""Creates a html dashboard to visualize portfolio information

Example:
        $python -m portman.portvis.dashboard "portfolio.csv"

"""
import argparse

import dash
import dash_core_components as dcc
import dash_html_components as html

import portman.portvis.portfolio

parser = argparse.ArgumentParser(description="Get portfolio .csv data")
parser.add_argument("portfolio")
args = parser.parse_args()
portfolio_file = args.portfolio

app = dash.Dash(__name__)

# dash core component (dcc) provides visual components
# higher level components (html, javascript, css)
# Graph render any plotly data visualization passed as the figure
# pie plot (subburst)
allocation_sunburst = dcc.Graph(
    id="Allocation",
    figure=portman.portvis.portfolio.allocation_sunburst(portfolio_file),
)

# bar plot with P/L for each asset
profit_loss_bar = dcc.Graph(
    id="P/L per asset",
    figure=portman.portvis.portfolio.profit_loss_asset(portfolio_file),
)

# table with portfolio data
portfolio_summary = dcc.Graph(
    id="Table", figure=portman.portvis.portfolio.summary_table(portfolio_file)
)


# layout describes what the application will look like
app.layout = html.Div(
    # list of components
    children=[
        # html provides visual components for hmtl tags
        html.H1(children="Portfolio Dashboard"),
        allocation_sunburst,
        profit_loss_bar,
        portfolio_summary,
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True, threaded=True, use_reloader=True)
