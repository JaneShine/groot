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
from src.strategy import TargetTrade

class BackTest(TargetTrade):
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
        
        return




