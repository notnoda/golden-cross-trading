import logging
import time

import trader.analyze.analysis_utils as analysis
from trader.kis.chart.chart import BaseChart

from trader.kis.strategy1.base_strategy import BaseStrategy

class IchimokuStrategy(BaseStrategy):
    __TICK_SMALL_LONG = 30
    __TICK_LARGE_LONG = 120
    __TICK_SMALL_SHRT = 15
    __TICK_LARGE_SHRT = 60

    __WEIGHT_VAL = 2
    __HOLDING_VAL = 0.005

    def __init__(self, stock_order, storage_long, storage_shrt):
        super().__init__(stock_order)
        self.__storage_long: BaseChart = storage_long
        self.__storage_shrt: BaseChart = storage_shrt
        self.__long_code = storage_long.get_stock_code()
        self.__shrt_code = storage_shrt.get_stock_code()

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
                    if self.__put_position(self.__storage_long, self.__TICK_SMALL_LONG, self.__TICK_LARGE_LONG): break
                elif stock_code == self.__shrt_code:
                    if self.__put_position(self.__storage_shrt, self.__TICK_SMALL_SHRT, self.__TICK_LARGE_SHRT): break
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
        tick_count = self.__TICK_LARGE_LONG * analysis.get_min_tick_count()

        while True:
            if self.__storage_long.get_length() >= tick_count: break
            time.sleep(60)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        while True:
            if self.__storage_long.is_closed(): return None

            stock_code = None
            data_small = self.get_last_data(self.__storage_long, self.__TICK_LARGE_LONG)
            data_large = self.get_last_data(self.__storage_long, self.__TICK_LARGE_SHRT)

            ref_small = self.get_reference_value(data_small, self.__WEIGHT_VAL)
            ref_large = self.get_reference_value(data_large)
            ref_val = ref_small + ref_large

            if ref_val > 0 and ref_small > ref_large:
                stock_code = self.__long_code
            elif ref_val < 0 and ref_small < ref_large:
                stock_code = self.__shrt_code

            if stock_code is not None:
                self.print_log(data_small, data_large, ref_small, ref_large)
                self.buy_stock(stock_code)
                return stock_code

            time.sleep(0.5)

    def get_last_data(self, storage, tick_size):
        data = analysis.add_ichimoku_base(storage.get_df(tick_size)).iloc[-1]
        data["median"] = round((data["high"] + data["low"]) / 2.0, 4)
        return data

    def get_reference_value(self, data, weight=1):
        median = data["median"]
        return round((median - data["ichimoku_base"]) / median, 4) * weight

    def print_log(self, data_small, data_large, ref_small, ref_large):
        logging.info(f"small: {data_small['high']}\t{data_small['low']}\t{data_small['median']}\t{data_small['ichimoku_base']}\t{ref_small}")
        logging.info(f"lager: {data_large['high']}\t{data_large['low']}\t{data_large['median']}\t{data_large['ichimoku_base']}\t{ref_large}")

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage, tick_small, tick_large):
        cut_price = self.get_purchase_price() * 0.995
        stock_code = storage.get_stock_code()

        while True:
            if storage.is_closed(): return True

            # 손절
            data_small = self.get_last_data(storage, tick_small)
            if data_small["close"] < cut_price:
                self.sell_stock(stock_code)
                return False

            data_large = self.get_last_data(storage, tick_large)
            ref_small = self.get_reference_value(data_small, self.__WEIGHT_VAL)
            ref_large = self.get_reference_value(data_large)

            diff_value = data_small["median"] - data_small["ichimoku_base"]
            hold_value = data_small["median"] * self.__HOLDING_VAL

            if ref_small < ref_large and 0 < diff_value <= hold_value:
                self.print_log(data_small, data_large, ref_small, ref_large)
                self.sell_stock(stock_code)
                return False

            time.sleep(0.5)
