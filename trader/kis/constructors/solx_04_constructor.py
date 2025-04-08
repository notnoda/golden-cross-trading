from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.macd_value_strategy import MacdValueStrategyBuilder
from trader.kis.stream.tick_chart_storage import TickChartStorage
from trader.kis.stream.trading_stream import StockTradingStreamBuilder

# -----------------------------------------------------------------------------
# - SolxOtherConstructor
# -----------------------------------------------------------------------------
class SolxOtherConstructor(BaseConstructor):

    def __init__(self, filename: str):
        super().__init__(filename)

    def get_streamer_object(self, storage_long: TickChartStorage, storage_short: TickChartStorage):
        config = self.get_config()

        return (
            StockTradingStreamBuilder()
            .set_tr_id("HDFSCNT0")
            .set_storages({
                config["socket_long"]:  storage_long,
                config["socket_short"]: storage_short,
            })
            .build()
        )

    def get_strategy_long_object(self, storage: TickChartStorage):
        config = self.get_config()

        return (
            MacdValueStrategyBuilder()
            .set_stock_code(config["stock_long"])
            .set_tick_chart([136, 68, 20])
            .set_storage(storage)
            .set_stock_order(OverseasSingleOrder(
                excg_cd=config["exchange"],
                order_qty=int(config["order_qty"])
            ))
            .build()
        )

    def get_strategy_short_object(self, storage: TickChartStorage):
        config = self.get_config()

        return (
            MacdValueStrategyBuilder()
            .set_stock_code(config["stock_short"])
            .set_tick_chart([68, 34, 10])
            .set_storage(storage)
            .set_stock_order(OverseasSingleOrder(
                excg_cd=config["exchange"],
                order_qty=int(config["order_qty"])
            ))
            .build()
        )

# end of class SolxOtherConstructor
