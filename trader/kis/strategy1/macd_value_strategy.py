import asyncio
import logging
import time

import trader.analyze.analysis_utils as analysis

from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.base_strategy import BaseStrategy
from trader.kis.stream.tick_chart_storage import TickChartStorage

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class MacdValueStrategy(BaseStrategy):
    # 매수/매도 신호
    __ORDER_CLOSE:   str = "closed"
    __CALL_POSITION: str = "call"
    __PUT_POSITION:  str = "put"

    # 주식 매수 가격
    __order_seq_no: int = 0

    def __init__(self, stock_code: str, tick_chart: [int],
                 stock_order: OverseasSingleOrder, storage: TickChartStorage):
        super().__init__(stock_order)
        self.__stock_code: str = stock_code
        self.__storage: TickChartStorage = storage

        self.__tick_count = len(tick_chart)
        self.__tick_chart: (int, int, int) = tick_chart

    def execute(self):
        logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdValueStrategy({self.__stock_code}) ready")
        self.ready()
        logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdValueStrategy({self.__stock_code}) start")

        position = self.__CALL_POSITION

        while True:
            if position == self.__CALL_POSITION:
                position = self.__call_position()
                time.sleep(0.5)
            elif position == self.__PUT_POSITION:
                position = self.__put_position()
                time.sleep(60)
            else:
                logging.info(">>>>>>>>>> closed")
                if position == self.__ORDER_CLOSE: asyncio.run(self.treade_closed())
                break

        logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdValueStrategy({self.__stock_code}) end")

    ################################################################################
    # 매매 시점 판단 가능 여부를 확인 한다.
    ################################################################################
    def ready(self):
        min_tick = analysis.get_min_tick_count()
        tick_val = self.__tick_chart[0]

        while True:
            if self.__storage.is_enough_count(tick_val, min_tick): break
            time.sleep(60)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                values: [float] = []

                for tick in self.__tick_chart:
                    data = analysis.get_analyze_data(self.__storage.get_tick_data(tick))
                    if data.macd_val() <= 0: break
                    values.append(data.macd_val())

                if self.__tick_count == len(values):
                    logging.info("------------------------------------------------------")
                    logging.info(f"buy : [{self.__stock_code}] [{values}]")
                    self.buy_stock(self.__stock_code)
                    logging.info("------------------------------------------------------")
                    return self.__PUT_POSITION
            except Exception as e:
                logging.error(e)

            time.sleep(0.5)

    ###########################################################################
    # Long 매도 시점을 확인 한다.
    ###########################################################################
    def __put_position(self) -> str:
        tick_chart = self.__tick_chart.iloc[-1]
        max_price = self.get_purchase_price() * 1.04

        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                data = analysis.get_analyze_data(self.__storage.get_tick_data(tick_chart))

                if data.close_val() >= max_price or data.macd_val() < 0:
                    logging.info("------------------------------------------------------")
                    logging.info(f"buy : [{self.__stock_code}] [{data.close_val()}, {data.macd_val()}]")
                    self.sell_stock(self.__stock_code)
                    logging.info("------------------------------------------------------")
                    return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)

            time.sleep(0.5)

# end of class MacdValueStrategy

# -----------------------------------------------------------------------------
# MacdValueStrategyBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class MacdValueStrategyBuilder:
    def __init__(self):
        self.stock_code  = None
        self.tick_chart = None
        self.stock_order = None
        self.storage     = None

    def set_stock_code(self, stock_code):
        self.stock_code = stock_code
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
        if not all([self.stock_code, self.tick_chart, self.stock_order, self.storage]):
            raise ValueError("모든 필드를 입력 하세요!")
        return MacdValueStrategy(
            stock_code=self.stock_code,
            tick_chart=self.tick_chart,
            stock_order=self.stock_order,
            storage=self.storage
        )

# end of class MacdValueStrategyBuilder
