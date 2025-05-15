import logging
import numpy
import time
import trader.analyze.analysis_utils as analysis

from trader.kis.strategy1.base_strategy import BaseStrategy

'''
    - 매수 조건 (Buy Signal)

    - 매도 조건 (Sell Signal)
'''

class Strategy_20250512_01(BaseStrategy):
    __DELAY_TIME = 30
    __RISE_TICKS = [10, 20, 30, 480]
    __FALL_TICKS = [10, 20, 30, 60]

    def __init__(self, stock_order, storage_long, storage_shrt):
        super().__init__(stock_order)
        self.__storage = storage_long
        self.__stock_long = storage_long.get_stock_code()
        self.__stock_shrt = storage_shrt.get_stock_code()

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy start")

        try:
            storage = self.__storage

            while True:
                stock_code = self.__call_position(storage)
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == self.__stock_long:
                    if self.__put_position_long(storage, self.__FALL_TICKS): break
                elif stock_code == self.__stock_shrt:
                    if self.__put_position_long(storage, self.__RISE_TICKS): break
                else:
                    break
                time.sleep(self.__DELAY_TIME)
        except Exception as e:
            print(e)
            logging.error(e)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy end")

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self, storage):
        while True:
            if storage.is_closed(): return None
            time.sleep(1)

            if self.__is_rising(storage, self.__RISE_TICKS):
                self.buy_stock(self.__stock_long)
                return self.__stock_long
            time.sleep(3)

            if self.__is_falling(storage, self.__FALL_TICKS):
                self.buy_stock(self.__stock_shrt)
                return self.__stock_shrt
            time.sleep(10)

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position_long(self, storage, ticks):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            if self.__is_falling(storage, ticks):
                self.buy_stock(self.__stock_long)
                return False

            time.sleep(10)

    def __put_position_shrt(self, storage, ticks):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            if self.__is_rising(storage, ticks):
                self.buy_stock(self.__stock_shrt)
                return False

            time.sleep(10)

    def __is_rising(self, storage, ticks):
        for tick_size in ticks:
            df = analysis.add_ichimoku(storage.get_df(tick_size))
            data = df.iloc[-1]

            middle_val = numpy.mean(data["ichimoku_span1"], data["ichimoku_span2"])
            if (data["close"] <= middle_val) return False

        return True

    def __is_falling(self, storage, ticks):
        for tick_size in ticks:
            df = analysis.add_ichimoku(storage.get_df(tick_size))
            data = df.iloc[-1]

            middle_val = numpy.mean(data["ichimoku_span1"], data["ichimoku_span2"])
            if (data["close"] >= middle_val) return False

        return True
