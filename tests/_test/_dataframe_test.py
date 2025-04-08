import time
from datetime import datetime
from trader.kis.stream.tick_chart_storage import KisTickChart

def test():
    tick_chart = get_tick_chart()
    print_time('>>>>> 데이터 생성 완료')
    index = 1

    while True:
        print_time('>>>>> 데이터{index} start')
        df = tick_chart.get_tick_data(466)
        print_time('>>>>> 데이터{index} end')
        #print(df)
        index += 1
        if index > 1000: break
        time.sleep(0.5)

def get_tick_chart():
    tick_chart = KisTickChart('tests')

    for i in range(1, 120000):
        if i % 50000 == 0: print(i)
        tick_chart.add_tick_data([
            [f't{str(i).zfill(10)}', i]
        ])

    return tick_chart

def print_time(name):
    now = datetime.now()
    print(f"{name} = {now.hour}:{now.minute}:{now.second}.{now.microsecond}")

if __name__ == '__main__':
    print_time('>>>>> start')
    test()
    print_time('>>>>> end')
