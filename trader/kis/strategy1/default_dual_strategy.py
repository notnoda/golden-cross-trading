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
# 첫 번째 기본 전략
# 466 틱봉의 MACD로 매수 판단
# -----------------------------------------------------------------------------
class DefaultDualStrategy(BaseStrategy):
    # 매수/매도 신호
    __ORDER_CLOSE:    str = "closed"
    __CALL_POSITION:  str = "call"
    __LONG_POSITION:  str = "long"
    __SHORT_POSITION: str = "short"

    # 주식 매수 가격
    __purchase_price: float = 0.0
    __order_seq_no: int = 0

    def __init__(self, stock_long: str, stock_short: str, tick_macd: str, tick_long: str, tick_short: str,
                 stock_order: OverseasSingleOrder, storage_long: TickChartStorage, storage_short: TickChartStorage):
        super().__init__(stock_order)
        self.__temp_count: int = 0

        self.__stock_long:  str = stock_long
        self.__stock_short: str = stock_short
        self.__tick_macd:   int = int(tick_macd)
        self.__tick_long:   int = int(tick_long)  # 장기 틱봉
        self.__tick_short:  int = int(tick_short) # 단기 틱봉

        self.__storage_long:  TickChartStorage = storage_long
        self.__storage_short: TickChartStorage = storage_short

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DefaultDualStrategy ready")
        self.check()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DefaultDualStrategy start")

        position = self.__CALL_POSITION

        while True:
            if position == self.__CALL_POSITION:
                position = self.__call_position()
            elif position == self.__LONG_POSITION:
                position = self.__put_position(self.__stock_long, self.__tick_long)
            elif position == self.__SHORT_POSITION:
                position = self.__put_position(self.__stock_short, self.__tick_short)
            else:
                logging.info(">>>>>>>>>> closed")
                if position == self.__ORDER_CLOSE: asyncio.run(self.treade_closed())
                break

            time.sleep(0.5)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DefaultDualStrategy end")

    ################################################################################
    # 매매 시점 판단 가능 여부를 확인 한다.
    ################################################################################
    def check(self):
        while True:
            if self.__storage_long.get_next_step() == "default": return
            time.sleep(30)

    def ready(self):
        min_tick = analysis.get_min_tick_count()
        is_enough_long = False
        is_enough_short = False
        is_after_time = True

        while True:
            if self.__storage_long.is_enough_count(self.__tick_long, min_tick): is_enough_long = True
            if self.__storage_short.is_enough_count(self.__tick_short, min_tick): is_enough_short = True
            if is_enough_long and is_enough_short and is_after_time: break
            time.sleep(30)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        # 0: 주식 종목 코드, 1: 틱의 크기, 2: 변경할 포지션, 3: 틱 데이터
        while True:
            try:
                if self.is_closed(): return self.__ORDER_CLOSE
                mdata: AnalysisData = analysis.get_analyze_macd_last(self.__storage_long.get_tick_data(self.__tick_macd))
                if mdata.macd_val != mdata.macd_signal:
                    logging.info("------------------------------------------------------")
                    logging.info(f"macd : [{mdata.to_str()}]")
                    logging.info("------------------------------------------------------")

                if mdata.macd() > 0:
                    return self.__call_position_stock(self.__stock_long, self.__tick_long)
                elif mdata.macd() < 0:
                    return self.__call_position_stock(self.__stock_short, self.__tick_short)
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ################################################################################
    # 중지 여부를 확인 한다.
    ################################################################################
    def is_closed(self) -> bool:
        return self.__storage_long.is_closed()

    ################################################################################
    # 주식의 매수 시점을 판단 한다.
    # (Macd > Macd Singnal) and (Rsi 단기선 > 장기선) and (Sar 상승신호)
    ################################################################################
    def __call_position_stock(self, stock_code: str, tick_chart):
        storage = self.__storage_long if self.__stock_long == stock_code else self.__storage_short

        while True:
            try:
                if self.is_closed(): return self.__ORDER_CLOSE
                data: AnalysisData = analysis.get_analyze_data(storage.get_tick_data(tick_chart))

                if data.macd() > 0 and data.rsi() > 0 and data.sar() > 0:
                    logging.info("------------------------------------------------------")
                    logging.info(f"buy : [{stock_code}] [{data.to_str()}]")
                    self.__purchase_price = data.close_val
                    self.buy_stock(stock_code)
                    logging.info("------------------------------------------------------")
                    return self.__LONG_POSITION if self.__stock_long == stock_code else self.__SHORT_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ###########################################################################
    # 매도 시점을 확인 한다.
    ###########################################################################
    def __put_position(self, stock_code: str, tick_chart) -> str:
        storage = self.__storage_long if self.__stock_long == stock_code else self.__storage_short

        while True:
            try:
                if self.is_closed(): return self.__ORDER_CLOSE
                data: AnalysisData = analysis.get_analyze_data(storage.get_tick_data(tick_chart))

                if data.sar() < 0:
                    logging.info("------------------------------------------------------")
                    logging.info(f"sell : [{stock_code}] [{data.to_str()}]")
                    self.sell_stock(stock_code)
                    logging.info("------------------------------------------------------")
                    return self.__CALL_POSITION
            except TradingOrderBuyError as e:
                logging.error(e)
                time.sleep(0.5)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

# end of class DefaultDualStrategy

# -----------------------------------------------------------------------------
# DefaultDualStrategyBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class DefaultDualStrategyBuilder:
    def __init__(self):
        self.stock_long  = None
        self.stock_short = None
        self.tick_macd   = None
        self.tick_long   = None
        self.tick_short  = None
        self.stock_order   = None
        self.storage_long  = None
        self.storage_short = None

    def set_stock_long(self, stock_long):
        self.stock_long = stock_long
        return self

    def set_stock_short(self, stock_short):
        self.stock_short = stock_short
        return self

    def set_tick_macd(self, tick_macd):
        self.tick_macd = tick_macd
        return self

    def set_tick_long(self, tick_long):
        self.tick_long = tick_long
        return self

    def set_tick_short(self, tick_short):
        self.tick_short = tick_short
        return self

    def set_stock_order(self, stock_order):
        self.stock_order = stock_order
        return self

    def set_storage_long(self, storage_long):
        self.storage_long = storage_long
        return self

    def set_storage_short(self, storage_short):
        self.storage_short = storage_short
        return self

    def build(self):
        if not all([self.stock_long, self.stock_short, self.tick_macd, self.tick_long, self.tick_short, self.stock_order, self.storage_long, self.storage_short]):
            raise ValueError("모든 필드를 입력 하세요!")
        return DefaultDualStrategy(
            stock_long=self.stock_long,
            stock_short=self.stock_short,
            tick_macd=self.tick_macd,
            tick_long=self.tick_long,
            tick_short=self.tick_short,
            stock_order=self.stock_order,
            storage_long=self.storage_long,
            storage_short=self.storage_short
        )

# end of class DefaultDualStrategyBuilder
