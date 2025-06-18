import time
import trader.commons.utils as utils
import trader.dbsec.api.api_overseas as api

from trader.base.base_thread import BaseThread

# -----------------------------------------------------------------------------
# BaseStrategy
# -----------------------------------------------------------------------------
class BaseStrategy(BaseThread):
    __WEIGHT_BUY = 0.4
    __WEIGHT_SELL = -0.4

    # 주식 매수 가격
    __purchase_price: float = 0.0

    def __init__(self, config):
        super().__init__()
        self.__config = config
        self.__order_qty = config["order_qty"]
        self.__close_date_time = utils.add_date(1, "%Y%m%d030000")

    def execute(self):
        pass

    ###########################################################################
    # 주식을 매매 한다.
    ###########################################################################
    async def buy_stock(self, stock_code):
        order_price = await self.__order_market(stock_code, "2", self.__order_qty, self.__WEIGHT_BUY)
        return stock_code, order_price

    ###########################################################################
    # 주식을 매도 한다.
    ###########################################################################
    async def sell_stock(self, stock_code):
        order_price = self.__order_market(stock_code, "1", self.__order_qty, self.__WEIGHT_SELL)
        return stock_code, order_price

    # 주식 주문
    async def __order_market(self, stock_code, tp_code, order_qty=1, weight=0.0):
        prices = await api.inquiry_price(self.__config, stock_code)
        order_price = float(prices["Sdpr"]) + weight
        time.sleep(0.5)

        orders = await api.order(self.__config, stock_code, tp_code, order_price, order_qty)
        order_no = int(orders["OrdNo"])
        time.sleep(0.5)

        histories = await api.transaction_history(self.__config, stock_code, order_no)
        if len(histories) == 0: return 0
        return float(histories[0]["AstkExecAmt"])

    ###########################################################################
    # 주식 거래를 마감 한다.
    ###########################################################################
    def is_closed(self):
        curr_date_time = utils.get_date("%Y%m%d%H%M%S")
        return curr_date_time > self.__close_date_time

# -----------------------------------------------------------------------------
# end of class BaseStrategy
# -----------------------------------------------------------------------------