from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy.dynamic_strategy import DynamicStrategy
from trader.kis.chart.chart import ApiChart

# -----------------------------------------------------------------------------
# - SolxFirstConstructor
# -----------------------------------------------------------------------------
class SolxFirstConstructor(BaseConstructor):

    def __init__(self, filename: str):
        super().__init__(filename)

    def get_strategy_object(self):
        config = self.get_config()

        return DynamicStrategy(
            stock_order=OverseasSingleOrder(
                exchange=config["exchange"],
                order_qty=int(config["order_qty"])
            ),
            storages=[
                ApiChart(code=config["stock_long"], name=config["socket_long"]),
                ApiChart(code=config["stock_short"], name=config["socket_short"]),
            ]
        )

# end of class SolxFirstConstructor
