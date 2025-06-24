import asyncio
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
    __PROFIT_RATE = 0.96
    __LOSS_RATE = 0.998

    __TICK1 = [20, [5, 20, 30, 60]]
    __TICK2 = [120, [5, 10, 20]]

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

                flag = asyncio.run(self.__put_position(data[0], data[1]))
                if flag: break
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

            # 매수 여부 확인 후 매수
            if await self.__is_rising():
                buy_price = await self.buy_stock(self.__stock_long)
                if buy_price is not None: return self.__stock_long, buy_price

            if await self.__is_declining():
                buy_price = await self.buy_stock(self.__stock_shrt)
                if buy_price is not None: return self.__stock_shrt, buy_price

            time.sleep(0.5)

        return None

    async def __is_rising(self):
        is_checker = await self.__check_rising(self.__TICK1)
        if not is_checker: return False

        is_checker = await self.__check_rising(self.__TICK2)
        return is_checker

    async def __check_rising(self, ticks):
        time.sleep(0.5)
        df = await api.chart_tick(self.__config, self.__stock_long, ticks[0])
        stock_price = float(df.iloc[-1]["close"])
        check_prices = [stock_price]

        for size in ticks[1]:
            avg_price = analysis.get_moving_average_ema(df["close"], size).iloc[-1]
            if stock_price <= avg_price: return False
            stock_price = avg_price
            check_prices.append(stock_price)

        logging.info(check_prices)
        return True

    async def __is_declining(self):
        is_checker = await self.__check_declining(self.__TICK1)
        if not is_checker: return False

        is_checker = await self.__check_declining(self.__TICK2)
        return is_checker

    async def __check_declining(self, ticks):
        time.sleep(0.5)
        df = await api.chart_tick(self.__config, self.__stock_long, ticks[0])
        stock_price = float(df.iloc[-1]["close"])
        check_prices = [stock_price]

        for size in ticks[1]:
            avg_price = analysis.get_moving_average_ema(df["close"], size).iloc[-1]
            if stock_price >= avg_price: return False
            stock_price = avg_price
            check_prices.append(stock_price)

        logging.info(check_prices)
        return True

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code, buy_price):
        max_price = buy_price
        loss_price = buy_price * self.__LOSS_RATE

        while True:
            # 마감 확인
            if self.is_closed(): break

            df = await api.chart_tick(self.__config, stock_code, self.__TICK1[0])
            close_price = float(df.iloc[-1]["close"])

            # 익절
            if close_price >= max_price:
                max_price = close_price
                continue
            else:
                profit_price = max_price * self.__PROFIT_RATE
                if max_price < profit_price:
                    logging.info(f"\t매도조건1-\t현재가: {close_price}\t최고가: {max_price}\t익절가: {profit_price}")
                    return await self.__sell_stock(stock_code)

            # 손절
            if close_price < loss_price:
                logging.info(f"\t매도조건2-\t현재가: {close_price}\t손절가: {loss_price}")
                return await self.__sell_stock(stock_code)

            # 일목균형표와 비교
            data = analysis.add_ichimoku(df).iloc[-1]
            min_price = min(data["ichimoku_span1"], data["ichimoku_span2"])
            if min_price > close_price:
                logging.info(f"\t매도조건3-\t: 일목가: {min_price}\t현재가: {close_price}")
                return await self.__sell_stock(stock_code)

            time.sleep(0.5)

        return True

    async def __sell_stock(self, stock_code):
        await self.sell_stock(stock_code)
        return False

# -----------------------------------------------------------------------------
# end of class StrategyAverages
# -----------------------------------------------------------------------------
