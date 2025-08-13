from market.base.broker import Broker
from market.base.rest import Rest

class DummyBroker(Broker):

    def __init__(self, rest: Rest, market_code: str):
        self.rest = rest
        self.market_code = market_code

    async def buy(self, stock_code, current_price, order_qty = 1):
        return current_price

    async def sell(self, stock_code: str, current_price: float):
        return current_price

    async def sell_all(self):
        return
