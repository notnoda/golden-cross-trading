import math
import numpy as np
import pandas as pd
import pandas_ta as ta

from trader.analyze.analysis_data import AnalysisData

def get_min_tick_count():
    return 26 + 9 - 1

################################################################################
# MACD, RSI, PSAR 값을 반환 한다.
################################################################################
def get_analyze_df(df):
    # MACD 계산
    df_data = add_analyze_macd(df)

    # RSI 계산
    df_data["rsi_long"] = ta.rsi(df["close"], length=14) # 장기선
    df_data["rsi_short"] = ta.rsi(df["close"], length=6)  # 단기선

    # Parabolic SAR 계산
    return add_analyze_sar(df_data)

################################################################################
# MACD 값을 반환 한다.
################################################################################
def add_analyze_macd(df):
    macd_df = get_analyze_macd(df)
    return pd.concat([df, macd_df], axis=1)

def get_analyze_macd(df):
    macd_df = ta.macd(df["close"], fast=12, slow=26, signal=9)
    diffs = []
    indexs = []
    prev_histo = np.nan
    prev_diff = np.nan
    index_val = np.nan

    for index, row in macd_df.iterrows():
        if math.isnan(row['MACDh_12_26_9']) or math.isnan(prev_histo):
            diffs.append(np.nan)
            indexs.append(np.nan)
        else:
            this_diff = row['MACDh_12_26_9'] - prev_histo
            diffs.append(this_diff)

            if math.isnan(index_val): index_val = 1
            elif prev_diff > 0 > this_diff or prev_diff < 0 < this_diff: index_val = 1
            else: index_val += 1

            sign = 1 if this_diff >= 0 else -1
            indexs.append(index_val * sign)

            prev_diff = this_diff

        prev_histo = row["MACDh_12_26_9"]

    return pd.DataFrame({
        "macd_val": macd_df["MACD_12_26_9"],
        "macd_signal": macd_df["MACDs_12_26_9"],
        "macd_histo": macd_df["MACDh_12_26_9"],
        "macd_diff": diffs,
        "macd_index": indexs,
    })

################################################################################
# PSAR 값을 반환 한다.
################################################################################
def add_analyze_sar(df):
    sar_df = get_analyze_sar(df)
    return pd.concat([df, sar_df], axis=1)

def get_analyze_sar(df):
    temp_df = ta.psar(df["high"], df["low"])
    return pd.DataFrame({
        "sar_long": temp_df["PSARl_0.02_0.2"],
        "sar_short": temp_df["PSARs_0.02_0.2"],
        "sar_af": temp_df["PSARaf_0.02_0.2"],
        "sar_r": temp_df["PSARr_0.02_0.2"],
    })

def get_sar_values(df):
    sar_df = get_analyze_sar(df)
    sar_values = []

    for index, row in sar_df.iterrows():
        if row["sar_long"] > 0: sar_values.append(row["sar_long"])
        else: sar_values.append(row["sar_short"])

    sar_df["sar_values"] = sar_values
    return sar_df

################################################################################
# 평균 이동 값을 반환 한다.
################################################################################
def add_analyze_sma(df, length=5):
    sma_df = get_analyze_sma(df, length)
    df["sma"] = sma_df
    return df

def get_analyze_sma(df, length=5):
    return ta.sma(df["close"], length)

def get_corr_val(x, y):
    correlation_matrix = np.corrcoef(x, y)
    return correlation_matrix

################################################################################
# 일목균형표 값을 반환 한다.
################################################################################
def add_ichimoku_base(df, base_period=26):
    df["ichimoku_base"] = get_ichimoku_base(df, base_period)
    return df

def get_ichimoku_base(df, base_period=26):
    return (df["high"].rolling(window=base_period).max() + df["low"].rolling(window=base_period).min()) / 2

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

################################################################################
# 마지막 데이터의 open, close, high, low, MACD, RSI, PSAR 값을 반환 한다.
################################################################################
def get_analyze_data(df):
    data_df = get_analyze_df(df)
    return transform_data(data_df.iloc[-1])

def get_analyze_tail(df, n=5):
    data_df = get_analyze_df(df)
    data = []

    for item in data_df.tail(n):
        data.append(transform_data(item))

    return data

################################################################################
# 데이터를 변환한다.
################################################################################
def transform_data(data):
    psar_long = data["PSARl_0.02_0.2"]
    psar_short = data["PSARs_0.02_0.2"]

    return AnalysisData(
        open_val=data["open"],
        high_val=data["high"],
        low_val=data["low"],
        close_val=data["close"],
        macd_val=data["MACD_12_26_9"],
        macd_signal=data["MACDs_12_26_9"],
        macd_histo=data["MACDh_12_26_9"],
        rsi_long=data["RSIl"],
        rsi_short=data["RSIs"],
        psar_long=(0.0 if math.isnan(psar_long) else psar_long),
        psar_short=(0.0 if math.isnan(psar_short) else psar_short),
    )

################################################################################
# MACD 값을 반환 한다.
################################################################################
def get_analyze_macd_last(df):
    macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
    data = pd.concat([df, macd], axis=1).iloc[-1]

    return AnalysisData(
        open_val=data["open"],
        high_val=data["high"],
        low_val=data["low"],
        close_val=data["close"],
        macd_val=data["MACD_12_26_9"],
        macd_signal=data["MACDs_12_26_9"]
    )
