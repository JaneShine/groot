__author__ = 'jxxie'
__license__ = 'MIT License'

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import datetime
from src.orchestrator import Orchestrator
from src.figure import add_figure
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    handlers=[
                        logging.FileHandler('./trade.log', mode='w'),
                        logging.StreamHandler()
                    ])
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
        html.Label('Actual Book Size', style=label_style),
        dcc.Input(
            id='actual-booksize-input',
            type='number',
            value=1000000,  # default value
            style=input_style
        ),
        html.Label('Commission', style=label_style),
        dcc.Input(
            id='commission-input',
            type='number',
            value=0.002,  # default value
            step=0.0001,
            style=input_style
        ),
        html.Label('Multiplier', style=label_style),
        dcc.Input(
            id='multiplier-input',
            type='number',
            value=100,  # default value
            step=0.1,
            style=input_style
        ),
        html.Button('GO', id='go-button', n_clicks=0, style=button_style)
    ], style=left_column_style),
    
    html.Div([
        dcc.Graph(id='value-graph'),
        dcc.Graph(id='trade-graph'),
        html.Div([
            html.H3('Log Details', style={'textAlign': 'center'}),
            html.Pre(id='log-output', style={
                'height': '300px', 'overflowY': 'scroll', 
                'backgroundColor': '#f5f5f5', 'padding': '10px',
                'border': '1px solid #ddd', 'borderRadius': '4px'
            }),
            dcc.Interval(
                id='interval-component',
                interval=1000,  # 1000ms
                n_intervals=0
            )
        ], style={'marginTop': '20px'})
    ], style=right_column_style)
], style={'display': 'flex', 'justifyContent': 'space-between'})

@app.callback(
    [Output('value-graph', 'figure'),
     Output('trade-graph', 'figure')],
    [Input('go-button', 'n_clicks')],
    [State('stock-selection-input', 'value'),
     State('start-date-picker', 'date'),
     State('end-date-picker', 'date'),
     State('frequency-dropdown', 'value'),
     State('actual-booksize-input', 'value'),
     State('commission-input', 'value'),
     State('multiplier-input', 'value')]
)
def update_graphs(n_clicks, querying,
                  start_date, end_date,
                  frequency, 
                  actual_booksize, 
                  commission, 
                  multi):
    if n_clicks > 0:
        orch = Orchestrator(querying, start_date, end_date, 
                            frequency, 
                            actual_booksize, 
                            commission, 
                            multi)
        orch.fetch_stock_codes()
        orch.fetch_daily_data()
        orch.run_backtest()
        df_report = orch.gen_report(save=True)
        logging.info('[INFO] Successfully generate backtest report data...')
        value_figure, trade_figure = add_figure(df_report)
        logging.info('[INFO] Result is now showing in app...')
        n_clicks = 0
        return value_figure, trade_figure
    return {}, {}

@app.callback(
    Output('log-output', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_log(n_intervals):
    with open('trade.log', 'r', encoding='utf-8') as f:
        logs = f.read()
    return logs

if __name__ == '__main__':
    app.run_server(debug=True)
    