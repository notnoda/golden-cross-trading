import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from trader.kis.stream.tick_chart_storage import KisTickChart

def test():
    tick_chart = get_tick_chart()
    df = tick_chart.get_tick_data(5)
    print(len(df))

    # RSI 계산
    #df['RSIs'] = ta.rsi(df['last'], length=6)
    #df['RSIl'] = ta.rsi(df['last'], length=14)

    # MACD 계산
    macd = ta.macd(df['last'], fast=6, slow=26, signal=8)
    df = pd.concat([df, macd], axis=1)

    # Parabolic SAR 계산
    #sar = ta.psar(df['max'], df['min'])
    #df = pd.concat([df, sar], axis=1)

    print(macd)

def get_tick_chart():
    tick_chart = KisTickChart('tests')

    for i in range(1, 33 * 5):
        if i % 50000 == 0: print(i)
        tick_chart.add_tick_data([
            [f't{str(i).zfill(10)}', i]
        ])

    return tick_chart

def print_time(name):
    now = datetime.now()
    print(f"{name} = {now.hour}:{now.minute}:{now.second}.{now.microsecond}")

if __name__ == '__main__':
    '''
    print_time('>>>>> start')
    tests()
    print_time('>>>>> end')
    '''

    from datetime import datetime
    formatted_date = datetime.now().strftime("%Y%m%d")
    print("포맷된 날짜와 시간:", formatted_date)
