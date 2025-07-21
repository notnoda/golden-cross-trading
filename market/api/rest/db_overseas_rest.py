import json
import pandas as pd

from pandas.core.interchange.dataframe_protocol import DataFrame
from market.api.rest.db_rest import DbRest

class DbOverseasRest(DbRest):

    def __init__(self, domain, token, market_code):
        super().__init__(domain, token)
        self.domain = domain
        self.token = token
        self.market_code = market_code
        self.start_date = ""
        self.end_date = ""

    ################################################################################
    # 틱봉을 조회 한다.
    ################################################################################
    async def chart_tick(self, stock_code, tick_size, tick_date) -> DataFrame:
        path = "/api/v1/quote/overseas-stock/chart/tick"
        params = json.dumps({
            "In": {
                "InputPwDataIncuYn": "Y",
                "InputOrgAdjPrc": "1",
                "dataCnt": "500",
                "InputHourClsCode": "0",
                "InputCondMrktDivCode": self.market_code,
                "InputIscd1": stock_code,
                "InputDate1": tick_date,
                "InputDivXtick": str(tick_size),
            }
        })

        data = await self.post(path, params)
        df = pd.DataFrame(data)
        df.columns = ["hour", "date", "close", "open", "high", "low", "volumns"]
        return df.sort_index(ascending=False)

    ################################################################################
    # 현재 주식 가격을 조회 한다.
    ################################################################################
    async def inquiry_price(self, stock_code):
        path = "/api/v1/quote/overseas-stock/inquiry/price"
        params = json.dumps({
            "In": {
                "InputCondMrktDivCode": self.market_code,
                "InputIscd1": stock_code,
            }
        })

        return await self.post(path, params)

    ################################################################################
    # 주식 거개 체결 내역을 조회 한다.
    ################################################################################
    async def history(self, stock_code, order_no=None):
        path = "/api/v1/trading/overseas-stock/inquiry/transaction-history"
        params = json.dumps({
            "In": {
                "QrySrtDt": self.start_date, #조회시작일자
                "QryEndDt": self.end_date, #조회종료일자
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

        history = await self.post(path, params)
        if order_no is None: return history
        return list(filter(lambda data : data["OrdNo"] == int(order_no), history))

    ################################################################################
    # 잔고 및 증거금을 조회 한다.
    ################################################################################
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

        return await self.post(path, params, name)

    ################################################################################
    # 보유 주식 수를 조회 한다.
    ################################################################################
    async def inquiry_qty(self, stock_code=None):
        balances = await self.inquiry_balance("Out2")
        if stock_code is None: return balances
        return list(filter(lambda data : data["SymCode"] == stock_code, balances))

    ################################################################################
    # 주식을 매수 또는 매도 주문을 한다.
    ################################################################################
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

        return await self.post(path, params)

    ################################################################################
    # 주문을 취소 한다.
    ################################################################################
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

        return await self.post(path, params)
