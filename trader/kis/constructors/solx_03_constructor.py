from trader.kis.constructors.base_constructor import BaseConstructor
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.macd_signal_strategy import MacdSignalStrategyBuilder
from trader.kis.stream.tick_chart_storage import TickChartStorage
from trader.kis.stream.trading_stream import StockTradingStreamBuilder

# -----------------------------------------------------------------------------
# - SolxThirdConstructor
# -----------------------------------------------------------------------------
class SolxThirdConstructor(BaseConstructor):

    def __init__(self, filename: str):
        super().__init__(filename)

    def get_streamer_object(self, storage: TickChartStorage):
        config = self.get_config()

        return (
            StockTradingStreamBuilder()
            .set_tr_id("HDFSCNT0")
            .set_storages({
                config["socket_long"]:  storage,
            })
            .build()
        )

    def get_strategy_object(self, storage: TickChartStorage):
        config = self.get_config()

        return (
            MacdSignalStrategyBuilder()
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

# end of class SolxThirdConstructor
