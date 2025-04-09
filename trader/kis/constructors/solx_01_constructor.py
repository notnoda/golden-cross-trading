from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy.ichimoku_strategy import IchimokuStrategy
from trader.kis.chart.chart import ApiChart

class SolxFirstConstructor(BaseConstructor):

    def __init__(self, filename: str):
        super().__init__(filename)

    def get_strategy_object(self):
        config = self.get_config()

        return IchimokuStrategy(
            stock_order=OverseasSingleOrder(
                exchange=config["exchange"],
                order_qty=int(config["order_qty"])
            ),
            storage=ApiChart(code=config["stock_long"], name=config["socket_long"]),
            short_code=config["stock_short"]
        )

# end of class SolxFirstConstructor
