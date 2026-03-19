def clean_data(df):
    stock_counts = df.groupby('date')['symbol'].nunique()
    valid_dates = stock_counts[stock_counts >= 7].index
    df_clean = df[df['date'].isin(valid_dates)].copy()
    return df_clean
