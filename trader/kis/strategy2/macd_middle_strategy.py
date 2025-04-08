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
# 1. SOXL 3분봉(또는 466틱봉)이 'MACD > 0' 이면 SOXL 선택, 'MACD < 0' 이면 SOXS 선택
# 2. 선택한 종목의 MACD 히스토그램 중간 값을 구한다.
#    1) 이전 틱봉의 중간 값을 구한다. ((macd값(-60)-signal선값(-55)) / 2)  <예:결과는 -57.5>
#    2) 두번째 전의 틱봉 중간 값을 구한다. ((macd값-signal선값) / 2)
# -----------------------------------------------------------------------------
class MacdMiddleStrategy(BaseStrategy):
    # 매수/매도 신호
    __ORDER_CLOSE:    str = "closed"
    __CALL_POSITION:  str = "call"
    __LONG_POSITION:  str = "long"
    __SHORT_POSITION: str = "short"

    # 주식 매수 가격
    __order_seq_no: int = 0

    def __init__(self, stock_long, stock_short, chart, stock_order):
        super().__init__(stock_order)
        self.__stock_long  = stock_long
        self.__stock_short = stock_short
        self.__chart = chart

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdMiddleStrategy start")

        position = self.__CALL_POSITION

        while True:
            if position == self.__CALL_POSITION:
                position = self.__call_position()
            elif position == self.__LONG_POSITION:
                position = self.__long_position()
            elif position == self.__SHORT_POSITION:
                position = self.__short_position()
            else:
                logging.info(">>>>>>>>>> closed")
                if position == self.__ORDER_CLOSE: asyncio.run(self.treade_closed())
                break

            time.sleep(0.5)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdMiddleStrategy end")

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        # 0: 주식 종목 코드, 1: 틱의 크기, 2: 변경할 포지션, 3: 틱 데이터
        while True:
            try:
                tdata = analysis.get_analyze_tail(df=self.__chart.get_df(), n=3)
                macd_val = tdata[2].macd_val

                if self.is_closed(): return self.__ORDER_CLOSE
                if macd_val > 0 and self.__rise_signal(tdata[0], tdata[1]):
                    logging.info("------------------------------------------------------")
                    self.__print_signal("buy", self.__stock_long, macd_val, tdata[0].macd_histogram(), tdata[1].macd_histogram())
                    self.buy_stock(self.__stock_long)
                    logging.info("------------------------------------------------------")
                    return self.__LONG_POSITION
                elif macd_val < 0 and  self.__decline_signal(tdata[0], tdata[1]):
                    logging.info("------------------------------------------------------")
                    self.__print_signal("buy", self.__stock_short, macd_val, tdata[0].macd_histogram(), tdata[1].macd_histogram())
                    self.buy_stock(self.__stock_short)
                    logging.info("------------------------------------------------------")
                    return self.__SHORT_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ################################################################################
    # 중지 여부를 확인 한다.
    ################################################################################
    def is_closed(self): return self.__chart.is_closed()

    ###########################################################################
    # 주가 상승 신호 여부를 확인 한다.
    ###########################################################################
    def __rise_signal(self, data1, data2):
            return data1.macd_histogram() > 0 and data2.macd_histogram() > 0

    ###########################################################################
    # 주가 하락 신호 여부를 확인 한다.
    ###########################################################################
    def __decline_signal(self, data1, data2):
            return data1.macd_histogram() < 0 and data2.macd_histogram() < 0

    ################################################################################
    # 매수/매도 시점의 신호를 출력 한다.
    ################################################################################
    def __print_signal(self, trade, code, macd, histogram1, histogram2):
        logging.info(f"{trade} : [{code}] [{macd}] [{histogram1}] [{histogram2}]")

    ###########################################################################
    # Long 매도 시점을 확인 한다.
    ###########################################################################
    def __long_position(self):
        while True:
            try:
                tdata = analysis.get_analyze_tail(df=self.__chart.get_df(), n=3)

                if self.is_closed(): return self.__ORDER_CLOSE
                if not self.__decline_signal(tdata[0], tdata[1]):
                    logging.info("------------------------------------------------------")
                    self.__print_signal("sell", self.__stock_long, 0, tdata[0].macd_histogram(), tdata[1].macd_histogram())
                    self.sell_stock(self.__stock_long)
                    logging.info("------------------------------------------------------")
                    return self.__CALL_POSITION
            except TradingOrderBuyError as e:
                logging.error(e)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

    ###########################################################################
    # Short 매도 시점을 확인 한다.
    ###########################################################################
    def __short_position(self):
        while True:
            try:
                tdata = analysis.get_analyze_tail(df=self.__chart.get_df(), n=3)

                if self.is_closed(): return self.__ORDER_CLOSE
                if not self.__rise_signal(tdata[0], tdata[1]):
                    logging.info("------------------------------------------------------")
                    self.__print_signal("sell", self.__stock_short, 0, tdata[0].macd_histogram(), tdata[1].macd_histogram())
                    self.sell_stock(self.__stock_short)
                    logging.info("------------------------------------------------------")
                    return self.__CALL_POSITION
            except TradingOrderBuyError as e:
                logging.error(e)
                return self.__CALL_POSITION
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)

# end of class MacdMiddleStrategy

# -----------------------------------------------------------------------------
# MacdMiddleStrategyBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class MacdMiddleStrategyBuilder:
    def __init__(self):
        self.stock_long  = None
        self.stock_short = None
        self.chart = None
        self.stock_order = None

    def set_stock_long(self, stock_long):
        self.stock_long = stock_long
        return self

    def set_stock_short(self, stock_short):
        self.stock_short = stock_short
        return self

    def set_chart(self, chart):
        self.chart = chart
        return self

    def set_stock_order(self, stock_order):
        self.stock_order = stock_order
        return self

    def build(self):
        if not all([self.stock_long, self.stock_short, self.chart, self.stock_order]):
            raise ValueError("모든 필드를 입력 하세요!")
        return MacdMiddleStrategy(
            stock_long=self.stock_long,
            stock_short=self.stock_short,
            chart=self.chart,
            stock_order=self.stock_order,
        )

# end of class MacdMiddleStrategyBuilder
