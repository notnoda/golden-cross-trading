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
    __PROFIT_RATE = 0.998
    __LOSS_RATE = 0.999
    __SELL_TICK = 60
    __TICKS = [
        [10, [5, 10, 20, 30, 60]],
        [60, [5, 20]]
    ]

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
            if await self.__checker(self.__is_rising, "long"):
                buy_price = await self.buy_stock(self.__stock_long)
                if buy_price is not None: return self.__stock_long, buy_price

            if await self.__checker(self.__is_declining, "short"):
                buy_price = await self.buy_stock(self.__stock_shrt)
                if buy_price is not None: return self.__stock_shrt, buy_price

            time.sleep(0.5)

        return None

    def __is_rising(self, pdata, tdata):
        return pdata > tdata

    def __is_declining(self, pdata, tdata):
        return pdata < tdata

    async def __checker(self, checker, type):
        for ticks in self.__TICKS:
            is_checker = await self.__check_ticks(ticks, checker, type)
            if not is_checker: return False
        return True

    async def __check_ticks(self, ticks, checker, type):
        df = await self.__get_tick_data(ticks[0])
        stock_price = [float(df.iloc[-1])]
        index = 0

        for size in ticks[1]:
            avg_price = analysis.get_moving_average_sma(df, size).iloc[-1]
            if not checker(stock_price[index], avg_price): return False
            stock_price.append(avg_price)
            index += 1

        logging.info(f"{type} - {ticks[0]} - {stock_price}")
        return True

    async def __get_tick_data(self, tick_size):
        time.sleep(0.5)
        df = await api.chart_tick(self.__config, self.__stock_long, tick_size)
        return df["close"]

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code, buy_price):
        max_price = buy_price
        loss_price = buy_price * self.__LOSS_RATE

        while True:
            # 마감 확인
            if self.is_closed(): break

            time.sleep(0.5)
            df = await api.chart_tick(self.__config, stock_code, self.__SELL_TICK)
            close_price = float(df.iloc[-1]["close"])

            # 고가
            if close_price >= max_price:
                max_price = close_price

            # 익절
            profit_price = max_price * self.__PROFIT_RATE
            if close_price < profit_price:
                logging.info(f"\t매도-익절\t현재가: {close_price}\t최고가: {max_price}\t익절가: {profit_price}")
                return await self.__sell_stock(stock_code)

            # 손절
            if close_price < loss_price:
                logging.info(f"\t매도-손절\t현재가: {close_price}\t손절가: {loss_price}")
                return await self.__sell_stock(stock_code)

            # 평균선
            avg5_price = analysis.get_moving_average_sma(df["close"], 5).iloc[-1]
            avg20_price = analysis.get_moving_average_sma(df["close"], 20).iloc[-1]
            if avg5_price < avg20_price:
                logging.info(f"\t매도-평균\t5평가: {avg5_price}\t20평가: {avg20_price}")
                return await self.__sell_stock(stock_code)

            # 일목균형표와 비교
            #data = analysis.add_ichimoku(df).iloc[-1]
            #min_price = min(data["ichimoku_span1"], data["ichimoku_span2"])
            #if min_price > close_price:
            #    logging.info(f"\t매도조건3-\t: 일목가: {min_price}\t현재가: {close_price}")
            #    return await self.__sell_stock(stock_code)

        return True

    async def __sell_stock(self, stock_code):
        await self.sell_stock(stock_code)
        return False

# -----------------------------------------------------------------------------
# end of class StrategyAverages
# -----------------------------------------------------------------------------
