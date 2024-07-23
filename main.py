import pandas as pd
from src.backtest import BackTest
from api.api_wencai import iFindQuerying
from src.report import app
import tushare as ts
pro = ts.pro_api()


if __name__ == '__main__':
    # quote = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')

    # a = BackTest(quote)
    # b = iFindQuerying(querying)
    # for idate in xxx:
    #     b.fetching_stock(idate)
    # a.order_execution(b.res)
    app.run_server(debug=True)
