import logging
import time

import trader.analyze.analysis_utils as analysis
from trader.kis.chart.chart import BaseChart

from trader.kis.strategy1.base_strategy import BaseStrategy

class IchimokuStrategy(BaseStrategy):
    __TICK_SMALL = 30
    __TICK_LARGE = 120

    def __init__(self, stock_order, storage, short_code):
        super().__init__(stock_order)
        self.__storage: BaseChart = storage
        self.__long_code = storage.get_stock_code()
        self.__shrt_code = short_code

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> IchimokuStrategy ready")
        self.ready()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> IchimokuStrategy start")

        try:
            while True:
                stock_code = self.__call_position()
                if stock_code is None: break
                time.sleep(0.5)

                if stock_code == self.__long_code:
                    if self.__put_long_position(self.__long_code): break
                elif stock_code == self.__shrt_code:
                    if self.__put_short_position(self.__shrt_code): break
                else:
                    break

                time.sleep(0.5)
        except Exception as e:
            logging.error(e)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy end")

    ################################################################################
    # 매매 시점 판단 가능 여부를 확인 한다.
    ################################################################################
    def ready(self):
        tick_count = self.__TICK_LARGE * analysis.get_min_tick_count()

        while True:
            if self.__storage.get_length() >= tick_count: break
            time.sleep(60)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        while True:
            if self.__storage.is_closed(): return None

            ref_small = self.get_reference_value(self.__TICK_SMALL) * 3
            ref_large = self.get_reference_value(self.__TICK_LARGE)
            ref_val = ref_small + ref_large

            if ref_val > 0 and ref_small > ref_large:
                self.buy_stock(self.__long_code)
                return self.__long_code
            elif ref_val < 0 and ref_small < ref_large:
                self.buy_stock(self.__shrt_code)
                return self.__shrt_code

    def get_reference_value(self, tick_size):
        data = analysis.add_ichimoku_base(self.__storage.get_df(tick_size)).iloc[-1]
        median = (data["high"] - data["low"]) / 2.0
        return (median - data["ichimoku_base"]) / median

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_long_position(self, stock_code):
        while True:
            if self.__storage.is_closed(): return True

            ref_small = self.get_reference_value(self.__TICK_SMALL) * 3
            ref_large = self.get_reference_value(self.__TICK_LARGE)
            ref_val = ref_small + ref_large

            if ref_val < 0 and ref_small < ref_large:
                self.sell_stock(stock_code)
                return False

            time.sleep(0.5)

    def __put_short_position(self, stock_code):
        while True:
            if self.__storage.is_closed(): return True

            ref_small = self.get_reference_value(self.__TICK_SMALL) * 3
            ref_large = self.get_reference_value(self.__TICK_LARGE)
            ref_val = ref_small + ref_large

            if ref_val > 0 and ref_small > ref_large:
                self.sell_stock(stock_code)
                return False

            time.sleep(0.5)
