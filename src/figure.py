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
