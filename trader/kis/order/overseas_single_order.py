import logging
import time
import trader.kis.api.overseas_stock_trading as stock_order
import trader.kis.api.overseas_price_quotations as stock_price

from trader.kis.order.stock_order import StockOrder

# -----------------------------------------------------------------------------
# - OverseasSingleOrder
# -----------------------------------------------------------------------------
class OverseasSingleOrder(StockOrder):

    __order_seq_no: int = 0

    def __init__(self, exchange, order_qty):
        self.__exchange = exchange
        self.__order_qty = order_qty

    ###########################################################################
    # 주식을 매수 한다.
    ###########################################################################
    async def buy(self, code):
        await self.check_buy_order()

        self.__order_seq_no += 1
        ord_price = await stock_price.get_current_price(self.__exchange, code)
        add_price = ord_price + 1
        order_qty = await self.__order_able_qty(code, add_price)

        logging.info(f"매수 : \t[{self.__order_seq_no}]\t[{code}]\t[{ord_price}]")
        await stock_order.order_buy(self.__exchange, code, add_price, order_qty)
        time.sleep(1)

        return ord_price

    ###########################################################################
    # 미체결 여부를 확인 한다.
    ###########################################################################
    async def check_buy_order(self):
        while True:
            if await stock_order.is_nccs(self.__exchange):
                time.sleep(0.1)
                break
            time.sleep(1)

    ###########################################################################
    # 주식 매수가 가능한 주수를 조회 한다.
    ###########################################################################
    async def __order_able_qty(self, stock_code, ord_price):
        order_able = await stock_order.inquire_psamount(self.__exchange, stock_code, ord_price)
        return self.__order_qty if order_able.psbl_qty > self.__order_qty else order_able.psbl_qty

    ###########################################################################
    # 매도 가능 주수를 조회한 후 매도 한다.
    ###########################################################################
    async def sell(self, code):
        balances = await stock_order.inquire_balance(self.__exchange)
        stock_qty: int = 0

        for data in balances:
            if data.pdno == code: stock_qty += data.psbl_qty

        await self.__sell_qty(code, stock_qty)

    ###########################################################################
    # 주식을 매도 한다.
    ###########################################################################
    async def __sell_qty(self, code, stock_qty):
        ord_price = await stock_price.get_current_price(self.__exchange, code)

        logging.info(f"매도 : \t[{self.__order_seq_no}]\t[{code}]\t[{ord_price}]")
        await stock_order.order_sell(self.__exchange, code, ord_price - 0.4, stock_qty)
        time.sleep(1)

    ###########################################################################
    # 모든 주식을 매도 한다.
    ###########################################################################
    async def closed(self):
        balances = await stock_order.inquire_balance(self.__exchange)
        for data in balances: await self.__sell_qty(data.pdno, data.psbl_qty)

# end of class OverseasSingleOrder
