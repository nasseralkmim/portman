"""Creates a html dashboard to visualize portfolio information

Example:
        $python -m portman.portvis.dashboard "portfolio.csv"

"""
import argparse

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import portman.portvis.portfolio

parser = argparse.ArgumentParser(description='Get portfolio .csv data')
parser.add_argument('portfolio')
args = parser.parse_args()
portfolio_file = args.portfolio

app = dash.Dash(__name__)

# layout describes what the application will look like
app.layout = html.Div(
    # list of components
    children=[
        # html provides visual components for hmtl tags
        html.H1(children="portvis - Portfolio Visualizer"),

        # dash core component (dcc) provides visual components
        # higher level components (html, javascript, css)
        # Graph render any plotly data visualization passed as the figure
        dcc.Graph(
            id="Allocation",
            figure=portman.portvis.portfolio.allocation_sunburst(
                portfolio_file
            ),
        ),

        dcc.Graph(
            id="P/L per asset",
            figure=portman.portvis.portfolio.profit_loss_asset(portfolio_file),
        ),

        dcc.Graph(
            id="Table",
            figure=portman.portvis.portfolio.summary_table(portfolio_file)
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
