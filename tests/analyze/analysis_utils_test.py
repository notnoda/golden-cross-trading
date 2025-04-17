import pandas as pd
import pandas_ta as ta
import numpy as np
import math

import trader.analyze.analysis_utils as utils
import tests.analyze.analyze_utils_data as adata

def add_analyze_macd():
    data_df = adata.get_test_df()
    macd_df = utils.add_analyze_macd(data_df)

    for index, row in macd_df.iterrows():
        print(f"{index}:\t{row['macd_val']}\t{row['macd_signal']}\t{row['macd_histo']}\t{row['macd_diff']}\t{row['macd_index']}")

def get_analyze_df():
    data_df = adata.get_test_df()
    macd_df = utils.get_analyze_df(data_df)

    for index, row in macd_df.iterrows():
        print(f"{index}:\t{row['macd_val']}\t{row['macd_signal']}\t{row['macd_histo']}\t{row['macd_diff']}\t{row['macd_index']}")

def get_analyze_sma():
    data_df = adata.get_test_df()
    sma_df = utils.add_analyze_sma(data_df)

    for index, row in sma_df.iterrows():
        print(f"{index}:\t{row['close']}\t{row['sma']}")

def get_analyze():
    data_df = utils.add_analyze_sma(utils.get_analyze_df(adata.get_test_df()))
    #print(data_df)

    #x = data_df["close"]
    #y = data_df["sma"]
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 30, 40, 50]

    val = utils.get_corr_val(x, y)
    print(val)

def get_corr_val():
    data_df = utils.add_analyze_sma(utils.get_analyze_df(adata.get_test_df()))
    #x = data_df["close"]
    #y = data_df["sma"]
    #x = [20, 31, 45, 53, 66]
    #y = [10, 20, 30, 40, 50]

    #val = utils.get_corr_val(x, y)
    #print(val)

    y = [1, 10]
    gradient = np.gradient(y)
    print("기울기:", gradient)


def test_df():

    items = [
        {"id": 1, "name": "apple", "price": 1000, "xhms": "130000"},
        {"id": 2, "name": "banana", "price": 1500, "xhms": "130000"},
        {"id": 3, "name": "orange", "price": 2000, "xhms": "130000"},
    ]

    df = pd.DataFrame(items)
    df = df.drop(index=range(2))
    print(df)

if __name__ == "__main__":
    test_df()
