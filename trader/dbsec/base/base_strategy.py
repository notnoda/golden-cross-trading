import logging
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
        history = await self.__order_market(stock_code, "2", self.__order_qty, self.__WEIGHT_BUY)

        if float(history["AstkOrdRmqty"]) > 0:
            await api.cancel_order(self.__config, stock_code, int(history["OrdNo"]))

        if float(history["AstkExecQty"]) == 0: return None
        else: return float(history["AstkExecPrc"])

    ###########################################################################
    # 주식을 매도 한다.
    ###########################################################################
    async def sell_stock(self, stock_code):
        balances = await api.inquiry_balance_qty(self.__config, stock_code)
        if len(balances) == 0: return stock_code, 0

        order_qty = int(float(balances[0]["AstkOrdAbleQty"]))
        history = await self.__order_market(stock_code, "1", order_qty, self.__WEIGHT_SELL)
        return float(history["AstkExecPrc"])

    # 주식 주문
    async def __order_market(self, stock_code, tp_code, order_qty=1, weight=0.0):
        prices = await api.inquiry_price(self.__config, stock_code)
        order_price = round(float(prices["Prpr"]) + weight, 2)
        time.sleep(0.5)

        orders = await api.order(self.__config, stock_code, tp_code, order_price, order_qty)
        order_no = int(orders["OrdNo"])
        time.sleep(0.5)

        histories = await api.transaction_history(self.__config, stock_code, order_no)
        history = histories[0]

        message = f"매매: {tp_code}\t주식코드: {stock_code}"
        message += f"\t현재가: {prices['Prpr']}\t지정가: {order_price}"
        message += f"\t주문가: {history['AstkOrdPrc']}\t체결가: {history['AstkExecPrc']}"
        message += f"\t체결량: {history['AstkExecQty']}\t미체결: {history['AstkOrdRmqty']}"
        logging.info(message)

        return history

    ###########################################################################
    # 주식 거래를 마감 한다.
    ###########################################################################
    def is_closed(self):
        curr_date_time = utils.get_date("%Y%m%d%H%M%S")
        return curr_date_time > self.__close_date_time

# -----------------------------------------------------------------------------
# end of class BaseStrategy
# -----------------------------------------------------------------------------