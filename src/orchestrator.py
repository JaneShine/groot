__author__ = 'jxxie'
__license__ = 'MIT License'

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import numpy as np
import tushare as ts
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    handlers=[
                        logging.FileHandler('./trade.log', mode='w'),
                        logging.StreamHandler()
                    ])
from tqdm import tqdm
from pyfolio.timeseries import perf_stats
from src.playback import Playback
from api.api_wencai import iFindQuerying
from src.utils import date_resample, TqdmToLogger
tqdm_out = TqdmToLogger(logging.getLogger(), level=logging.INFO)


class Orchestrator:
    def __init__(self, querying, start_date, end_date,
                freq, booksize, commission, multi, token
                 ):
        try:
            self.pro = ts.pro_api(token)
            os.environ['TUSHARE_TOKEN'] = token
        except:
            raise ValueError('API token invalid!')
        self.querying = querying
        self.robot = iFindQuerying(querying)
        self.start = str(start_date).replace('-','')
        self.end = str(end_date).replace('-','')
        self.freq = freq
        self.booksize = booksize
        self.commission = commission
        self.multi = multi
        self.querying_date = date_resample(self.start, self.end, self.freq)
        return

    def fetch_stock_codes(self):
        logging.info('[INFO] Querying understanding...')
        for idate in tqdm(self.querying_date,file=tqdm_out,
                           ncols=100, desc='Processing'):
            self.robot.fetching_stock(idate)
        return

    def fetch_daily_data(self):
        self.codes = set(self.robot.stk_codes)
        quote_list = []
        logging.info('[INFO] Fetching stk quote...')
        for icode in self.codes:
            _quote = self.pro.daily(ts_code=icode,
                                    start_date=self.start,
                                    end_date=self.end)
            quote_list.append(_quote)
        df_quote = pd.concat(quote_list)
        self.quote_matrix = df_quote.pivot_table(index='trade_date',
                                                 columns='ts_code', values='close')
        self.quote = self.quote_matrix.values
        return 

    def run_backtest(self):
        logging.info('[INFO] Run backtest...')
        # mark idx for robot.res
        for k in self.robot.res.keys():
            _slice = self.robot.res[k]
            _slice['stk_idx'] = self.quote_matrix.columns\
                                    .get_indexer(_slice['股票代码'].to_list())
        self.quote_matrix.columns
        # offset tradingdate mapping: find the nearlest date can be traded
        self.trading_date_mapping = {}
        date_list = list(self.robot.res.keys())
        for idate in date_list:
            _quote_date = idate.replace('.','')
            if idate != date_list[-1]:
                find_trading_date = self.quote_matrix.index >= _quote_date
                idx = np.where(find_trading_date == True)[0][0]
            else:
                idx = -1
            self.trading_date_mapping[idx] = idate
        self.robot.res['date_mapping'] = self.trading_date_mapping
        self.robot.res['stkcode_mapping'] = self.quote_matrix.columns
        # backtest go
        self.brain = Playback(quote=self.quote, booksize=self.booksize,
                              commission=self.commission, multi=self.multi)
        self.brain.order_execution(self.robot.res)
        logging.info('[INFO] Backtest Done...')
        return 
    
    def gen_report(self):
        df_report = pd.DataFrame()
        df_report['total_pnl'] = pd.DataFrame(self.brain.pnl).sum(axis=1)
        df_report['mktv'] = pd.DataFrame(self.brain.market_val)\
                            .fillna(method='ffill').sum(axis=1)
        df_report['cash_remained'] = self.brain.cash
        df_report['trade_value'] = pd.DataFrame(self.brain.trade_val).sum(axis=1)
        df_report['booksize'] = df_report.mktv + df_report.cash_remained
        df_report.booksize = df_report.booksize.fillna(method='ffill')
        df_report.index = self.quote_matrix.index
        df_report.index = pd.to_datetime(df_report.index, format='%Y%m%d')
        stats = perf_stats(df_report.booksize.pct_change().dropna())
        return df_report, stats
    
    def save_report(self, df, save=True):
        if save and not df.empty:
            record_list = []
            for k,v in self.robot.res.items():
                if k not in ('date_mapping', 'stkcode_mapping'):
                    v.columns = [x.split('[')[0] for x in v.columns]
                    v.drop(['market_code','code','stk_idx'],
                            axis=1, inplace=True)
                    v['rebalance_date'] = k
                    record_list.append(v)
            df_record = pd.concat(record_list)
            df_record.to_csv('detail_data.csv', encoding='gbk')
            df.to_csv('rpt_data.csv')
            logging.info(f'[INFO] Results have been saved to {os.getcwd()}!')
        return


