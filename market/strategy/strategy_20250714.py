import logging
import trader.analyze.analysis_utils as analysis

from market.base.strategy import Strategy
from market.base.provider import Provider

class TradingStrategy(Strategy):
    __DELAY_TIME = 3
    __TICK_SIZE = 10
    __BUY_AVERAGES = [5, 10, 15, 20, 25]
    __SELL_AVERAGES = [5, 10]

    def __init__(self, provider: Provider, stock_long: str, stock_short: strt):
        self.provider = provider
        self.stock_long = stock_long
        self.stock_shrt = stock_short
        self.tick_size = tick_size

    async def is_buy(self) -> (str, float):
        stock_code = self.stock_long
        df = await self.provider.chart(stock_code, self.__TICK_SIZE)

        prices1 = [float(df.iloc[-2])]
        prices2 = [float(df.iloc[-1])] # 현재 주가
        index = 0
        count = 0

        for window in averages:
            average = analysis.get_moving_average_sma(df, window)
            price1 = average.iloc[-2]
            price2 = average.iloc[-1]

            # 이전 틱과 비교
            if not checker(price1, price2): count += 1
            # 이전 평균 선과 비교
            if not checker(price2, prices2[index]): count += 1

            prices1.append(price1)
            prices2.append(price2)
            index += 1

        if count > 0: return None, 0.0

        logging.info(f"\t{stock_code}\t1:\t{prices1}")
        logging.info(f"\t{stock_code}\t2:\t{prices2}")
        return stock_code, 10.0

    def before_sell(self, buy_price: float):
        self.buy_price = buy_price

    async def is_sell(self, stock_code: str) -> (str, float):
        stock_code = self.stock_long
        return stock_code, self.buy_price

    async def is_closed(self) -> bool:
        return False
