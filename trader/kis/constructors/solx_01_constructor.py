from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy.strategy_20250507_01 import Strategy_20250507_01
from trader.kis.chart.chart import MinuteChart, ApiChart


class SolxFirstConstructor(BaseConstructor):

    def __init__(self, filename: str):
        super().__init__(filename)

    def get_strategy_object(self):
        config = self.get_config()

        return Strategy_20250507_01(
            stock_order=OverseasSingleOrder(
                exchange=config["exchange"],
                order_qty=int(config["order_qty"])
            ),
            storage_long=MinuteChart(code=config["stock_long"], exchange=config["exchange"]),
            storage_shrt=MinuteChart(code=config["stock_short"], exchange=config["exchange"])
        )

#storage_api_long = ApiChart(code=config["stock_long"], name=config["socket_long"]),
#storage_api_shrt = ApiChart(code=config["stock_short"], name=config["socket_short"])

# end of class SolxFirstConstructor
