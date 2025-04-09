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
    #df = utils.add_ichimoku_base(adata.get_test_df())

    #for index, row in df.iterrows():
    #    print(f"{index}:\t{row['close']}\t{row['ichimoku_base']}")

    #data_df = df.iloc[-3:]
    #print(data_df.iloc[0]["open"])

    #for i in range(-1, -10, -1): print(i)

    data = [10, 20, 30, 40, 50]
    for i in range(len(data) - 1, -1, -1): print(data[i])

    '''
    data = np.array([10, 15, 23, 30, 42])
    differences = np.diff(data)
    print(differences)  # [5 8 7 12]

    data = np.array([10, 20, 30, 40, 50])
    average = np.mean(data)
    print(average)  # 30.0

    data = np.array([10, 20, 30, 40, 50])
    std_dev = np.std(data, ddof=1)  # 샘플 표준편차 (Bessel's correction 적용)
    print(std_dev)  # 15.811388300841896
    '''

def math_test():
    angle_threshold = 30  # 기준 각도
    sar_slopes = [10, 15, 20, 25, 30]

    print(sar_slopes[-5:])

    a = -0.0134
    b = -0.0056
    print(a + b)

    '''
    recent_angles = [math.degrees(math.atan(sar_slopes[i])) for i in range(-10, 0)]
    print(recent_angles)

    strong_trend_count = sum(1 for angle in recent_angles if angle > angle_threshold)
    print(strong_trend_count)
    '''

if __name__ == "__main__":
    math_test()
