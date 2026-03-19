import talib
import pandas as pd

from MachineLearning.label import TARGET_LABEL_30_MIN_RETURN_4

STRATEGY = {
    "30min": {
        "strat1": ["symbol", "date",
                   "return_1", "return_2", "return_4", "return_8",
                   "MA5", "MA10", "MA20", "price_MA20",
                   "rolling_std_5", "rolling_std_10", "ATR", "high_low_range",
                   "RSI", "MACD", "BOLL",
                   "volume_change", "volume_ma_ratio", "price_volume_corr", "volume_zscore",
                   TARGET_LABEL_30_MIN_RETURN_4
                   ],
    }
}

EXCLUDED_COLS = ['symbol', 'date', TARGET_LABEL_30_MIN_RETURN_4]

def cal_momentum(df):
    df["return_1"] = df["close"].pct_change(1)
    df["return_2"] = df["close"].pct_change(2)
    df["return_4"] = df["close"].pct_change(4)
    df["return_8"] = df["close"].pct_change(8)

def cal_trend(df):
    df["MA5"] = df["close"].rolling(5).mean()
    df["MA10"] = df["close"].rolling(10).mean()
    df["MA20"] = df["close"].rolling(20).mean()
    df["price_MA20"] = df["close"] / (df["close"].rolling(20).mean())

def cal_volatility(df):
    df["rolling_std_5"] = df["close"].rolling(5).std()
    df["rolling_std_10"] = df["close"].rolling(10).std()
    df["ATR"] = talib.ATR(df["high"], df["low"], df["close"], timeperiod=14)
    df["high_low_range"] = (df["high"] - df["low"]).ewm(span=10).mean()

def cal_ta(df):
    df["RSI"] = talib.RSI(df["close"], timeperiod=14)
    df["MACD"], df["MACD_signal"], df["MACD_hist"] = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
    upperband, middleband, lowerband = talib.BBANDS(df["close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    df["BOLL"] = (upperband - lowerband) / middleband

def cal_volume(df):
    df["volume_change"] = df["volume"].pct_change()
    df["volume_ma5"] = df["volume"].rolling(5).mean()
    df["volume_ma_ratio"] = df["volume"] / df["volume_ma5"]
    df["price_return"] = df["close"].pct_change()
    df["price_volume_corr"] = df["price_return"].rolling(10).corr(df["volume_change"])
    df["volume_zscore"] = (df["volume"] - df["volume"].rolling(10).mean()) / df["volume"].rolling(10).std()

def generate_all_features(df):
    cal_momentum(df)
    cal_trend(df)
    cal_volatility(df)
    cal_ta(df)
    cal_volume(df)
    return df