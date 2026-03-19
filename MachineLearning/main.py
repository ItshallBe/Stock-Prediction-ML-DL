import pandas as pd
import numpy as np

from MachineLearning.feature import cal_momentum
from utils.constants import STOCK_DAILY, STOCK_5MIN, STOCK_30MIN
from utils.util import get_config, get_stock_data_csv_path

if __name__ == '__main__':
    config_data = get_config()
    stocks = config_data["test_stocks"]
    df_30min_dict = {}
    df_5min_dict = {}
    df_daily_dict = {}
    for stock in stocks:
        df_30min_dict[stock] = pd.read_csv(get_stock_data_csv_path(stock, STOCK_30MIN))
        df_5min_dict[stock] = pd.read_csv(get_stock_data_csv_path(stock, STOCK_5MIN))
        df_daily_dict[stock] = pd.read_csv(get_stock_data_csv_path(stock, STOCK_DAILY))
        df_30min_dict[stock].sort_values("date", ascending=True, inplace=True)
        df_5min_dict[stock].sort_values("date", ascending=True, inplace=True)
        df_daily_dict[stock].sort_values("date", ascending=True, inplace=True)
        cal_momentum(df_30min_dict[stock])

    print(df_30min_dict["AAPL"].head())

    pass