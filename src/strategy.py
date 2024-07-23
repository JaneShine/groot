__author__ = 'jxxie'
__license__ = 'MIT License'

#================================================================================
# Copyright (c) [2021] [jxxie]

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
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')



class TradeBase:
    """ A trade base declared kinds of trading executions, and for stk&etf only
    """
    def __init__(self, quote, booksize, params, *args, **kwargs):
        self.params = params  # this is for position adjustion weights and trading commissions dict
        if self.params is None:
            self.commission = 0.0005
            self.partial_traded = False
            self.multi = 100  # default stk cn
        else:
            self.commission = float(self.params['commission'])
            self.partial_traded = self.params['partial_traded'] == 'true'
            self.multi = int(self.params['multi'])
        self.quote = quote
        self.booksize = booksize
        return
    
    def buy(self, idate, iasset, trade_val, price, cash_remained):
        '''signal == 1 trade_val is target trading market value WITH DIRECTION
        '''
        if trade_val > cash_remained:
            if  self.partial_traded:
                trade_val = cash_remained
                logging.warning(f'[WARNIG] date {idate}, asset {iasset}: only have cash of {cash_remained}, partial traded!')
            else:
                raise ValueError(f'trade value of {trade_val} exceeds cash remained:{cash_remained}!')
        
        trade_volume = np.floor(trade_val / price // self.multi) * self.multi 
        self.update_balancesheet(idate, iasset, trade_volume, price)
        return

    def sell(self, idate, iasset, trade_val, price, pos):
        '''trade_val is target trading market value WITH DIRECTION
        '''
        if pos < 1e-5:
            raise KeyError(f'current position of {iasset} is 0, sell is forbiden!')
        
        trade_volume = np.sign(trade_val) * np.floor(abs(trade_val) / price // self.multi) * self.multi
        
        if abs(trade_volume) > pos:
            if self.partial_traded:
                trade_volume = np.sign(trade_val) * pos
                logging.info(f'[WARNIG] date {idate}, asset {iasset}: only have position of {pos}, partial traded!')
            else:
                raise ValueError(
                f'only have position of {pos}, require {trade_volume}')

        self.update_balancesheet(idate, iasset, trade_volume, price)
        return 
    
    def hold(self, idate, iasset):
        trade_volume = 0
        trade_price = 0
        self.update_balancesheet(idate, iasset, trade_volume, trade_price)
        return

    def update_balancesheet(self, idate, iasset, trade_volume, trade_price):
        '''update the balancesheet by a specific trade_volume WITH DIRECTION
           NOTICE: 
           `self.position`, `self.cash`,`self.trade_val`,`self.trade_price`,`self.trade_volume`, `self.market_val`,`self.pnl`,should be define in subclass
        '''
        
        self.position[idate + 1][iasset] = self.position[idate][iasset] + trade_volume
        self.cash[idate + 1] = self.cash[idate] -  trade_volume * trade_price - \
                                trade_volume * trade_price * self.commission
        self.trade_val[idate][iasset] = trade_volume * trade_price
        self.trade_price[idate][iasset] = trade_price if trade_volume > 1e-5 else np.nan
        self.trade_volume[idate][iasset] = trade_volume
        self.market_val[idate + 1][iasset] = self.position[idate + 1][iasset] *\
                                             self.quote[idate + 1][iasset]
        
        self.pnl[idate + 1][iasset] = self.pnl[idate][iasset] + \
                                    (self.position[idate] * (self.quote[idate + 1][iasset] - self.quote[idate][iasset])) + \
                                    (trade_volume * (self.quote[idate + 1][iasset] - trade_price))
                                    
        return


class TargetTrade(TradeBase):
    """SignalTrade
    This is a sim-trade object job base for signal-based strategy with specified buy/sell/hold signal in timeline and a trading weight of booksize declared.
    The class aimed at updation of current state of position and pnl calculation

    """
    def __init__(self, init_position=None, *args, **kwargs) -> None:
        '''init the requried dict to record the trade order
        status dict: pnl, price, market_val, cash, positon 
        var dict: trade_volume, trade_val
        the var dict is the variation of status dict
        '''
        super().__init__(*args, **kwargs)
        self.status_tuple = self.quote.shape
        self.var_tuple = (self.quote.shape[0]-1, self.quote.shape[1])
        # mandatory
        self.cash = np.zeros(self.status_tuple[0])
        self.cash[0] = self.booksize
        # optional
        self.position = init_position
        if self.position is None:
            self.position = np.zeros(self.status_tuple) # positions are initialized by setting default of ndarray of signal.shape
        else:
            self.position =  np.vstack((self.position, np.zeros(self.var_tuple)))  # expand into panel

        self.reset()
        return 

    def reset(self):
        '''reset the dict to be traced
        '''
        self.trade_val = np.zeros(self.var_tuple)
        self.market_val = np.zeros(self.status_tuple)
        self.market_val[:,0] = self.position[:,0] * self.quote[:,0]
        # for performance
        self.pnl = np.zeros(self.status_tuple)
        self.trade_price = np.zeros(self.var_tuple)
        self.trade_volume = np.zeros(self.var_tuple)
        return
    
    def buy(self, idate, iasset, trade_val):
        price = self.quote[idate][iasset]
        cash_remained = self.cash[idate]
        super().buy(idate, iasset, trade_val, price, cash_remained)
        return
    
    def sell(self, idate, iasset, trade_val):
        '''trade_val is target trading market value WITH DIRECTION
        '''
        pos = self.position[idate][iasset]
        price = self.quote[idate][iasset]
        super().sell(idate, iasset, trade_val, price, pos)
        return 

    def hold(self, idate, iasset):
        super().hold(idate, iasset)
        return

    def order_execution(self):
        '''the order to update the position
        '''
        raise NotImplementedError(f"Please implement the `order_execution` method")