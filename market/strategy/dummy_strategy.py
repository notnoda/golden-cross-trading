from market.base.strategy import Strategy
from market.base.provider import Provider

class DummyStrategy(Strategy):

    def __init__(self, provider: Provider, stock_long: str, stock_short: str):
        self.provider = provider
        self.stock_long = stock_long
        self.stock_short = stock_short

    async def is_buy(self) -> (str, float):
        return self.stock_long, 10.0

    def before_sell(self, buy_price: float):
        self.buy_price = buy_price

    async def is_sell(self, stock_code: str) -> (str, float):
        return stock_code, self.buy_price

    async def is_closed(self) -> bool:
        return False
