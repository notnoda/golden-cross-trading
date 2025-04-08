from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.default_single_strategy import DefaultSingleStrategyBuilder
from trader.kis.stream.tick_chart_storage import TickChartStorage
from trader.kis.stream.trading_stream import StockTradingStreamBuilder

# -----------------------------------------------------------------------------
# - SolxSecondConstructor
# -----------------------------------------------------------------------------
class SolxSecondConstructor(BaseConstructor):

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

    def get_default_long_object(self, storage: TickChartStorage):
        config = self.get_config()

        return (
            DefaultSingleStrategyBuilder()
            .set_stock_long(config["stock_long"])
            .set_stock_short(config["stock_short"])
            .set_tick_chart(config["tick_long"])
            .set_storage(storage)
            .set_stock_order(OverseasSingleOrder(
                excg_cd=config["exchange"],
                order_qty=int(config["order_qty"])
            ))
            .build()
        )

    def get_default_short_object(self, storage: TickChartStorage):
        config = self.get_config()

        return (
            DefaultSingleStrategyBuilder()
            .set_stock_code(config["stock_short"])
            .set_tick_chart(config["tick_short"])
            .set_storage(storage)
            .set_stock_order(OverseasSingleOrder(
                excg_cd=config["exchange"],
                order_qty=int(config["order_qty"])
            ))
            .build()
        )

# end of class SolxSecondConstructor
