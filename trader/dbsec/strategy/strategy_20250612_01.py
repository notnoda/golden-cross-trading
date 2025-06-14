import logging
import time
import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.api_overseas as api

from trader.dbsec.base.base_strategy import BaseStrategy

class StrategyAverages(BaseStrategy):
    __DELAY_TIME = 3
    __PROFIT_RATE = 1.04
    __LOSS_RATE = 0.998
    __WINDOWS = range(10, 121, 10)

    def __init__(self, config):
        super().__init__()
        self.__config = config
        self.__stock_long = config["stock_long"]
        self.__stock_shrt = config["stock_short"]
        self.__tick_size = config["tick_size"]

    def execute(self):
        try:
            while True:
                price = self.__call_position()
                if price is None: break
                time.sleep(self.__DELAY_TIME)

                stock_code = price["stock_code"]
                stock_price = float(price["Oprc"])

                if self.__put_position(stock_code, stock_price): break
                time.sleep(self.__DELAY_TIME)
        except Exception as e:
            print(e)
            logging.error(e)

        self.treade_closed()
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DynamicStrategy end")

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    async def __call_position(self):

        while True:
            #TODO - 마감여부 정의
            df = api.chart_tick(self.__config, self.__stock_long, self.__tick_size)
            if self.__is_rising(df): return await self.__buy_stock(self.__stock_long)
            if self.__si_declining(df): return await self.__buy_stock(self.__stock_shrt)
            time.sleep(self.__DELAY_TIME)

        #TODO - return None

    def __is_rising(self, df):
        averages = [10000]
        index = 1

        for size in self.__WINDOWS:
            averages.append(analysis.get_moving_average_ema(df, size)[-1])
            if averages[index] >= averages[index - 1]: return False
            index += 1

        return ((averages[1] - averages[2]) / averages[2]) > ((averages[2] - averages[3]) / averages[3])

    def __si_declining(self, df):
        averages = [10000]
        index = 1

        for size in self.__WINDOWS:
            averages.append(analysis.get_moving_average_ema(df, size)[-1])
            if averages[index] <= averages[index - 1]: return False
            index += 1

        return ((averages[1] - averages[2]) / averages[2]) <= ((averages[2] - averages[3]) / averages[3])

    async def __buy_stock(self, stock_code):
        await api.order_buy(self.__config, stock_code)
        price = await api.inquiry_price(self.__config, stock_code)
        price["stock_code"] = stock_code
        return price

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code, buy_price):
        profit_price = buy_price * self.__PROFIT_RATE
        loss_price = buy_price * self.__LOSS_RATE

        while True:
            #TODO - 마감여부 정의
            data = await api.inquiry_price(self.__config, stock_code)
            price = float(data["Oprc"])
            if price >= profit_price or price <= loss_price: return self.__sell_stock(stock_code)

            df = api.chart_tick(self.__config, stock_code, self.__tick_size)
            if self.__si_declining(df):
                await self.__sell_stock(stock_code)
                return False

            time.sleep(self.__DELAY_TIME)

        #TODO - return True

    async def __sell_stock(self, stock_code):
        await api.order_sell(self.__config, stock_code)
        return
