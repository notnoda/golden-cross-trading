import logging
import time
import trader.analyze.analysis_utils as analysis

from trader.kis.chart.chart import BaseChart
from trader.kis.strategy1.base_strategy import BaseStrategy

class IchimokuStrategy(BaseStrategy):
    __TICK_LONG = [ 30, 120 ]
    __TICK_SHRT = [ 15, 60 ]

    __DELAY_TIME = 120
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
        self.ready(self.__storage_long, self.__TICK_LONG[1])
        self.ready(self.__storage_shrt, self.__TICK_SHRT[1])
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> IchimokuStrategy start")

        try:
            while True:
                stock_code = self.__call_position(self.__storage_long, self.__TICK_LONG)
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == self.__long_code:
                    if self.__put_position(self.__storage_long, self.__TICK_LONG): break
                elif stock_code == self.__shrt_code:
                    if self.__put_position(self.__storage_shrt, self.__TICK_SHRT): break
                else:
                    break
                time.sleep(self.__DELAY_TIME)
        except Exception as e:
            print(e)
            logging.error(e)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy end")

    ################################################################################
    # 매매 시점 판단 가능 여부를 확인 한다.
    ################################################################################
    def ready(self, storage, tick_size):
        tick_count = tick_size * analysis.get_min_tick_count()

        while True:
            if storage.get_length() >= tick_count: break
            time.sleep(60)

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self, storage, ticks):
        while True:
            if self.__storage_long.is_closed(): return None

            stock_code = None
            data_small = self.get_last_and_refer(storage, ticks[0], self.__WEIGHT_VAL)
            data_large = self.get_last_and_refer(storage, ticks[1])

            ref_small = data_small["refer"]
            ref_large = data_large["refer"]
            ref_val = ref_small + ref_large

            if ref_val > 0 and ref_small > ref_large:
                stock_code = self.__long_code
            elif ref_val < 0 and ref_small < ref_large:
                stock_code = self.__shrt_code

            if stock_code is not None:
                self.print_log(data_small, data_large)
                self.buy_stock(stock_code)
                return stock_code

            time.sleep(0.5)

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage, ticks):
        cap_price = self.get_purchase_price() * self.__HOLDING_VAL
        cut_price = self.get_purchase_price() - cap_price
        stock_code = storage.get_stock_code()

        while True:
            if storage.is_closed(): return True

            # 손절
            data_small = self.get_last_and_refer(storage, ticks[0], self.__WEIGHT_VAL)
            if data_small["close"] < cut_price:
                self.sell_stock(stock_code)
                return False

            data_large = self.get_last_and_refer(storage, ticks[1])
            ref_small = data_small["refer"]
            ref_large = data_large["refer"]

            diff_value = data_small["median"] - data_small["ichimoku_base"]
            hold_value = data_small["median"] * self.__HOLDING_VAL

            if ref_small < ref_large and 0 < diff_value <= hold_value:
                self.print_log(data_small, data_large)
                self.sell_stock(stock_code)
                return False

            time.sleep(0.5)

    ################################################################################
    # 데이터를 가져와 가공 한다.
    ################################################################################
    def get_last_and_refer(self, storage, tick_size, weight=1):
        data = analysis.add_ichimoku_base(storage.get_df(tick_size)).iloc[-1]
        median = round((data["high"] + data["low"]) / 2.0, 4)

        data["median"] = median
        data["refer"] = round((median - data["ichimoku_base"]) / median, 4) * weight
        return data

    ################################################################################
    # 로그에 출력 한다.
    ################################################################################
    def print_log(self, data_small, data_large):
        logging.info(f"small: {data_small['high']}\t{data_small['low']}\t{data_small['median']}\t{data_small['ichimoku_base']}\t{data_small['refer']}")
        logging.info(f"lager: {data_large['high']}\t{data_large['low']}\t{data_large['median']}\t{data_large['ichimoku_base']}\t{data_large['refer']}")
