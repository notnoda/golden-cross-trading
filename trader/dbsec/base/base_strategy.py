import trader.commons.utils as utils
import trader.dbsec.api.api_overseas as api

from trader.base.base_thread import BaseThread

# -----------------------------------------------------------------------------
# BaseStrategy
# -----------------------------------------------------------------------------
class BaseStrategy(BaseThread):

    # 주식 매수 가격
    __purchase_price: float = 0.0

    def __init__(self):
        super().__init__()
        self.__close_date_time = utils.add_date(1, "%Y%m%d030000")

    def execute(self):
        pass

    ###########################################################################
    # 주식을 매수 한다.
    ###########################################################################
    async def buy_stock(self, config, stock_code, order_qty):
        order_price = await api.order_market_buy(config, stock_code, order_qty)
        return (stock_code, order_price)

    ###########################################################################
    # 주식을 매도 한다.
    ###########################################################################
    async def sell_stock(self, config, stock_code, order_qty):
        order_price = await api.order_market_sell(config, stock_code, order_qty)
        return (stock_code, order_price)

    ###########################################################################
    # 주식 거래를 마감 한다.
    ###########################################################################
    def is_closed(self):
        curr_date_time = utils.get_date("%Y%m%d%H%M%S")
        return curr_date_time > self.__close_date_time

# end of class BaseStrategy
