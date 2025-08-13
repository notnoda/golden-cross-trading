import asyncio
import logging
import time

from market.base.broker import Broker
from market.base.strategy import Strategy
from market.base.worker import Worker

class DefaultWorker(Worker):
    __DELAY_TIME = 3

    def __init__(self, broker: Broker, strategy: Strategy, order_qty = 1):
        self.broker = broker
        self.strategy = strategy
        self.order_qty = order_qty

    def execute(self):
        try:
            asyncio.run(self.trading())
        except Exception as e:
            logging.error(e)

    async def trading(self):
        try:
            while True:
                stock_code, buy_price = await self.call_position()
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

                stock_code, sell_price = await self.put_position(stock_code, buy_price)
                if stock_code is None: break
                time.sleep(self.__DELAY_TIME)

        except Exception as e:
            logging.error(e)
        finally:
            await self.close_trading()

    async def call_position(self) -> (str, float):
        while True:
            if self.is_closed(): break
            time.sleep(self.__DELAY_TIME)

            stock_code, current_price = self.strategy.is_buy()
            if stock_code is None: continue

            buy_price = await self.broker.buy(stock_code, current_price, self.order_qty)
            return stock_code, buy_price

        return None, 0.0

    async def put_position(self, stock_code: str, buy_price: float):
        self.strategy.before_sell(buy_price)

        while True:
            if self.is_closed(): break
            time.sleep(self.__DELAY_TIME)

            stock_code, current_price = self.strategy.is_sell(stock_code)
            if stock_code is None: continue

            sell_price = await self.broker.sell(stock_code, current_price)
            return stock_code, sell_price

        return None, 0.0

    async def is_closed(self):
        return await self.strategy.is_closed()

    async def close_trading(self):
        try:
            await self.broker.sell_all()
        except Exception as e:
            logging.error(e)
