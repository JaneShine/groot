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

import numpy as np
from src.strategy import TargetTrade
import pdb

class Backtest(TargetTrade):
    def __init__(self, quote, params=None):
        self.params = params
        # self.quote = np.random.rand(10, 3) * 10
        default_position = None
        default_booksize = 100_0000
        self.quote = quote
        if self.params is None:
            self.booksize = default_booksize
            self.init_position = default_position
        else:
            if 'booksize' in self.params.keys():
                self.booksize = self.params['booksize']
            else:
                self.booksize = default_booksize
            if 'init_position' in self.params.keys():
                self.init_position = self.params['init_position']
            else:
                self.init_position = default_position
                
        self.init_trade()
        return
    
    def init_trade(self):
        TargetTrade.__init__(self, quote=self.quote, booksize=self.booksize,
                             init_position=self.init_position, params=self.params)
        return
    
    def order_execution(self, stk_dict):
        operating_date = stk_dict['mapping']
        for di in range(1, self.quote.shape[0]):
            if di in operating_date.keys():
                date_key = operating_date[di]
                stk_list = stk_dict[date_key].stk_idx.to_list()
                previous_booksize = self.cash[di-1] + sum(self.market_val[di-1])
                target_value = previous_booksize / len(stk_list)

                for ii in self.quote.shape[1]:
                    if ii in stk_list:
                        previous_mktv = self.position[di-1][ii] * self.quote[di-1][ii]
                        trade_value = target_value - previous_mktv
                        trade_price = self.quote[di][ii]
                        if trade_value < 0:  # close the position first
                            self.sell(di, ii, trade_value, trade_price, self.position[di-1][ii])
                        elif trade_value > 0:
                            self.buy(di, ii, trade_value, trade_price, self.cash[di-1])  # TODO: cash remained ranking and iteration!
                        else:
                            self.hold(di, ii)
                    else:
                        self.hold(di, ii)
            else:
                self.hold(di, ii)
        return




