from abc import abstractmethod

# -----------------------------------------------------------------------------
# - StockOrder
# -----------------------------------------------------------------------------
class StockOrder:

    @abstractmethod
    def buy(self, stock_code: str) -> str: pass

    @abstractmethod
    def sell(self, stock_code: str) -> str: pass

    @abstractmethod
    def closed(self): pass

# end of class StockOrder
