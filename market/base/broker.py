from abc import ABC, abstractmethod

class Broker(ABC):

    @abstractmethod
    async def buy(self, stock_code: str, current_price: float, order_qty = 1) -> float:
        pass

    @abstractmethod
    async def sell(self, stock_code: str, current_price: float) -> float:
        pass

    @abstractmethod
    async def sell_all(self):
        pass
