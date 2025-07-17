import logging
import trader.analyze.analysis_utils as analysis

from trader.dbsec.base.base_strategy import BaseStrategy

# -----------------------------------------------------------------------------
# TradingStrategy
# -----------------------------------------------------------------------------
class TradingStrategy(BaseStrategy):
    __DELAY_TIME = 3
    __PROFIT_RATE = 1.004
    __LOSS_RATE = 0.998
    __SELL_TICK = 60
    __TICKS = [
        [60, [5, 10, 20]]
    ]

    def __init__(self, config, rest):
        super().__init__(config)
        self.__config = config
        self.__rest = rest
        self.__stock_long = config["stock_long"]
        self.__stock_shrt = config["stock_short"]

    def __is_over(self, pdata, tdata): return pdata > tdata
    def __is_under(self, pdata, tdata): return pdata < tdata

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    async def buy_price(self):
        curr_price = await self.__buy_price("long", self.__is_over)
        if curr_price > 0: return self.__stock_long, curr_price

        curr_price = await self.__buy_price("short", self.__is_under)
        return self.__stock_shrt, curr_price

    async def __buy_price(self, type, compareTo):
        close_price = 0

        for ticks in self.__TICKS:
            close_price = await self.__get_tick_price(type, ticks, compareTo)
            if close_price == 0: return 0

        return close_price

    async def __get_tick_price(self, type, ticks, compareTo):
        df = await self.__get_close_df(self.__stock_long, ticks[0])
        avg100 = analysis.get_moving_average_sma(df, 100).iloc[-1]
        stock_price = [float(df.iloc[-1])]
        index = 0

        for size in ticks[1]:
            avgs = analysis.get_moving_average_sma(df, size)
            prcs = avgs.iloc[-2:]
            if not compareTo(prcs[0], avg100): return 0
            if not compareTo(prcs[0], prcs[1]): return 0
            if not compareTo(stock_price[index], prcs[0]): return 0
            stock_price.append(prcs[0])
            index += 1

        logging.info(f"\t매수 - {type} - {ticks[0]} - {stock_price}")
        return stock_price[0]

    async def __get_close_df(self, stock_code, tick_size):
        df = await self.__rest.chart_tick(stock_code, tick_size)
        return df["close"]

    ################################################################################
    # 매도 시점을 판단 한다.
    ################################################################################
    async def put_position(self, stock_code, buy_price):
        profit_price = buy_price * self.__PROFIT_RATE
        loss_price = buy_price * self.__LOSS_RATE
        prev_diff = 0

        df = await self.__get_close_df(self.__stock_long, self.__SELL_TICK)
        close_price = float(df.iloc[-1])

        # 익절
        if close_price >= profit_price:
            logging.info(f"\t매도-익절\t현재가: {close_price}\t익절가: {profit_price}")
            return True

        # 손절
        if close_price < loss_price:
            logging.info(f"\t매도-손절\t현재가: {close_price}\t손절가: {loss_price}")
            return True

        # 평균선
        avg10_price = analysis.get_moving_average_sma(df, 10).iloc[-1]
        avg60_price = analysis.get_moving_average_sma(df, 60).iloc[-1]
        avg_diff = abs(avg10_price - avg60_price)

        if prev_diff > avg_diff:
            logging.info(f"\t매도-평균\t5평가: {avg10_price}\t20평가: {avg60_price}\t차: {prev_diff}\t{avg_diff}")
            return True

        return False

# -----------------------------------------------------------------------------
# end of class TradingStrategy
# -----------------------------------------------------------------------------
