import asyncio
import tests.const.test_data_values as conf

from trader.kis.chart.chart import MinuteChart

async def minute_chart(exchange, code):
    chart = MinuteChart(exchange, code)
    df = chart.get_df()

    for data in df:
        print()

if __name__ == "__main__":
    is_real: bool = True # 실전: True, 모의: False
    config = conf.get_test_config(is_real)

    exchange = "AMS"
    code = "SOXS"

    minute_chart(exchange, code)
