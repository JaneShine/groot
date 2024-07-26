__author__ = 'jxxie'
__license__ = 'MIT License'

import warnings
warnings.filterwarnings('ignore')
import pywencai as pywc


class iFindQuerying:
    def __init__(self, querying):
        self.querying = querying
        self.res = {}
        self.stk_codes = []

    def fetching_stock(self, date):
        df_stk = pywc.get(query=f'{date} {self.querying}', loop=True)
        self.res[date] = df_stk
        self.stk_codes += df_stk['股票代码'].to_list()
        return self

