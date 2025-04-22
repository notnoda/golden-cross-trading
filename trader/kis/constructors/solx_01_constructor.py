from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy.macd_histogram_strategy import MacdHistogramStrategy
from trader.kis.chart.chart import MinuteChart

class SolxFirstConstructor(BaseConstructor):

    def __init__(self, filename: str):
        super().__init__(filename)

    def get_strategy_object(self):
        config = self.get_config()

        return MacdHistogramStrategy(
            stock_order=OverseasSingleOrder(
                exchange=config["exchange"],
                order_qty=int(config["order_qty"])
            ),
            storage_long=MinuteChart(code=config["stock_long"], exchange=config["exchange"]),
            storage_shrt=MinuteChart(code=config["stock_short"], exchange=config["exchange"])
        )

# end of class SolxFirstConstructor
