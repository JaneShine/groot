__author__ = 'jxxie'
__license__ = 'MIT License'

#================================================================================
# Copyright (c) [2024] [jxxie]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
 #================================================================================

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
from src.datamanager import DataManager

app = dash.Dash(__name__)

# Styling dictionaries
left_column_style = {
    'width': '25%', 'padding': '20px', 
    'backgroundColor': '#e6f4ff', 'borderRadius': '10px', 
    'boxShadow': '2px 2px 5px #888888', 'display': 'inline-block', 
    'verticalAlign': 'top', 'marginRight': '2%', 'float': 'left'
}

right_column_style = {
    'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top', 
    'padding': '20px', 'backgroundColor': '#f9f9f9', 
    'borderRadius': '10px', 'boxShadow': '2px 2px 5px #888888', 'float': 'left'
}

input_style = {
    'width': '92%', 'height': '32px', 'padding': '6px 12px', 
    'fontSize': '14px', 'lineHeight': '1.42857143', 'color': '#555', 
    'backgroundColor': '#fff', 'border': '1px solid #ccc', 
    'borderRadius': '4px', 'boxShadow': 'inset 0 1px 1px rgba(0,0,0,.075)', 
    'transition': 'border-color ease-in-out .15s,box-shadow ease-in-out .15s',
    'marginBottom': '20px'
}

button_style = {
    'width': '100%', 'backgroundColor': '#337ab7', 'color': 'white', 
    'padding': '10px', 'border': 'none', 'borderRadius': '4px', 
    'cursor': 'pointer'
}

label_style = {
    'display': 'block', 'marginBottom': '5px', 'fontSize': '16px', 
    'color': '#333', 'fontWeight': 'bold'
}

# Custom CSS for the date picker
date_picker_style = {
    'border': '1px solid #ccc', 
    'borderRadius': '4px', 
    'padding': '4px 8px', 
    'fontSize': '14px', 
    'width': '94%',
    'height': '50px', 
    'marginBottom': '20px',
    'boxShadow': 'inset 0 1px 1px rgba(0,0,0,.075)',
    'transition': 'border-color ease-in-out .15s, box-shadow ease-in-out .15s'
}

# Layout of the app
app.layout = html.Div([
    html.Div([
        html.H2('Groot', style={'textAlign': 'center', 'color': '#0D47A1'}),
        html.Label('Prompt', style=label_style),
        dcc.Input(
            id='stock-selection-input',
            type='text',
            value='中外资加仓持股股数前十的股票',  # default value
            style=input_style
        ),
        html.Label('StartDate', style=label_style),
        html.Div(
            dcc.DatePickerSingle(
                id='start-date-picker',
                min_date_allowed=datetime.date(2000, 1, 1),
                max_date_allowed=datetime.date.today(),
                initial_visible_month=datetime.date.today(),
                date=datetime.date(2019, 1, 1),  # default value
                day_size=35,
                style=date_picker_style
            ), style={'width': '100%'}
        ),
        html.Label('EndDate', style=label_style),
        html.Div(
            dcc.DatePickerSingle(
                id='end-date-picker',
                min_date_allowed=datetime.date(2000, 1, 1),
                max_date_allowed=datetime.date.today(),
                initial_visible_month=datetime.date.today(),
                date=datetime.date(2020, 1, 1),  # default value
                day_size=35,
                style=date_picker_style
            ), style={'width': '100%'}
        ),
        html.Label('BacktestFreq', style=label_style),
        dcc.Dropdown(
            id='frequency-dropdown',
            options=[
                {'label': 'Monthly', 'value': 'M'},
                {'label': 'Quarterly', 'value': 'Q'}
            ],
            value='M',  # default value
            style={'marginBottom': '20px'}
        ),
        html.Button('GO', id='go-button', n_clicks=0, style=button_style)
    ], style=left_column_style),
    
    html.Div([
        dcc.Graph(id='value-graph'),
        dcc.Graph(id='trade-graph')
    ], style=right_column_style)
], style={'display': 'flex', 'justifyContent': 'space-between'})

@app.callback(
    [Output('value-graph', 'figure'),
     Output('trade-graph', 'figure')],
    [Input('go-button', 'n_clicks')],
    [State('stock-selection-input', 'value'),
     State('start-date-picker', 'date'),
     State('end-date-picker', 'date'),
     State('frequency-dropdown', 'value')
     ]
)
def update_graphs(n_clicks, querying, start_date, end_date, frequency):
    if n_clicks > 0:
        dm = DataManager(querying, start_date, end_date, frequency)
        dm.fetch_stock_codes()
        dm.fetch_daily_data()
        value_figure = {
            'data': [],
            'layout': {
                'title': 'Backtest Value'
            }
        }
        trade_figure = {
            'data': [],
            'layout': {
                'title': 'Trade Actions'
            }
        }
        return value_figure, trade_figure
    return {}, {}

if __name__ == '__main__':
    app.run_server(debug=True)


