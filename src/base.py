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

class TradeBase:
    """ A trade base declared kinds of trading executions, and for stk&etf only.
    `idate`or `di` represents the trading operation day, with the default being trading at the close.
    After a successful trade, this class will update the balance sheet for the tradingday's close and record the trade info.
    """
    def __init__(self, quote, booksize, commission=None, multi=None, *args, **kwargs):
        self.partial_traded = True  # partial execution of trades when cash or position is insufficient
        if commission is None:
            self.commission = 0.0005
        else:
            self.commission = commission
        if multi is None:
            self.multi = 100
        else:
            self.multi = multi
        self.quote = quote
        self.booksize = booksize
        self.cash_remained = self.booksize
        return
    
    def buy(self, idate, iasset, trade_val, price):
        '''signal == 1 trade_val is target trading market value WITH DIRECTION
        '''
        if trade_val > self.cash_remained:
            if self.partial_traded:
                trade_val = self.cash_remained
            else:
                raise ValueError(f'[ERROR] date {idate}, asset {iasset}: trade value of {trade_val} exceeds cash remained:{self.cash_remained}!')
        
        trade_volume = np.floor(trade_val / price // self.multi) * self.multi 
        self.update_balancesheet(idate, iasset, trade_volume, price)
        return

    def sell(self, idate, iasset, trade_val, price):
        '''trade_val is target trading market value WITH DIRECTION
        '''
        pos = self.position[idate - 1][iasset]
        if pos < 1e-5:
            raise KeyError(f'current position of {iasset} is 0, sell is forbiden!')
        
        trade_volume = np.sign(trade_val) * np.floor(abs(trade_val) / price // self.multi) * self.multi
        
        if abs(trade_volume) > pos:
            if self.partial_traded:
                trade_volume = np.sign(trade_val) * pos
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
        self.position[idate][iasset] = self.position[idate - 1][iasset] + trade_volume
        # consider the sequential trading scenarios of multiple assets, separately extract the retained cash for iteration
        self.cash_remained += -  trade_volume * trade_price - \
                                    trade_volume * trade_price * self.commission  
        self.cash[idate] = self.cash_remained
        self.trade_val[idate][iasset] = trade_volume * trade_price
        self.trade_price[idate][iasset] = trade_price if trade_volume > 1e-5 else np.nan
        self.trade_volume[idate][iasset] = trade_volume
        self.market_val[idate][iasset] = self.position[idate][iasset] *\
                                             self.quote[idate][iasset]
        if np.isnan(self.quote[idate][iasset]) or np.isnan(self.quote[idate - 1][iasset]):  # suspension of trading
            self.pnl[idate][iasset] = self.pnl[idate - 1][iasset]
        else:
            self.pnl[idate][iasset] = self.pnl[idate - 1][iasset] + \
                                        (self.position[idate - 1][iasset] * (self.quote[idate][iasset] - self.quote[idate - 1][iasset])) + \
                                        (trade_volume * (self.quote[idate][iasset] - trade_price))
        return


class TargetTrade(TradeBase):
    """SignalTrade
    This is a sim-trade object job base for a target market value strategy in timeline and a trading weight or value of booksize should be declared.
    The class aimed at updation of current state of position and pnl calculation
    """
    def __init__(self, *args, **kwargs) -> None:
        '''init the requried dict to record the trade order
        status dict: pnl, price, market_val, cash, positon 
        var dict: trade_volume, trade_val
        the var dict is the variation of status dict
        '''
        super().__init__(*args, **kwargs)
        self.status_tuple = self.quote.shape
        self.cash = np.zeros(self.status_tuple[0])
        self.cash[0] = self.booksize
        self.position = np.zeros(self.status_tuple)
        self.reset()
        return 

    def reset(self):
        '''reset the dict to be traced
        '''
        self.trade_val = np.zeros(self.status_tuple)
        self.market_val = np.zeros(self.status_tuple)
        self.market_val[:,0] = self.position[:,0] * self.quote[:,0]
        # for performance
        self.pnl = np.zeros(self.status_tuple)
        self.trade_price = np.zeros(self.status_tuple)
        self.trade_volume = np.zeros(self.status_tuple)
        return
    
    def target_buy(self, idate, iasset, trade_val):
        price = self.quote[idate][iasset]
        if np.isnan(price):
            super().hold(idate, iasset)  # suspension of trading
        else:
            super().buy(idate, iasset, trade_val, price)
        return
    
    def target_sell(self, idate, iasset, trade_val):
        '''trade_val is target trading market value WITH DIRECTION
        '''
        price = self.quote[idate][iasset]
        if np.isnan(price):
            super().hold(idate, iasset)  # suspension of trading
        else:
            super().sell(idate, iasset, trade_val, price)
        return 

    def target_hold(self, idate, iasset):
        super().hold(idate, iasset)
        return

    def order_execution(self):
        '''the order to update the position
        '''
        raise NotImplementedError(f"Please implement the `order_execution` method")
    