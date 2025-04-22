import logging
import time
import math
import numpy as np

import trader.analyze.analysis_utils as analysis
from trader.kis.chart.chart import BaseChart

from trader.kis.strategy1.base_strategy import BaseStrategy

'''
    일목균형표 보다 위에 있으면서,
    MACD의 히스토그램이 반전 상승이 세번째 까지 이어지면 매수,
    그 반대의 경우 매도
'''
class MacdHistogramStrategy(BaseStrategy):
    __TICK_MINUTES = [ "3", "1" ]
    __DELAY_TIME = 120
    __WEIGHT_VAL = 2

    def __init__(self, stock_order, storage_long, storage_shrt):
        super().__init__(stock_order)
        self.__storages = [ storage_long, storage_shrt ]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdHistogramStrategy start")

        try:
            long_code = self.__storages[0].get_stock_code()
            shrt_code = self.__storages[1].get_stock_code()

            while True:
                stock_code = self.__call_position()
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == long_code:
                    if self.__put_position(self.__storages[0]): break
                elif stock_code == shrt_code:
                    if self.__put_position(self.__storages[1]): break
                else:
                    break

                time.sleep(self.__DELAY_TIME)
        except Exception as e:
            print(e)
            logging.error(e)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MacdHistogramStrategy end")

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        while True:
            for storage in self.__storages:
                if storage.is_closed(): return None
                time.sleep(1)

                is_up = self.__is_upward_trend(storage, self.__TICK_MINUTES[0])
                if not is_up: continue
                time.sleep(0.3)

                is_up = self.__is_upward_trends(storage, self.__TICK_MINUTES[1])
                if not is_up: continue
                time.sleep(0.3)

                # 매수 한다.
                stock_code = storage.get_stock_code()
                self.buy_stock(stock_code)
                return stock_code

            time.sleep(0.5)

    def __is_upward_trend(self, storage, minute):
        data = analysis.add_analyze_macd(storage.get_df(minute))["macd_histo"]
        return data.iloc[-2] < data.iloc[-1]

    def __is_upward_trends(self, storage, minute):
        data = analysis.add_analyze_macd(storage.get_df(minute))["macd_histo"]
        logging.info(f"[{data.iloc[-3]}][{data.iloc[-2]}][{data.iloc[-1]}]")
        return data.iloc[-3] < data.iloc[-2] < data.iloc[-1]

    def __get_lowest_point(self, storage, minute):
        df = analysis.add_analyze_macd(storage.get_df(minute))
        prev_val = 0
        lowest_point = 0

        for curr_val in df["macd_histo"][::-1]:
            if lowest_point > 0 and curr_val > prev_val: return lowest_point
            prev_val = curr_val
            lowest_point += 1

        return -1

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            is_down = self.__is_downward_trend(storage, self.__TICK_MINUTES[0])
            if not is_down: continue
            time.sleep(0.3)

            is_down = self.__is_downward_trends(storage, self.__TICK_MINUTES[1])
            if not is_down: continue
            time.sleep(0.3)

            # 매도 한다.
            self.sell_stock(storage.get_stock_code())
            return False

    def __is_downward_trend(self, storage, minute):
        data = analysis.add_analyze_macd(storage.get_df(minute))["macd_histo"]
        return data.iloc[-2] > data.iloc[-1]

    def __is_downward_trends(self, storage, minute):
        data = analysis.add_analyze_macd(storage.get_df(minute))["macd_histo"]
        logging.info(f"[{data.iloc[-3]}][{data.iloc[-2]}][{data.iloc[-1]}]")
        return data.iloc[-3] > data.iloc[-2] > data.iloc[-1]

    def __get_highest_point(self, storage, minute):
        df = analysis.add_analyze_macd(storage.get_df(minute))
        prev_val = 0
        lowest_point = 0

        for curr_val in df["macd_histo"][::-1]:
            if lowest_point > 0 and curr_val < prev_val: return lowest_point
            prev_val = curr_val
            lowest_point += 1

        return -1
