import asyncio
import trader.dbsec.api.overseas_order as order

from trader.base.base_thread import BaseThread

# -----------------------------------------------------------------------------
# BaseStrategy
# -----------------------------------------------------------------------------
class BaseStrategy(BaseThread):

    # 주식 매수 가격
    __purchase_price: float = 0.0

    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    ###########################################################################
    # 주식의 매수 금액을 반환 한다.
    ###########################################################################
    def get_purchase_price(self) -> float: return self.__purchase_price

    ###########################################################################
    # 주식을 매수 한다.
    ###########################################################################
    def buy_stock(self, stock_code: str):
        self.__purchase_price = asyncio.run(order.order_buy(stock_code))

    ###########################################################################
    # 주식을 매도 한다.
    ###########################################################################
    def sell_stock(self, stock_code: str):
        asyncio.run(order.order_sell(stock_code))

    ###########################################################################
    # 주식 거래를 마감 한다.
    ###########################################################################
    def treade_closed(self):
        return False

# end of class BaseStrategy
