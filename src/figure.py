__author__ = 'jxxie'
__license__ = 'MIT License'

import plotly.graph_objs as go

def add_figure(df_report):

    pnl_trace = go.Scatter(x=df_report.index,
                           y=df_report['total_pnl'],
                           mode='lines', name='PnL')
    
    booksize_trace = go.Scatter(x=df_report.index, 
                                y=df_report['booksize'], 
                                mode='lines', 
                                fill='tozeroy', name='Book Size', 
                                yaxis='y2')
    
    value_figure = {
        'data': [pnl_trace, booksize_trace],
        'layout': {
            'title': 'PnL and Book Size Over Time',
            'yaxis': {'title': 'PnL', 'tickformat': '.2s'},
            'yaxis2': {
                'title': 'Book Size',
                'overlaying': 'y',
                'side': 'right',
                'tickformat': '.2s'
            }
        }
    }
        
    trade_trace = go.Bar(x=df_report.index, 
                         y=df_report['trade_value'], 
                         name='Trade Value',
                         yaxis='y2')
    
    cash_trace = go.Scatter(x=df_report.index, 
                            y=df_report['cash_remained'], 
                            mode='lines', name='Cash Remained')
    
    mktv_trace = go.Scatter(x=df_report.index, 
                            y=df_report['mktv'], 
                            mode='lines', name='Market Value')
    
    trade_figure = {
        'data': [trade_trace, cash_trace, mktv_trace],
        'layout': {
            'title': 'Trade Value, Cash Remained and Market Value Over Time',
            'yaxis': {'title': 'Cash and Market Value',
                      'tickformat': '.2s'},
            'yaxis2': {
                'title': 'Trade Value',
                'overlaying': 'y',
                'side': 'right',
                'tickformat': '.2s'
            },
            'barmode': 'group'
        }
    }
    return value_figure, trade_figure

