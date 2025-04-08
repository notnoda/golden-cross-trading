import logging
import time

import trader.analyze.analysis_utils as analysis

from trader.analyze.analysis_data import AnalysisData
from trader.errors.trading_error import TradingOrderBuyError
from trader.kis.order.overseas_single_order import OverseasSingleOrder
from trader.kis.strategy1.base_strategy import BaseStrategy
from trader.kis.stream.tick_chart_storage import TickChartStorage

# -----------------------------------------------------------------------------
# 두 번째 기본 전략
# -----------------------------------------------------------------------------
class DefaultSingleStrategy(BaseStrategy):
    # 매수/매도 신호
    __ORDER_CLOSE:   str = "closed"
    __CALL_POSITION: str = "call"
    __PUT_POSITION:  str = "put"

    # 주식 매수 가격
    __purchase_price: float = 0.0
    __order_seq_no: int = 0

    def __init__(self, stock_code: str, tick_chart: str, stock_order: OverseasSingleOrder, storage: TickChartStorage):
        super().__init__(stock_order)
        self.__temp_count: int = 0

        self.__stock_code: str = stock_code
        self.__tick_chart: int = int(tick_chart)
        self.__storage: TickChartStorage = storage

    def execute(self):
        logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DefaultSingleStrategy[{self.__stock_code}] ready")
        self.ready()
        logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DefaultSingleStrategy[{self.__stock_code}] start")

        position = self.__CALL_POSITION

        while True:
            if position == self.__CALL_POSITION:
                position = self.__call_position()
            elif position == self.__PUT_POSITION:
                position = self.__put_position()
            else:
                logging.info(">>>>>>>>>> closed")
                self.sell_stock(self.__stock_code)
                break

            time.sleep(0.5)
        logging.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DefaultSingleStrategy[{self.__stock_code}] end")

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
    def __call_position(self) -> str:
        # 0: 주식 종목 코드, 1: 틱의 크기, 2: 변경할 포지션, 3: 틱 데이터
        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                data: AnalysisData = analysis.get_analyze_data(self.__storage.get_tick_data(self.__tick_chart))

                if data.macd() > 0 and data.rsi() > 0 and data.sar() > 0 and data.is_rsi_under(30):
                    logging.info("------------------------------------------------------")
                    logging.info(f"buy : [{self.__stock_code}] [{data.to_str()}]")
                    self.__purchase_price = data.close_val
                    self.buy_stock(self.__stock_code)
                    logging.info("------------------------------------------------------")
                    return self.__PUT_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ###########################################################################
    # 매도 시점을 확인 한다.
    ###########################################################################
    def __put_position(self) -> str:
        while True:
            try:
                if self.__storage.is_closed(): return self.__ORDER_CLOSE
                data: AnalysisData = analysis.get_analyze_data(self.__storage.get_tick_data(self.__tick_chart))

                if data.sar() < 0 and data.is_rsi_over(30):
                    logging.info("------------------------------------------------------")
                    logging.info(f"sell : [{self.__stock_code}] [{data.to_str()}]")
                    self.sell_stock(self.__stock_code)
                    logging.info("------------------------------------------------------")
                    return self.__CALL_POSITION
            except TradingOrderBuyError as e:
                logging.error(e)
                time.sleep(0.5)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

# end of class DefaultSecondStrategy

# -----------------------------------------------------------------------------
# DefaultSingleStrategyBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class DefaultSingleStrategyBuilder:
    def __init__(self):
        self.stock_code  = None
        self.tick_chart  = None
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
        return DefaultSingleStrategy(
            stock_code=self.stock_code,
            tick_chart=self.tick_chart,
            stock_order=self.stock_order,
            storage=self.storage
        )

# end of class DefaultSingleStrategyBuilder
