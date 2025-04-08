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
# 변동성 교차 전략
# -----------------------------------------------------------------------------
class VolatilityCrossoverStrategy(BaseStrategy):
    # 매수/매도 신호
    __ORDER_CLOSE:    str = "closed"
    __CALL_POSITION:  str = "call"
    __LONG_POSITION:  str = "long"
    __SHORT_POSITION: str = "short"

    # 주식 매수 가격
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
        is_enough_long = False
        is_enough_short = False
        is_after_time = True

        while True:
            if self.__storage_long.is_enough_count(self.__tick_long, min_tick): is_enough_long = True
            if self.__storage_short.is_enough_count(self.__tick_short, min_tick): is_enough_short = True
            if is_enough_long and is_enough_short and is_after_time: break
            time.sleep(60)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __check_call_position(self):
        # 0: 주식 종목 코드, 1: 틱의 크기, 2: 변경할 포지션, 3: 틱 데이터
        while True:
            try:
                if self.is_closed(): return self.__ORDER_CLOSE
                ldata: AnalysisData = analysis.get_analyze_data(self.__storage_long.get_tick_data(self.__tick_long))
                sdata: AnalysisData = analysis.get_analyze_data(self.__storage_short.get_tick_data(self.__tick_short))

                if self.__rise_signal(ldata, sdata):
                    logging.info("------------------------------------------------------")
                    self.__print_signal("buy", self.__stock_long, ldata, sdata)
                    self.buy_stock(self.__stock_long)
                    logging.info("------------------------------------------------------")
                    return self.__LONG_POSITION
                elif self.__decline_signal(ldata, sdata):
                    logging.info("------------------------------------------------------")
                    self.__print_signal("buy", self.__stock_long, ldata, sdata)
                    self.buy_stock(self.__stock_short)
                    logging.info("------------------------------------------------------")
                    return self.__SHORT_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ################################################################################
    # 중지 여부를 확인 한다.
    ################################################################################
    def is_closed(self) -> bool:
        if not self.__storage_long.is_enough_count(self.__tick_macd): return False
        if not self.__storage_short.is_enough_count(self.__tick_short): return False
        self.__storage_long.set_next_step("default")
        return True

    ################################################################################
    # 매수/매도 시점의 신호를 출력 한다.
    ################################################################################
    def __print_signal(self, trade: str, stock_code: str, ldata: AnalysisData, sdata: AnalysisData):
        logging.info(f"{trade} : [{stock_code}] [{ldata.to_str()}] [{sdata.to_str()}]")

    ###########################################################################
    # 주가 상승 신호 여부를 확인 한다.
    ###########################################################################
    def __rise_signal(self, ldata: AnalysisData, sdata: AnalysisData) -> bool:
            return (ldata.macd() > 0 # MACD > 시그널 선
                and ldata.rsi() > 0 # RSI 단기선 > RSI 장기선
                and ldata.sar() > 0 # SAR 상승 신호(장기선 > 0)
                and sdata.macd() < 0 # MACD < 시그널 선
                and sdata.rsi() < 0 # RSI 단기선 < RSI 장기선
                and sdata.sar() < 0) # SAR 하락 신호(단기선 > 0)

    ###########################################################################
    # 주가 하락 신호 여부를 확인 한다.
    ###########################################################################
    def __decline_signal(self, ldata: AnalysisData, sdata: AnalysisData) -> bool:
            return (ldata.macd() < 0 # MACD < 시그널 선
                    and ldata.rsi() < 0 # RSI 단기선 < RSI 장기선
                    and ldata.sar() < 0 # SAR 하락 신호(단기선 > 0)
                    and sdata.macd() > 0 # MACD > 시그널 선
                    and sdata.rsi() > 0 # RSI 단기선 > RSI 장기선
                    and sdata.sar() > 0) # SAR 상승 신호(장기선 > 0)

    ###########################################################################
    # Long 매도 시점을 확인 한다.
    ###########################################################################
    def __check_put_long(self) -> str:
        while True:
            try:
                if self.is_closed(): return self.__ORDER_CLOSE
                ldata: AnalysisData = analysis.get_analyze_data(self.__storage_long.get_tick_data(self.__tick_long))
                sdata: AnalysisData = analysis.get_analyze_data(self.__storage_short.get_tick_data(self.__tick_short))

                if not self.__decline_signal(ldata, sdata):
                    time.sleep(0.5)
                    continue

                logging.info("------------------------------------------------------")
                self.__print_signal("sell", self.__stock_long, ldata, sdata)
                self.sell_stock(self.__stock_long)
                self.buy_stock(self.__stock_short)
                logging.info("------------------------------------------------------")
                return self.__SHORT_POSITION
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
                if self.is_closed(): return self.__ORDER_CLOSE
                ldata: AnalysisData = analysis.get_analyze_data(self.__storage_long.get_tick_data(self.__tick_long))
                sdata: AnalysisData = analysis.get_analyze_data(self.__storage_short.get_tick_data(self.__tick_short))

                if not self.__rise_signal(ldata, sdata):
                    time.sleep(0.5)
                    continue

                logging.info("------------------------------------------------------")
                self.__print_signal("sell", self.__stock_short, ldata, sdata)
                self.sell_stock(self.__stock_short)
                self.buy_stock(self.__stock_long)
                logging.info("------------------------------------------------------")
                return self.__LONG_POSITION
            except TradingOrderBuyError as e:
                logging.error(e)
                time.sleep(0.5)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
                time.sleep(0.5)

        return ""

# end of class VolatilityCrossoverStrategy

# -----------------------------------------------------------------------------
# VolatilityCrossoverStrategyBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class VolatilityCrossoverStrategyBuilder:
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
        return VolatilityCrossoverStrategy(
            stock_long=self.stock_long,
            stock_short=self.stock_short,
            tick_macd=self.tick_macd,
            tick_long=self.tick_long,
            tick_short=self.tick_short,
            stock_order=self.stock_order,
            storage_long=self.storage_long,
            storage_short=self.storage_short
        )

# end of class VolatilityCrossoverStrategyBuilder
