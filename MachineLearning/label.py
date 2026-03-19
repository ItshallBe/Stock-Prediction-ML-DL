import pandas as pd

TARGET_LABEL_30_MIN_RETURN_4 = "will_return_4"

def get_30min_label(df):
    df[TARGET_LABEL_30_MIN_RETURN_4] = (df["close"].shift(-4) - df["close"]) / df["close"]