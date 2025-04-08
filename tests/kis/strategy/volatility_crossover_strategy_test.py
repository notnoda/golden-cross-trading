import tests.const.test_data_values as conf
import tests.kis.stream.tick_chart_storage_test as test_data

from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.volatility_crossover_strategy import VolatilityCrossoverStrategyBuilder

def execute():
    strategy = get_strategy()
    strategy.execute()

def get_strategy():
    is_real: bool = True # 실전: True, 모의: False
    config = conf.get_test_config(is_real)
    storage = test_data.get_storage("tests", 2)

    return (
        VolatilityCrossoverStrategyBuilder()
        .set_stock_long(config["stock_long"])
        .set_stock_short(config["stock_short"])
        .set_tick_macd(config["tick_macd"])
        .set_tick_long(config["tick_long"])
        .set_tick_short(config["tick_short"])
        .set_storage_long(storage)
        .set_storage_short(storage)
        .set_stock_order(OverseasSingleOrder(
            excg_cd=config["exchange"],
            order_qty=int(config["tick_long"])
        ))
        .build()
    )

if __name__ == "__main__":
    execute()
