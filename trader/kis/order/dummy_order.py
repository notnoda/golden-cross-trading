import logging
import time
import trader.kis.api.overseas_price_quotations as stock_price

from trader.kis.order.stock_order import StockOrder

# -----------------------------------------------------------------------------
# - OverseasDummyOrder
# -----------------------------------------------------------------------------
class OverseasDummyOrder(StockOrder):

    __order_seq_no: int = 0

    def __init__(self, excg_cd: str):
        self.__excg_cd: str = excg_cd

    async def buy(self, stock_code: str) -> float:
        self.__order_seq_no += 1
        ord_price: float = await stock_price.get_current_price(self.__excg_cd, stock_code)
        logging.info(f"매수 : \t[{self.__order_seq_no}]\t[{stock_code}]\t[{ord_price}]")
        time.sleep(0.3)

        return ord_price

    async def sell(self, stock_code: str):
        ord_price = await stock_price.get_current_price(self.__excg_cd, stock_code)
        logging.info(f"매도 : \t[{self.__order_seq_no}]\t[{stock_code}]\t[{ord_price}]")
        time.sleep(0.3)

    def closed(self): pass

# end of class StockOrder
