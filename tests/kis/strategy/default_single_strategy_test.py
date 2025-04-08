import tests.const.test_data_values as conf
import tests.kis.stream.tick_chart_storage_test as test_data

from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.default_single_strategy import DefaultSingleStrategyBuilder

def execute():
    strategy = get_strategy()
    strategy.execute()

def get_strategy():
    is_real: bool = True # 실전: True, 모의: False
    config = conf.get_test_config(is_real)
    storage = test_data.get_storage("tests", 2400)

    return (
        DefaultSingleStrategyBuilder()
        .set_stock_code(config["stock_long"])
        .set_tick_chart(config["tick_long"])
        .set_storage(storage)
        .set_stock_order(OverseasSingleOrder(
            excg_cd=config["exchange"],
            order_qty=int(config["order_qty"])
        ))
        .build()
    )

if __name__ == "__main__":
    execute()
