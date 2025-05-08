import logging
import time
import trader.analyze.analysis_utils as analysis

from trader.kis.strategy1.base_strategy import BaseStrategy

'''
    - 매수 조건 (Buy Signal)

    - 매도 조건 (Sell Signal)
'''

class Strategy_20250507_01(BaseStrategy):
    __DELAY_TIME = 30

    def __init__(self, stock_order, storage_long, storage_shrt):
        super().__init__(stock_order)
        self.__storages = [ storage_long, storage_shrt ]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy start")

        try:
            while True:
                stock_code = self.__call_position()
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                if stock_code == self.__storages[0].get_stock_code():
                    if self.__put_position(self.__storages[0]): break
                elif stock_code == self.__storages[1].get_stock_code():
                    if self.__put_position(self.__storages[1]): break
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
        while True:
            for storage in self.__storages:
                if storage.is_closed(): return None
                time.sleep(1)

                if self.__is_buy_3m(storage) and self.__is_buy_1m(storage):
                    self.buy_stock(storage.get_stock_code())
                    return storage.get_stock_code()

            time.sleep(self.__DELAY_TIME)

    def __is_buy_3m(self, storage):
        time.sleep(1)
        df = analysis.add_analyze_macd(analysis.add_ichimoku(storage.get_df("3"))).iloc[-3:]

        data = df.iloc[-1]
        if data["close"] <= max(data["ichimoku_span1"], data["ichimoku_span2"]): return True

        return self.__is_rising(df)

    def __is_buy_1m(self, storage):
        time.sleep(1)
        df = analysis.add_analyze_macd(storage.get_df("1")).iloc[-4:-1]
        return self.__is_rising(df)

    def __is_rising(self, df):
        pdata = df.iloc[0]

        for index, data in df.iloc[1:].iterrows():
            if data["macd_histo"] <= pdata["macd_histo"]: return False
            if data["macd_middle"] <= pdata["macd_middle"]: return False
            pdata = data

        return True

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    def __put_position(self, storage):
        while True:
            if storage.is_closed(): return True
            time.sleep(1)

            df = analysis.add_analyze_macd(storage.get_df("1")).iloc[-4:-1]
            if self.__is_falling(df):
                self.sell_stock(storage.get_stock_code())
                return False

            time.sleep(self.__DELAY_TIME)

    def __is_falling(self, df):
        pdata = df.iloc[0]

        for index, data in df.iloc[1:].iterrows():
            if data["macd_histo"] >= pdata["macd_histo"]: return False
            if data["macd_middle"] > pdata["macd_middle"]: return False
            pdata = data

        return True
