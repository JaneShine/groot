__author__ = 'jxxie'
__license__ = 'MIT License'

import numpy as np
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    handlers=[
                        logging.FileHandler('./trade.log', mode='w'),
                        logging.StreamHandler()
                    ])
from src.base import TargetTrade


class Playback(TargetTrade):
    def __init__(self, quote, booksize=None,
                  commission=None, multi=None):
        self.quote = quote
        if booksize is None:
            self.booksize = 100_0000
        else:
            self.booksize = booksize
        self.commission = commission
        self.multi = multi
        self.init_trade()
        return
    
    def init_trade(self):
        TargetTrade.__init__(self, quote=self.quote, booksize=self.booksize,
                             commission=self.commission, multi=self.multi)
        return
    
    def order_execution(self, stk_dict):
        operating_date = stk_dict['date_mapping']
        stkcode_mapping = stk_dict['stkcode_mapping']

        for di in range(1, self.quote.shape[0]):

            if di in operating_date.keys():
                date_key = operating_date[di]
                stk_list = stk_dict[date_key].stk_idx.to_list()
                now_booksize = self.cash[di-1] + np.nansum(self.market_val[di-1])  # booksize can be used
                target_value = now_booksize / len(stk_list)
                now_mktv = self.position[di-1] * self.quote[di-1]
                now_stk_list = np.where(now_mktv> 0)[0]
                # calc trade value for different asset
                trade_value_array = np.zeros(len(now_mktv))
                diff = set(now_stk_list) - set(stk_list)
                close_idx = np.array(list(diff))
                stk_list_new = np.array(list(set(stk_list + list(now_stk_list))))
                trade_value_array[stk_list_new] = target_value - now_mktv[stk_list_new]

                if len(close_idx):
                    trade_value_array[close_idx] = - now_mktv[close_idx]  # close position when need

                # locate trade operate type
                sell_idx = np.where(trade_value_array < 0)[0]
                buy_idx = np.where(trade_value_array > 0)[0]
                all_idx = np.arange(len(trade_value_array))
                hold_idx = np.setdiff1d(all_idx, np.union1d(sell_idx, buy_idx))  # fix suspending

                # close the position first to release cash
                for ii in sell_idx:
                    trade_value = trade_value_array[ii]
                    self.target_sell(di, ii, trade_value)
                    logging.info(f'[INFO] date {date_key}, asset {stkcode_mapping[ii]}, trade_value {trade_value}')
                for ii in buy_idx:
                    trade_value = trade_value_array[ii]
                    self.target_buy(di, ii, trade_value)
                    logging.info(f'[INFO] date {date_key}, asset {stkcode_mapping[ii]}, trade_value {trade_value}')
                for ii in hold_idx:
                    self.target_hold(di, ii)
            else:
                for ii in range(self.quote.shape[1]):
                    self.target_hold(di, ii)
        return

