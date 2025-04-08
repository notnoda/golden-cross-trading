import asyncio
import logging
import time

import trader.analyze.analysis_utils as analysis

from trader.analyze.analysis_data import AnalysisData
from trader.errors.trading_error import TradingOrderBuyError
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.base_strategy import BaseStrategy
from trader.kis.stream.tick_chart_storage import TickChartStorage

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class MacdSignalStrategy(BaseStrategy):
    # 매수/매도 신호
    __ORDER_CLOSE:    str = "closed"
    __CALL_POSITION:  str = "call"
    __LONG_POSITION:  str = "long"
    __SHORT_POSITION: str = "short"

    # 주식 매수 가격
    __order_seq_no: int = 0

    def __init__(self, stock_long: str, stock_short: str, tick_chart: str,
                 stock_order: OverseasSingleOrder, storage: TickChartStorage):
        super().__init__(stock_order)
        self.__stock_long:  str = stock_long
        self.__stock_short: str = stock_short
        self.__tick_chart:  int = int(tick_chart)
        self.__storage: TickChartStorage = storage

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VolatilityStrategy ready")
        self.ready()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VolatilityStrategy start")

        position = self.__CALL_POSITION

        while True:
            if position == self.__CALL_POSITION:
                position = self.__check_call_position()
            elif position == self.__LONG_POSITION:
                position = self.__check_put_long()
            elif position == self.__SHORT_POSITION:
                position = self.__check_put_short()
            else:
                logging.info(">>>>>>>>>> closed")
                if position == self.__ORDER_CLOSE: asyncio.run(self.treade_closed())
                break

            time.sleep(0.5)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VolatilityStrategy end")

    ################################################################################
    # 매매 시점 판단 가능 여부를 확인 한다.
    ################################################################################
    def ready(self):
        min_tick = analysis.get_min_tick_count()

        while True:
            if self.__storage.is_enough_count(self.__tick_chart, min_tick): break
            time.sleep(60)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __check_call_position(self):
        # 0: 주식 종목 코드, 1: 틱의 크기, 2: 변경할 포지션, 3: 틱 데이터
        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                df = analysis.get_analyze_df(self.__storage.get_tick_data(self.__tick_chart))
                prev_data: AnalysisData = analysis.transform_data(df.iloc[-2])
                last_data: AnalysisData = analysis.transform_data(df.iloc[-1])

                if last_data.macd_val() > 0 > prev_data.macd_val():
                    logging.info("------------------------------------------------------")
                    self.__print_signal("buy", self.__stock_long, prev_data, last_data)
                    self.buy_stock(self.__stock_long)
                    logging.info("------------------------------------------------------")
                    return self.__LONG_POSITION
                elif last_data.macd_val() < 0 < prev_data.macd_val():
                    logging.info("------------------------------------------------------")
                    self.__print_signal("buy", self.__stock_long, prev_data, last_data)
                    self.buy_stock(self.__stock_short)
                    logging.info("------------------------------------------------------")
                    return self.__SHORT_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ################################################################################
    # 매수/매도 시점의 신호를 출력 한다.
    ################################################################################
    def __print_signal(self, trade: str, stock_code: str, pdata: AnalysisData, ldata: AnalysisData):
        logging.info(f"{trade} : [{stock_code}] [{pdata.to_str()}] [{ldata.to_str()}]")

    ###########################################################################
    # Long 매도 시점을 확인 한다.
    ###########################################################################
    def __check_put_long(self) -> str:
        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                df = analysis.get_analyze_df(self.__storage.get_tick_data(self.__tick_chart))
                prev_data: AnalysisData = analysis.transform_data(df.iloc[-2])
                last_data: AnalysisData = analysis.transform_data(df.iloc[-1])

                if last_data.macd_val() < 0 < prev_data.macd_val():
                    logging.info("------------------------------------------------------")
                    self.__print_signal("sell", self.__stock_long, prev_data, last_data)
                    self.sell_stock(self.__stock_long)
                    self.buy_stock(self.__stock_short)
                    logging.info("------------------------------------------------------")
                    return self.__SHORT_POSITION
                time.sleep(0.5)
            except TradingOrderBuyError as e:
                logging.error(e)
                time.sleep(0.5)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
                time.sleep(0.5)

        return ""

    ###########################################################################
    # Short 매도 시점을 확인 한다.
    ###########################################################################
    def __check_put_short(self) -> str:
        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                df = analysis.get_analyze_df(self.__storage.get_tick_data(self.__tick_chart))
                prev_data: AnalysisData = analysis.transform_data(df.iloc[-2])
                last_data: AnalysisData = analysis.transform_data(df.iloc[-1])

                if last_data.macd_val() > 0 > prev_data.macd_val():
                    logging.info("------------------------------------------------------")
                    self.__print_signal("sell", self.__stock_short, prev_data, last_data)
                    self.sell_stock(self.__stock_short)
                    self.buy_stock(self.__stock_long)
                    logging.info("------------------------------------------------------")
                    return self.__LONG_POSITION
                time.sleep(0.5)
            except TradingOrderBuyError as e:
                logging.error(e)
                time.sleep(0.5)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
                time.sleep(0.5)

        return ""

# end of class MacdSignalStrategy

# -----------------------------------------------------------------------------
# MacdSignalStrategyBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class MacdSignalStrategyBuilder:
    def __init__(self):
        self.stock_long  = None
        self.stock_short = None
        self.tick_chart  = None
        self.stock_order = None
        self.storage     = None

    def set_stock_long(self, stock_long):
        self.stock_long = stock_long
        return self

    def set_stock_short(self, stock_short):
        self.stock_short = stock_short
        return self

    def set_tick_chart(self, tick_chart):
        self.tick_chart = tick_chart
        return self

    def set_stock_order(self, stock_order):
        self.stock_order = stock_order
        return self

    def set_storage(self, storage):
        self.storage = storage
        return self

    def build(self):
        if not all([self.stock_long, self.stock_short, self.tick_chart, self.stock_order, self.storage]):
            raise ValueError("모든 필드를 입력 하세요!")
        return MacdSignalStrategy(
            stock_long=self.stock_long,
            stock_short=self.stock_short,
            tick_chart=self.tick_chart,
            stock_order=self.stock_order,
            storage=self.storage
        )

# end of class MacdSignalStrategyBuilder
