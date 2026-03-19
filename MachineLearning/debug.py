def concat_statics(df):
    stock_counts = df.groupby('date')['symbol'].nunique()

    print("unique date&symbol distribute: ")
    print(stock_counts.value_counts())