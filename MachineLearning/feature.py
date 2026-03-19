
def cal_momentum(df):
    df["return_1"] = df["close"].pct_change(1)
    df["return_2"] = df["close"].pct_change(2)
    df["return_4"] = df["close"].pct_change(4)
    df["return_8"] = df["close"].pct_change(8)
    pass

def cal_trend(df):
    df["MA5"] = df["close"].rolling(5).mean()
    df["MA10"] = df["close"].rolling(10).mean()
    df["MA20"] = df["close"].rolling(20).mean()
    df["price_MA20"] = df["close"] / (df["close"].rolling(20).mean())

def cal_volatility(df):
    df["rolling_std_5"] = df["close"].rolling(5).std()
    df["rolling_std_10"] = df["close"].rolling(10).std()
    df["ATR"] = df["close"].ewm()
    df["high_low_range"] = (df["high"] - df["low"]).ewm(span=10).mean()
    pass

def cal_liquidity(df):

    pass

def cal_ta(df):
    df["volume_change"] = df["volume"].pct_change(1)

    pass