import logging
import json
import commons.utils as utils

from market.base.broker import Broker
from market.base.rest import Rest

class DbOverseasBroker(Broker):
    __WEIGHT_BUY = 0.4
    __WEIGHT_SELL = -0.4

    def __init__(self, rest: Rest, market_code: str):
        self.rest = rest
        self.market_code = market_code
        self.start_dt = utils.get_date()
        self.end_dt = utils.add_date(1)

    # 주식을 매수 한다.
    async def buy(self, stock_code, current_price, order_qty = 1):
        # 1. 시장가 매수를 한다.
        history = await self.order_market(stock_code, "2", order_qty, self.__WEIGHT_BUY)

        # 2. 미체결 된 주식 주문을 취소 한다.
        if float(history["AstkOrdRmqty"]) > 0:  # 미체결 주식 수
            await self.cancel(stock_code, int(history["OrdNo"]))

        # 체결 된 주식 가격과 주식 수를 확인 한다.
        exec_qty = float(history["AstkExecQty"]) # 매수한 주식 수
        exec_prc = float(history["AstkExecPrc"]) # 매수한 주식 가격

        # 체결 된 주식 가격을 반환 한다.
        return exec_prc if exec_qty > 0 else None

    # 주식을 매도 한다.
    async def sell(self, stock_code, current_price):
        # 1. 주식 잔고를 조회 한다.
        balances = await self.inquiry_qty(stock_code)
        if len(balances) == 0: return stock_code, 0

        # 2. 보유 주식 수를 확인 한다.
        order_qty = int(float(balances[0]["AstkOrdAbleQty"]))

        # 3. 주식을 매도 한다.
        data = await self.order_market(stock_code, "1", order_qty, self.__WEIGHT_SELL)

        # 4. 매도한 주식 가격을 반환 한다.
        return float(data["AstkExecPrc"])

    async def sell_all(self):
        # TODO - 구현 할 것
        pass

    # 시장가 주문을 한다.
    async def order_market(self, stock_code, tp_code, order_qty=1, weight=0.0):
        prices = await self.inquiry_price(stock_code)
        order_price = round(float(prices["Prpr"]) + weight, 2)

        orders = await self.order(stock_code, tp_code, order_price, order_qty)
        order_no = int(orders["OrdNo"])

        histories = await self.history(stock_code, order_no)
        history = histories[0]

        message = f"매매: {tp_code}\t주식코드: {stock_code}"
        message += f"\t현재가: {prices['Prpr']}\t지정가: {order_price}"
        message += f"\t주문가: {history['AstkOrdPrc']}\t체결가: {history['AstkExecPrc']}"
        message += f"\t체결량: {history['AstkExecQty']}\t미체결: {history['AstkOrdRmqty']}"
        logging.info(message)

        return history

    ################################################################################
    # API 호출
    ################################################################################

    # 현재 주식 가격을 조회 한다.
    async def inquiry_price(self, stock_code):
        path = "/api/v1/quote/overseas-stock/inquiry/price"
        params = json.dumps({
            "In": {
                "InputCondMrktDivCode": self.market_code,
                "InputIscd1": stock_code,
            }
        })

        return await self.rest.post(path, params)

    # 주식을 매수 또는 매도 주문을 한다.
    async def order(self, stock_code, tp_code, order_price, order_qty=1):
        path = "/api/v1/trading/overseas-stock/order"
        params = json.dumps({
            "In": {
                "AstkIsuNo" : stock_code,
                "AstkBnsTpCode" : tp_code, #해외주식매매구분코드(1:매도, 2:매수)
                "AstkOrdprcPtnCode" : "1", #해외주식호가유형코드(1:지정가, 2:시장가)
                "AstkOrdCndiTpCode" : "1", #해외주식주문조건구분코드
                "AstkOrdQty" : order_qty, #해외주식주문수량
                "AstkOrdPrc" : order_price, #해외주식주문가격(시장가주문시: 0)
                "OrdTrdTpCode" : "0", #주문거래구분코드(0:주문, 1:정정주문, 2:취소주문)
                "OrgOrdNo" : 0 #원주문번호(매수/매도주문시:0)
            }
        })

        return await self.rest.post(path, params)

    # 주식 거개 체결 내역을 조회 한다.
    async def history(self, stock_code, order_no=None):
        path = "/api/v1/trading/overseas-stock/inquiry/transaction-history"
        params = json.dumps({
            "In": {
                "QrySrtDt": self.start_dt, #조회시작일자
                "QryEndDt": self.end_dt, #조회종료일자
                "AstkIsuNo": stock_code, #해외주식종목번호
                "AstkBnsTpCode": "0", #해외주식매매구분코드(0:전체, 1:매도, 2:매수)
                "OrdxctTpCode": "0", #주문체결구분코드(0:전체, 1:체결, 2:미체결)
                "StnlnTpCode": "1", #정렬구분코드(0:역순, 1:정순)
                "QryTpCode": "0", #조회구분코드(0:합산별, 1:건별)
                "OnlineYn": "0", #온라인여부(0:전체, Y:온라인, N:오프라인)
                "CvrgOrdYn": "0", #반대매매주문여부(0:전체, Y:반대매매, N:일반주문)
                "WonFcurrTpCode": "2", #원화외화구분코드(1:원화, 2:외화)
            }
        })

        history = await self.rest.post(path, params)
        if order_no is None: return history
        return list(filter(lambda data : data["OrdNo"] == int(order_no), history))

    # 주문을 취소 한다.
    async def cancel(self, stock_code, order_no):
        path = "/api/v1/trading/overseas-stock/order"
        params = json.dumps({
            "In": {
                "AstkIsuNo" : stock_code,
                "AstkOrdCndiTpCode" : "1", #해외주식주문조건구분코드
                "OrdTrdTpCode" : "2", #주문거래구분코드(0:주문, 1:정정주문, 2:취소주문)
                "OrgOrdNo" : order_no #원주문번호(매수/매도주문시:0)
            }
        })

        return await self.rest.post(path, params)

    # 잔고 및 증거금을 조회 한다.
    async def inquiry_balance(self, name="Out"):
        path = "/api/v1/trading/overseas-stock/inquiry/balance-margin"
        params = json.dumps({
            "In": {
                "TrxTpCode": "2", #처리구분코드(1:외화잔고, 2:주식잔고상세, 3:주식잔고(국가별), 9:당일실현손익)
                "CmsnTpCode": "2", #수수료구분코드(0:전부 미포함, 1:매수제비용만 포함, 2:매수제비용+매도제비용)
                "WonFcurrTpCode": "2", #원화외화구분코드(1:원화, 2:외화)
                "DpntBalTpCode": "1", #소수점잔고구분코드(0:전체, 1:일반, 2: 소수점)
            }
        })

        return await self.rest.post(path, params, name)

    # 보유 주식 수를 조회 한다.
    async def inquiry_qty(self, stock_code=None):
        balances = await self.inquiry_balance("Out2")
        if stock_code is None: return balances
        return list(filter(lambda data : data["SymCode"] == stock_code, balances))

