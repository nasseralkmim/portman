"""Creates a html dashboard to visualize portfolio information

Example:
        $python -m portman.portvis.dashboard "portfolio.csv"


"""
import argparse

import dash
import dash_core_components as dcc
import dash_html_components as html

import portman.labels

import portman.portvis.portfolio

parser = argparse.ArgumentParser(description='Get portfolio .csv data')
parser.add_argument('portfolio')
args = parser.parse_args()
portfolio_file = args.portfolio

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="portvis - Portfolio Visualizer"),
        # dash core component
        dcc.Graph(
            id="Allocation",
            figure=portman.portvis.portfolio.allocation_sunburst(
                portfolio_file, portman.labels
            ),
        ),
        dcc.Graph(
            id="P/L per asset",
            figure=portman.portvis.portfolio.profit_loss_asset(portfolio_file, portman.labels),
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
