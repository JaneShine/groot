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
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
from src.backtest import Backtest
from api.api_wencai import iFindQuerying
from src.utils import date_resample
import tushare as ts
from tqdm import tqdm
import pdb


class DataManager:
    def __init__(self, querying, start_date, end_date, freq):
        self.pro = ts.pro_api()
        self.querying = querying
        self.robot = iFindQuerying(querying)
        self.start = str(start_date).replace('-','')
        self.end = str(end_date).replace('-','')
        self.freq = freq
        self.querying_date = date_resample(self.start, self.end, self.freq)
        return

    def fetch_stock_codes(self):
        for idate in tqdm(self.querying_date):
            self.robot.fetching_stock(idate)
        return

    def fetch_daily_data(self):
        self.codes = set(self.robot.stk_codes)
        quote_list = []
        for icode in self.codes:
            _quote = self.pro.daily(ts_code=icode, start_date=self.start, end_date=self.end)
            quote_list.append(_quote)
        df_quote = pd.concat(quote_list)
        self.quote_matrix = df_quote.pivot_table(index='trade_date',
                                                 columns='ts_code', values='close')
        self.quote = self.quote_matrix.values
        return 

    def run_backtest(self):
        # mark idx for robot.res
        for k in self.robot.res.keys():
            _slice = self.robot.res[k]
            _slice['stk_idx'] = self.quote_matrix.columns.get_indexer(_slice['股票代码'].to_list())
        self.quote_matrix.columns
        # offset tradingdate mapping
        self.trading_date_mapping = {}
        date_list = list(self.robot.res.keys())
        for idate in date_list:
            _quote_date = idate.replace('.','')
            find_trading_date = self.quote_matrix.index >= _quote_date
            idx = np.where(find_trading_date == True)[0][0]
            self.trading_date_mapping[idx] = idate
        self.robot.res['mapping'] = self.trading_date_mapping
        # backtest go
        brain = Backtest(quote=self.quote)
        brain.order_execution(self.robot.res)
        return 

if __name__ == '__main__':
    # a = BackTest(quote)
    # a.order_execution(b.res)
    dm = DataManager('中外资加仓持股股数前十的股票', '20190101', '20200101', 'M')
    dm.fetch_stock_codes()
    dm.fetch_daily_data()
    dm.run_backtest()