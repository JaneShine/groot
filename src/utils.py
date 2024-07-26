__author__ = 'jxxie'
__license__ = 'MIT License'

import pandas as pd
import logging

def date_resample(start, end, freq):
    '''
    start: date string, YYYY-MM-DD
    end: date string, YYYY-MM-DD
    '''
    dates = pd.date_range(start=start, end=end, freq=freq)
    dates = [str(x)[:10].replace('-', '.') for x in dates]
    return dates


class TqdmToLogger:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level
        self.buf = ''

    def write(self, buf):
        self.buf = buf.strip('\r\n\t ')
        if self.buf:
            self.logger.log(self.level, self.buf)

    def flush(self):
        pass

