import logging
import trader.analyze.analysis_utils as analysis

from trader.dbsec.base.base_strategy import BaseStrategy

# -----------------------------------------------------------------------------
# TradingStrategy
# -----------------------------------------------------------------------------
class TradingStrategy(BaseStrategy):
    __DELAY_TIME = 3
    __TICK_SIZE = 10
    __BUY_AVERAGES = [5, 10, 15, 20, 25]
    __SELL_AVERAGES = [5, 10]

    def __init__(self, config, provider):
        super().__init__(config)
        self.__config = config
        self.provider = provider
        self.stock_long = ""
        self.stock_shrt = ""

    def __is_over(self, pdata, tdata): return pdata > tdata
    def __is_under(self, pdata, tdata): return pdata < tdata

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    async def buy_price(self):
        stock_code = self.stock_long

        while True:
            # 마감 확인
            if self.is_closed(): return None, None

            # 상승장 인지 확인 한다.
            if await self.__is_trading(stock_code, self.__BUY_AVERAGES, self.__is_over):
                buy_price = await self.buy_stock(self.stock_long)
                if buy_price is not None: return self.stock_long, buy_price

            # 하락장 인지 확인 한다.
            if await self.__is_trading(stock_code, self.__BUY_AVERAGES, self.__is_under):
                buy_price = await self.buy_stock(self.stock_shrt)
                if buy_price is not None: return self.stock_shrt, buy_price

    async def __is_trading(self, stock_code, averages, checker):
        df = await self.__get_tick_data(stock_code, self.__TICK_SIZE)
        prices = [float(df.iloc[-1])] # 현재 주가

        avg120 = self.__sma_value(df, 120)
        avg480 = self.__sma_value(df, 480)
        if not checker(avg480, avg120): return False

        for window in averages:
            price = self.__sma_value(df, window)

            # 이전 평균 선과 비교
            if not checker(price, prices[-1]): return False
            prices.append(price)

        logging.info(f"\t{stock_code}\t1:\t{prices}\t,\t{avg120}\t{avg480}")
        return True

    async def __get_tick_data(self, stock_code, tick_size):
        df = await self.provider.chart_tick(stock_code, tick_size)
        return df["close"]

    def __sma_value(self, df, window):
        avgs = analysis.get_moving_average_sma(df, window)
        return round(avgs.iloc[-1], 2)

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def sell_price(self, stock_code, buy_price):

        while True:
            # 마감 확인
            if self.is_closed(): return True

            df = await self.__get_tick_data(stock_code, self.__TICK_SIZE)
            avg5 = self.__sma_value(df, self.__SELL_AVERAGES[0])
            avg10 = self.__sma_value(df, self.__SELL_AVERAGES[1])

            if avg10 > avg5:
                logging.info(f"\t매도\t5평선: {avg5}\t10평선: {avg10}")
                await self.sell_stock(stock_code)
                return False

# -----------------------------------------------------------------------------
# end of class TradingStrategy
# -----------------------------------------------------------------------------
