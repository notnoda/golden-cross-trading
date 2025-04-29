import logging
import time
import trader.analyze.analysis_utils as analysis

from trader.kis.strategy1.base_strategy import BaseStrategy

'''
    1. 3분봉 기준으로 일목균형표의 구름대 중간값 위에 있는 종목(SOXL, SOXS 중) 선택
    2. 10~60틱봉 모두 구름대 상단 위에 각각 2개 캔들이 위치(확정)할 경우 매수
        ※ SOXS 는 10~30틱봉
    3. 10틱봉, 20틱봉이 구름대 하단 밑에 각각 2개 캔들이 위치(확정) 할 경우 매도
        ※ SOXS는 10틱봉
'''

class Strategy_20250429_01(BaseStrategy):
    __DELAY_TIME = 10

    def __init__(self, stock_order, storage_min_long, storage_min_shrt, storage_api_long, storage_api_shrt):
        super().__init__(stock_order)
        self.__stock_long = storage_api_long.get_stock_code()
        self.__stock_shrt = storage_api_shrt.get_stock_code()
        self.__storages = [
            [ storage_min_long, storage_api_long, [10, 20, 30, 40, 50, 60] ],
            [ storage_min_shrt, storage_api_shrt, [10, 20, 30] ],
        ]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy ready")
        self.ready(self.__storages[0][1], self.__storages[0][2][-1])
        self.ready(self.__storages[1][1], self.__storages[1][2][-1])
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy start")

        try:
            while True:
                stock_code = self.__call_position()
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == self.__stock_long:
                    if self.__put_position(self.__storages[0][1], [10, 20, 30]): break
                elif stock_code == self.__stock_shrt:
                    if self.__put_position(self.__storages[1][1], [10]): break
                else:
                    break
                time.sleep(self.__DELAY_TIME)
        except Exception as e:
            print(e)
            logging.error(e)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy end")

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
    def __call_position(self):
        while True:
            for storage in self.__storages:
                if storage[0].is_closed(): return None
                time.sleep(1)

                # 3분봉의 일목균형표 중간값 확인
                data = analysis.add_ichimoku(storage[0].get_df("3")).iloc[-1]
                middle_val = (data["ichimoku_span1"] + data["ichimoku_span2"]) / 2.0
                if data["close"] < middle_val: continue
                time.sleep(0.5)

                if self.__is_buy(storage[1], storage[2]):
                    time.sleep(0.1)
                    self.buy_stock(storage[0].get_stock_code())
                    return storage[0].get_stock_code()

    def __is_buy(self, storage, ticks):
        for tick_size in ticks:
            list = analysis.add_ichimoku(storage.get_df(tick_size)).tail(2)
            if self.__is_under(list.iloc[0]) or self.__is_under(list.iloc[-1]): return False
            time.sleep(0.1)

        return True

    def __is_under(self, data):
        return data["close"] <= max(data["ichimoku_span1"], data["ichimoku_span2"])

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage, ticks):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            if self.__is_sell(storage, ticks):
                time.sleep(0.1)
                self.sell_stock(storage.get_stock_code())
                return False

    def __is_sell(self, storage, ticks):
        for tick_size in ticks:
            list = analysis.add_ichimoku(storage.get_df(tick_size)).tail(2)
            if self.__is_over(list.iloc[0]) or self.__is_over(list.iloc[-1]): return False
            time.sleep(0.1)

        return True

    def __is_over(self, data):
        return data["close"] >= max(data["ichimoku_span1"], data["ichimoku_span2"])
