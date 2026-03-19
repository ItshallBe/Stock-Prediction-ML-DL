import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt

from MachineLearning.clean import clean_data
from MachineLearning.debug import concat_statics
from MachineLearning.feature import cal_momentum, generate_all_features, STRATEGY, EXCLUDED_COLS
from MachineLearning.label import get_30min_label, TARGET_LABEL_30_MIN_RETURN_4
from utils.constants import STOCK_DAILY, STOCK_5MIN, STOCK_30MIN
from utils.util import get_config, get_stock_data_csv_path

if __name__ == '__main__':
    config_data = get_config()
    stocks = config_data["stocks"]
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
        # process features and labels
        generate_all_features(df_30min_dict[stock])
        get_30min_label(df_30min_dict[stock])
        df_30min_dict[stock] = df_30min_dict[stock].dropna()
        df_30min_dict[stock]["symbol"] = stock
        columns_to_keep = STRATEGY["30min"]["strat1"]
        df_30min_dict[stock] = df_30min_dict[stock][columns_to_keep]

    # multi stock concat
    df_all = pd.concat(df_30min_dict.values(), ignore_index=True)
    df_all = df_all.sort_values(["date", "symbol"])
    df_all = df_all.reset_index(drop=True)
    df_clean = clean_data(df_all)
    features = [c for c in df_clean.columns if c not in EXCLUDED_COLS]
    train_df = df_clean[df_clean["date"] < '2024-01-01']
    valid_df = df_clean[(df_clean["date"] >= '2024-01-01') & (df_clean["date"] < '2025-01-01')]
    test_df = df_clean[df_clean["date"] >= '2025-01-01']
    X_train, y_train = train_df[features], train_df[TARGET_LABEL_30_MIN_RETURN_4]
    X_valid, y_valid = valid_df[features], valid_df[TARGET_LABEL_30_MIN_RETURN_4]
    X_test, y_test = test_df[features], test_df[TARGET_LABEL_30_MIN_RETURN_4]

    model = lgb.LGBMRegressor(
        n_estimators=1000,
        learning_rate=0.01,
        max_depth=4,
        num_leaves=9,
        min_child_samples=200,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
    )
    print("开始训练 LightGBM...")
    model.fit(
        X_train, y_train,
        eval_set=[(X_valid, y_valid)],
        eval_metric="rmse",
        callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=True)],
    )
    lgb.plot_importance(model, max_num_features=15, importance_type='gain', figsize=(10, 6), title='Top 15 Feature Importance (Gain)')
    plt.show()
    test_df['prediction'] = model.predict(X_test)
    print("\n预测完成！测试集预览：")
    print(test_df[['date', 'symbol', 'will_return_4', 'prediction']].head(10))


    # debug
    # concat_statics(df_30_min_all)
    # print(f"参与训练的特征数量: {len(features)}")
    # print(features)

    pass