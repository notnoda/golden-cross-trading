from abc import ABC, abstractmethod

class Strategy(ABC):

    @abstractmethod
    async def is_buy(self) -> (str, float):
        pass

    @abstractmethod
    def before_sell(self, buy_price: float):
        pass

    @abstractmethod
    async def is_sell(self, stock_code: str) -> (str, float):
        pass

    @abstractmethod
    async def is_closed(self) -> bool:
        pass
