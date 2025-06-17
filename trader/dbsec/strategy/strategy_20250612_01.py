import logging
import time
import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.api_overseas as api

from trader.dbsec.base.base_strategy import BaseStrategy

# -----------------------------------------------------------------------------
# StrategyAverages
# -----------------------------------------------------------------------------
class StrategyAverages(BaseStrategy):
    __DELAY_TIME = 3
    __PROFIT_RATE = 1.04
    __LOSS_RATE = 0.998
    __WINDOWS = range(10, 121, 10)

    def __init__(self, config):
        super().__init__(config)
        self.__config = config
        self.__stock_long = config["stock_long"]
        self.__stock_shrt = config["stock_short"]
        self.__tick_size = config["tick_size"]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy Start")

        try:
            while True:
                data = self.__call_position()
                if data is None: break
                time.sleep(self.__DELAY_TIME)

                if self.__put_position(data[0], data[1]): break
                time.sleep(self.__DELAY_TIME)
        except Exception as e:
            print(e)
            logging.error(e)

        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy End")

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    async def __call_position(self):
        while True:
            # 마감 확인
            if self.is_closed(): break

            # 틱봉 조회
            df = api.chart_tick(self.__config, self.__stock_long, self.__tick_size)

            # 매수 여부 확인 후 매수
            if self.__is_rising(df): return self.buy_stock(self.__stock_long)
            if self.__is_declining(df): return self.buy_stock(self.__stock_shrt)
            time.sleep(self.__DELAY_TIME)

        return None

    def __is_rising(self, df):
        averages = [10000]
        index = 1

        for size in self.__WINDOWS:
            averages.append(analysis.get_moving_average_ema(df, size)[-1])
            if averages[index] >= averages[index - 1]: return False
            index += 1

        return ((averages[1] - averages[2]) / averages[2]) > ((averages[2] - averages[3]) / averages[3])

    def __is_declining(self, df):
        averages = [10000]
        index = 1

        for size in self.__WINDOWS:
            averages.append(analysis.get_moving_average_ema(df, size)[-1])
            if averages[index] <= averages[index - 1]: return False
            index += 1

        return ((averages[1] - averages[2]) / averages[2]) <= ((averages[2] - averages[3]) / averages[3])

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code, buy_price):
        profit_price = buy_price * self.__PROFIT_RATE
        loss_price = buy_price * self.__LOSS_RATE

        while True:
            # 마감 확인
            if self.is_closed(): break

            df = api.chart_tick(self.__config, stock_code, self.__tick_size)
            price = float(df.iloc[-2]["close"])

            if price >= profit_price or price <= loss_price:
                self.sell_stock(stock_code)
                return False
            if self.__is_declining(df):
                self.sell_stock(stock_code)
                return False

            time.sleep(self.__DELAY_TIME)

        return True

# -----------------------------------------------------------------------------
# end of class StrategyAverages
# -----------------------------------------------------------------------------
