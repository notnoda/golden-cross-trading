import tests.const.test_data_values as conf

from trader.kis.stream.tick_chart_storage import TickChartStorage
from trader.kis.stream.trading_stream import StockTradingStreamBuilder

def execute():
    get_streamer().execute()

def get_streamer():
    is_real: bool = True # 실전: True, 모의: False
    conf.get_test_config(is_real)

    storages = {
        #"005930": TickChartStorage("SAMSUNG"),
        "RAMSSOXL": TickChartStorage("RAMSSOXL"),
    }

    builder = StockTradingStreamBuilder()
    return (
        builder
        .set_tr_id("HDFSCNT0") #H0STCNT0
        .set_storages(storages)
        .build()
    )

if __name__ == "__main__":
    execute()
