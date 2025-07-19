import asyncio
import logging
import time
import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.api_overseas as api

from trader.dbsec.base.base_strategy import BaseStrategy

# -----------------------------------------------------------------------------
# TradingStrategy
# -----------------------------------------------------------------------------
class DefaultWorker:
    __DELAY_TIME = 3
    __PROFIT_RATE = 1.004
    __LOSS_RATE = 0.998
    __SELL_TICK = 60
    __TICKS = [
        [60, [5, 10, 20]]
    ]

    def __init__(self, config, rest, broker, provider, strategy):
        self.__config = config
        self.rest = rest
        self.broker = broker
        self.strategy = strategy

        self.order_qty = config["order_qty"]
        self.__stock_long = config["stock_long"]
        self.__stock_shrt = config["stock_short"]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy Start")

        try:
            while True:
                stock_code, stock_price = asyncio.run(self.strategy.buy_price())
                if stock_code is None: break
                self.broker.buy(stock_code, stock_price, self.order_qty)

                time.sleep(self.__DELAY_TIME)

                flag = asyncio.run(self.__put_position(stock_code, stock_price))
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
        df = await self.__get_tick_data(self.__stock_long, ticks[0])
        avg100 = analysis.get_moving_average_sma(df, 100).iloc[-1]
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

        logging.info(f"\t매수 - {type} - {ticks[0]} - {stock_price}")
        return True

    async def __get_tick_data(self, stock_code, tick_size):
        time.sleep(0.5)
        df = await api.chart_tick(self.__config, stock_code, tick_size)
        return df["close"]

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self, stock_code, buy_price):
        profit_price = buy_price * self.__PROFIT_RATE
        loss_price = buy_price * self.__LOSS_RATE
        prev_diff = 0

        while True:
            # 마감 확인
            if self.is_closed(): break

            time.sleep(0.5)
            df = await self.__get_tick_data(self.__stock_long, self.__SELL_TICK)
            close_price = float(df.iloc[-1])

            # 익절
            if close_price >= profit_price:
                logging.info(f"\t매도-익절\t현재가: {close_price}\t익절가: {profit_price}")
                return await self.__sell_stock(stock_code)

            # 손절
            if close_price < loss_price:
                logging.info(f"\t매도-손절\t현재가: {close_price}\t손절가: {loss_price}")
                return await self.__sell_stock(stock_code)

            # 평균선
            avg10_price = analysis.get_moving_average_sma(df, 10).iloc[-1]
            avg60_price = analysis.get_moving_average_sma(df, 60).iloc[-1]
            avg_diff = abs(avg10_price - avg60_price)

            if prev_diff > avg_diff:
                logging.info(f"\t매도-평균\t5평가: {avg10_price}\t20평가: {avg60_price}\t차: {prev_diff}\t{avg_diff}")
                return await self.__sell_stock(stock_code)

            prev_diff = avg_diff

        return True

    async def __sell_stock(self, stock_code):
        await self.sell_stock(stock_code)
        return False

# -----------------------------------------------------------------------------
# end of class TradingStrategy
# -----------------------------------------------------------------------------
