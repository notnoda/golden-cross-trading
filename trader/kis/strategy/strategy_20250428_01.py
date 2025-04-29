import logging
import time
import trader.analyze.analysis_utils as analysis

from trader.kis.strategy1.base_strategy import BaseStrategy

'''
    1. 10~60틱봉의 각각의 macd 골든크로스 여부 와 일목균형표 구름대의 중간값 위에 있는지 여부를 상태값을 구하고( 1 또는 0)
    2. 각 틱봉별로 가중치를 적용(5%, 8%, 10%, 20%, 25%, 32%)
    3. macd 조건에 80%, 일목균형표 구름대 중간값 위 조건에 20% 씩 가중치를 적용해서 최종값(확률) 산출
    4. 최종값이 90% 이상을 경우 '매수'
    5. 최종값이 40% 이하일 경우 '매도'
'''

class Strategy_20250428_01(BaseStrategy):
    __DELAY_TIME = 10
    __TICK_WEIGHT = [
        [ 10, 0.05 ],
        [ 20, 0.08 ],
        [ 30, 0.10 ],
        [ 40, 0.20 ],
        [ 50, 0.25 ],
        [ 60, 0.32 ]
    ]

    def __init__(self, stock_order, storage_long, storage_shrt):
        super().__init__(stock_order)
        self.__storage = storage_long
        self.__stock_long = storage_long.get_stock_code()
        self.__stock_shrt = storage_shrt.get_stock_code()

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy ready")
        self.ready(self.__storage, self.__TICK_WEIGHT[-1][0])
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy start")

        try:
            while True:
                stock_code = self.__call_position(self.__storage)
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == self.__stock_long:
                    if self.__put_position_long(self.__storage, stock_code): break
                elif stock_code == self.__stock_shrt:
                    if self.__put_position_shrt(self.__storage, stock_code): break
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
    def __call_position(self, storage):
        while True:
            if storage.is_closed(): return None
            time.sleep(1)

            weight = self.__weight_value(storage)
            if weight >= 0.9:
                self.buy_stock(self.__stock_long)
                return self.__stock_long
            elif weight <= 0.1:
                self.buy_stock(self.__stock_shrt)
                return self.__stock_shrt

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position_long(self, storage, stock_code):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            weight = self.__weight_value(storage)
            if weight <= 0.4:
                self.sell_stock(stock_code)
                return False

    def __put_position_shrt(self, storage, stock_code):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            weight = self.__weight_value(storage)
            if weight >= 0.6:
                self.sell_stock(stock_code)
                return False

    ################################################################################
    # 가중치를 계산한다.
    ################################################################################
    def __weight_value(self, storage):
        macd_vals = 0.0
        ichimoku_vals = 0.0

        for tick in self.__TICK_WEIGHT:
            data = analysis.add_ichimoku(analysis.add_analyze_macd(storage.get_df(tick[0]))).iloc[-1]

            # MACD
            if data["macd_val"] > data["macd_signal"]: macd_vals += tick[1]

            # 일목균형표
            middle_val = (data["ichimoku_span1"] + data["ichimoku_span2"]) / 2.0
            if data["close"] > middle_val: ichimoku_vals += tick[1]

        return macd_vals * 0.8 + ichimoku_vals * 0.2
