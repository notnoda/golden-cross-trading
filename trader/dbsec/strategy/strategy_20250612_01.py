import logging
import time
import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.overseas_chart as chart

from trader.dbsec.base.base_strategy import BaseStrategy

'''
    - 매수 조건 (Buy Signal)
      현재 캔들이 각각의 틱봉(10틱, 20틱, 60틱)의 일목균형표 구름대 상단 위에 있음
      즉: 현재 종가 > max(선행스팬1, 선행스팬2)
      선행 구름(예: 미래 26틱) 동안 양운(적운)만 존재함
      즉: 선행스팬1 > 선행스팬2 for 모든 미래 i

    - 매도 조건 (Sell Signal)
      10틱봉과 20틱봉의 현재 캔들이 구름대 하단 아래에 있음
      즉: 현재 종가 < min(선행스팬1, 선행스팬2)
'''

class strategy_20250612_01(BaseStrategy):
    __TICK_BUY = [ [ 10, 20, 60 ], [ 5, 10, 30 ] ]
    __TICK_SEL = [ [ 10, 20 ],  [ 5, 10 ] ]

    __DELAY_TIME = 10
    __WEIGHT_VAL = 2
    __HOLDING_VAL = 0.005

    def __init__(self, config, storage_shrt):
        super().__init__()
        self.__config = config
        self.__market_code = config[""]
        self.__stock_code = config[""]
        self.__tick_size = config[""]

    def execute(self):

        try:
            while True:
                stock_code = self.__call_position()
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == self.__storages[0].get_stock_code():
                    if self.__put_position(self.__storages[0], self.__TICK_SEL[0]): break
                elif stock_code == self.__storages[1].get_stock_code():
                    if self.__put_position(self.__storages[1], self.__TICK_SEL[1]): break
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
    def __call_position(self):
        tick_count = len(ticks)

        while True:
            index = 0

            for storage in self.__storages:
                if storage.is_closed(): return None
                buy_count = 0
                time.sleep(1)

                ticks = self.__TICK_BUY[index]
                index += 1

                for tick_size in ticks:
                    time.sleep(0.5)
                    if self.__is_buy(storage, tick_size): buy_count += 1

                if tick_count == buy_count:
                    self.buy_stock(storage.get_stock_code())
                    return storage.get_stock_code()

            time.sleep(0.5)

    def __is_buy(self, storage, tick_size):
        ticks = chart.chart_tick(self.__config, self.__market_code, self.__stock_code, self.__tick_size)

        # 마지막 캔들의 종가 일목균형표 구름대 상단에 위치하는지 확인한다.
        ldata = tails.tail(1)
        if ldata["close"] <= max(ldata["ichimoku_span1"], ldata["ichimoku_span2"]): return False

        # 최근 20개의 캔들이 양운만 있는지 확인 한다.
        for data in tails:
            if data["ichimoku_span1"] <= data["ichimoku_span2"]: return False

        return True

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage, ticks):
        tick_count = len(ticks)

        while True:
            if storage.is_closed(): return False
            sell_count = 0
            time.sleep(1)

            for tick_size in ticks:
                time.sleep(0.5)

                data = analysis.add_ichimoku(storage.get_df(tick_size)).tail(1)
                if data["close"] < min(ldata["ichimoku_span1"], data["ichimoku_span2"]): sell_count += 1

            if tick_count == sell_count:
                self.sell_stock(storage.get_stock_code())
                return True

            time.sleep(0.5)
