import logging
import time
import math
import numpy as np

import trader.analyze.analysis_utils as analysis
from trader.kis.chart.chart import BaseChart

from trader.kis.strategy1.base_strategy import BaseStrategy

class DynamicStrategy(BaseStrategy):
    __STANDARD_TICK_SIZE = 10
    __TICKS = {
        10: 6,
        20: 5,
        40: 4,
        60: 3,
        80: 3,
    }

    def __init__(self, stock_order, storages):
        super().__init__(stock_order)
        self.__storages: [BaseChart] = storages

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy ready")
        self.ready()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy start")

        while True:
            storage = self.__call_position()
            if storage is None: break
            time.sleep(0.5)

            if self.__put_position(storage): break
            time.sleep(0.5)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy end")

    ################################################################################
    # 매매 시점 판단 가능 여부를 확인 한다.
    ################################################################################
    def ready(self):
        tick_size = max(self.__TICKS.keys())
        tick_count = tick_size * analysis.get_min_tick_count()
        storage_count = len(self.__storages)

        while True:
            pass_count = 0
            for storage in self.__storages:
                if storage.get_length() >= tick_count:
                    pass_count += 1
                    #storage.get_df(tick_size)

            if pass_count >= storage_count:break
            time.sleep(60)



    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    def __call_position(self):
        while True:
            try:
                for storage in self.__storages:
                    time.sleep(0.3)
                    if storage.is_closed(): return None

                    # 기울기를 확인 할 tick을 조회 한다.
                    selected_tick = self.select_tick(storage)
                    if selected_tick == 0: continue

                    # 3. 5개의 연속 된 틱이 상승 하고 있는지 확인 한다.
                    is_buy = self.check_rised_slope(storage, selected_tick)
                    if is_buy: return storage
            except Exception as e:
                logging.error(e)

    ################################################################################
    # Diff 가 가장 작은 tick을 선택 한다.
    ################################################################################
    def select_tick(self, storage):
        prev_diff = 30
        selected = 0

        for tick in self.__TICKS.keys():
            counter = self.__TICKS[tick]
            df = analysis.add_analyze_sar(storage.get_df(tick))

            # 1. 현재 '주가' 가 '일목 균형표' 기준선 위에 있는지 확인 한다.
            data = analysis.add_ichimoku_base(df).iloc[-1]
            if data["ichimoku_base"] >= data["close"]: continue

            # 2-1. '최저가' 위치를 확인 한다.
            lowest_point = self.lowest_price_point(df["close"])
            if lowest_point > 5: continue

            # 2-2. 'SAR' 의 상승 반전 시작 위치를 확인 한다.
            sar_df = analysis.get_analyze_sar(df)
            sar_point = len(self.sar_inversion_data(sar_df["sar_long"]))
            if sar_point == 0 or sar_point > 2: continue

            # 2-3. Diff 값이 가장 작은 틱을 확인 한다.
            curr_diff = lowest_point - sar_point
            if prev_diff >= curr_diff:
                selected = tick
                prev_diff = curr_diff

        return selected

    ################################################################################
    # 주식 가격의 최저 위치를 확인 한다.
    ################################################################################
    def lowest_price_point(self, items):
        prev_price = 0
        lowest_point = 0

        for curr_price in items[::-1]:
            if lowest_point > 0 and curr_price > prev_price: return lowest_point
            prev_price = curr_price
            lowest_point += 1

        return 0

    ################################################################################
    # SAR 상승 신호(long > short) 또는 하락 신호(long < short) 시작 위치를 확인 한다.
    ################################################################################
    def sar_inversion_data(self, items):
        data = []

        for item in items[::-1]:
            if math.isnan(item): break
            data.append(item)

        return data[::-1]

    ################################################################################
    # SAR 상승 신호(long > short) 시작 위치를 확인 한다.
    ################################################################################
    def check_rised_slope(self, storage, tick):
        tick_count = self.__TICKS[tick]

        while True:
            sar_df = analysis.get_analyze_sar(storage.get_df(tick))
            sar_data = self.sar_inversion_data(sar_df["sar_long"])

            sar_size = len(sar_data)
            if sar_size == 0: return False
            if sar_size < tick_count:
                time.sleep(0.2)
                continue

            data = sar_data[tick_count * -1:]

            # 1차 기울기가 10 이상 인지 확인 한다.
            angles = math.degrees(math.atan(data[-1] - data[0]))
            logging.info(f"기울기 = {angles}")
            if angles < 3: return False

            # 2차 기울기를 확인 한다.
            differences = np.diff(np.array(data))
            if sum(1 for acc in differences if acc > 0) < len(differences): return False

            # 매수 한다.
            stock_code = storage.get_stock_code()
            self.buy_stock(stock_code)
            return True

    ################################################################################
    # *****
    ################################################################################
    def __get_limit_slope(self, df):
        values = []
        for index, row in df.iterrows():
            if math.isnan(row["sar_long"]) and math.isnan(row["sar_long"]): continue
            if math.isnan(row["sar_long"]): values.append(row["sar_short"])
            else: values.append(row["sar_long"])

        differences = np.array(np.diff(np.array(values)))
        average = np.mean(differences)
        std_dev = np.std(differences, ddof=1)
        return average + std_dev * 1.5

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage):
        stock_code = storage.get_stock_code()

        while True:
            if storage.is_closed(): return True

            sar_df = analysis.get_analyze_sar(storage.get_df(self.__STANDARD_TICK_SIZE))
            data = sar_df.iloc[-1]
            if math.isnan(data["sar_short"]): continue

            logging.info("------------------------------------------------------")
            logging.info(f"sell : [{stock_code}]")
            self.sell_stock(stock_code)
            logging.info("------------------------------------------------------")

            return False
