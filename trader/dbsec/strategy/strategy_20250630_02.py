import asyncio
import logging
import time
import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.api_overseas as api

from trader.dbsec.base.base_strategy import BaseStrategy

# -----------------------------------------------------------------------------
# TradingStrategy
# -----------------------------------------------------------------------------
class TradingStrategy(BaseStrategy):
    __DELAY_TIME = 3
    __TICKS = [10, [5, 10, 20]]

    def __init__(self, config):
        super().__init__(config)
        self.__config = config
        self.__stock_long = config["stock_long"]
        self.__stock_shrt = config["stock_short"]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy Start")

        try:
            while True:
                data = asyncio.run(self.__call_position())
                if data is None: break
                time.sleep(self.__DELAY_TIME)

                flag = asyncio.run(self.__put_position(data[0]))
                if flag: break
                time.sleep(self.__DELAY_TIME)

            # 전체 매도
            self.sell_close_all()
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

            # 매수 여부 확인 후 매수
            if await self.__checker(self.__stock_long, self.__is_rising):
                buy_price = await self.buy_stock(self.__stock_long)
                if buy_price is not None: return self.__stock_long, buy_price

            if await self.__checker(self.__stock_long, self.__is_declining):
                buy_price = await self.buy_stock(self.__stock_shrt)
                if buy_price is not None: return self.__stock_shrt, buy_price

            time.sleep(0.5)

        return None

    def __is_rising(self, pdata, tdata):
        return pdata > tdata

    def __is_declining(self, pdata, tdata):
        return pdata < tdata

    async def __checker(self, stock_code, checker):
        is_checker = await self.__check_ticks(stock_code, self.__TICKS, checker)
        return is_checker

    async def __check_ticks(self, stock_code, ticks, checker):
        df = await self.__get_tick_data(stock_code, ticks[0])
        avg100 = analysis.get_moving_average_sma(df, 130).iloc[-1]
        stock_price = [float(df.iloc[-1])]
        index = 0

        for size in ticks[1]:
            avgs = analysis.get_moving_average_sma(df, size)
            prcs = avgs.iloc[-2:]
            if not checker(prcs[0], avg100): return False
            if not checker(prcs[0], prcs[1]): return False
            if not checker(stock_price[index], prcs[0]): return False
            stock_price.append(prcs[0])
            index += 1

        logging.info(f"\t{stock_code} - {ticks[0]} - {stock_price}")
        return True

    async def __get_tick_data(self, stock_code, tick_size):
        time.sleep(0.5)
        df = await api.chart_tick(self.__config, stock_code, tick_size)
        return df["close"]

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code):
        while True:
            # 마감 확인
            if self.is_closed(): break

            if await self.__checker(stock_code, self.__is_declining):
                return await self.__sell_stock(stock_code)

        return True

    async def __sell_stock(self, stock_code):
        await self.sell_stock(stock_code)
        return False

# -----------------------------------------------------------------------------
# end of class TradingStrategy
# -----------------------------------------------------------------------------
