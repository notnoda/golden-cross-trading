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
    __LOSS_RATE = 0.997
    __PROFIT_RATE = 1.01

    __TICK_SIZE = 10
    __BUY_AVERAGES = [5, 10, 20, 30, 40, 50, 60, 120, 240, 360]
    __SELL_AVERAGES = [5, 10, 20, 30, 40, 50, 60]

    def __init__(self, config):
        super().__init__(config)
        self.__config = config
        self.__stock_long = config["stock_long"]
        self.__stock_shrt = config["stock_short"]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy Start")

        try:
            while True:
                # 매수 조건 확인 후 주식을 매수 한다.
                stock_code, buy_price = asyncio.run(self.__call_position())
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                # 매수 조건 확인 후 주식을 매수 한다.
                flag = asyncio.run(self.__put_position(stock_code, buy_price))
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
        stock_code = self.__stock_long

        while True:
            # 마감 확인
            if self.is_closed(): return None, None
            time.sleep(0.5)

            # 상승장 인지 확인 한다.
            if await self.__is_trading(stock_code, self.__BUY_AVERAGES, self.__is_rising):
                buy_price = await self.buy_stock(self.__stock_long)
                if buy_price is not None: return self.__stock_long, buy_price

            # 하락장 인지 확인 한다.
            if await self.__is_trading(stock_code, self.__BUY_AVERAGES, self.__is_declining):
                buy_price = await self.buy_stock(self.__stock_shrt)
                if buy_price is not None: return self.__stock_shrt, buy_price


    def __is_rising(self, price1, price2):
        return price1 < price2

    def __is_declining(self, price1, price2):
        return price1 > price2

    async def __is_trading(self, stock_code, averages, checker):
        df = await self.__get_tick_data(stock_code, self.__TICK_SIZE)
        time.sleep(0.5)

        prices = [float(df.iloc[-1])] # 현재 주가
        index = 0

        for window in averages:
            average = analysis.get_moving_average_sma(df, window)
            price1 = average.iloc[-2]
            price2 = average.iloc[-1]

            # 이전 틱과 비교
            if not checker(price1, price2): return False
            # 이전 평균 선과 비교
            if not checker(prices[index], price2): return False

            prices.append(price2)
            index += 1

        logging.info(f"\t{stock_code}\t{prices}")
        return True

    async def __get_tick_data(self, stock_code, tick_size):
        time.sleep(0.5)
        df = await api.chart_tick(self.__config, stock_code, tick_size)
        return df["close"]

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code, buy_price):
        loss_price = buy_price * self.__LOSS_RATE
        profit_price = buy_price * self.__PROFIT_RATE

        while True:
            # 마감 확인
            if self.is_closed(): return True

            is_sell = await self.__is_sell(stock_code, loss_price, profit_price)
            if is_sell:
                await self.sell_stock(stock_code)
                return False

    async def __is_sell(self, stock_code, loss_price, profit_price):
        # 하락 추세
        if await self.__is_trading(stock_code, self.__SELL_AVERAGES, self.__is_declining):
            return True

        df = await self.__get_tick_data(stock_code, self.__TICK_SIZE)
        time.sleep(0.5)
        close_price = float(df.iloc[-1]) # 현재 주가

        # 손절
        if close_price < loss_price:
            logging.info(f"\t매도-손절\t현재가: {close_price}\t손절가: {loss_price}")
            return True
        # 익절
        if close_price >= profit_price:
            logging.info(f"\t매도-익절\t현재가: {close_price}\t익절가: {profit_price}")
            return

        return False

# -----------------------------------------------------------------------------
# end of class TradingStrategy
# -----------------------------------------------------------------------------
