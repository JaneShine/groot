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

