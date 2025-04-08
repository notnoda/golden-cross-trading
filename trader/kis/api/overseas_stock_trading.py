import trader.kis.api.fetch as fetch

from trader.errors.trading_error import TradingOrderBuyError, TradingOrderSellError
from trader.kis.api.access_config import AccessConfig
from trader.kis.api.response import APIResponse

# 해외 거래소 코드 - NASD:나스닥, NYSE:뉴욕, AMEX:아멕스
# ------------------------------------------------------------------------------
# - OverseasStockOrderData
# ------------------------------------------------------------------------------
class OverseasStockOrderData:
    pdno     = None #
    psbl_qty = None # 보유 주식/주문 가능 수량
    psbl_amt = None # 주문 가능 금액

    def __init__(self, pdno="", psbl_qty="0", psbl_amt="0.0"):
        self.pdno = pdno
        self.psbl_qty = int(psbl_qty)
        self.psbl_amt = float(psbl_amt)
# end of class OverseasStockOrderData

################################################################################
# 해외 주식을 주문 한다.[v1_해외 주식-001]
# - exchange: 해외 거래소 코드 - NYSE:뉴욕, NASD:나스닥, AMEX:아멕스
# - code:     상품 번호 - 종목 코드
# - price:    해외 주문 단가
# - qty:      주문 수량
################################################################################
# 해외 주식을 매수 주문 한다.
async def order_buy(exchange, code, price, qty):
    rt_cd, msg = await __order_execute("TTTT1002U", exchange, code, price, qty)
    if rt_cd != "0": raise TradingOrderBuyError(f"매수 주문 실패: {msg}")

# 해외 주식을 매도 주문 한다.
async def order_sell(exchange, code, price, qty):
    rt_cd, msg = await __order_execute("TTTT1006U", exchange, code, price, qty, "00")
    if rt_cd != "0": raise TradingOrderSellError(f"매도 주문 실패: {msg}")

# 해외 주식을 매매 주문 한다.
async def __order_execute(tr_id, exchange, code, price, qty, sll_type=""):
    if qty == 0: return

    params = {
        "CANO":            AccessConfig().account_no(),
        "ACNT_PRDT_CD":    AccessConfig().product_no(),
        "OVRS_EXCG_CD":    exchange,
        "PDNO":            code,
        "OVRS_ORD_UNPR":   f"{price:.2f}",
        "ORD_QTY":         str(qty),
        "CTAC_TLNO":       "",   # 연락 전화 번호
        "MGCO_APTM_ODNO":  "",   # 운용사 지정 주문 번호
        "ORD_SVR_DVSN_CD": "0",  # 주문 서버 구분 코드 - 0:Default
        "ORD_DVSN":        "00", # 주문 구분 - 00:지정가
    }

    # 판매 유형 - 제거:매수, 00:매도
    if sll_type != "": params["SLL_TYPE"] = "00"

    # API 호출
    res = await fetch.fetch_post(
        path="/uapi/overseas-stock/v1/trading/order",
        tr_id=tr_id,
        params=params
    )

    # 결과 반환
    data = res.get_body()
    return data.rt_cd, data.msg1

################################################################################
# 해외 주식의 매수 가능 금액을 조회 한다.[v1_해외 주식-014]
# - exchange: 해외 거래소 코드 - NYSE:뉴욕, NASD:나스닥, AMEX:아멕스
# - code:     상품 번호 - 종목 코드
# - price:    해외 주문 단가
################################################################################
async def inquire_psamount(exchange, code, price):
    params = {
        "CANO":          AccessConfig().account_no(),
        "ACNT_PRDT_CD":  AccessConfig().product_no(),
        "OVRS_EXCG_CD":  exchange,
        "OVRS_ORD_UNPR": f"{price:.2f}",
        "ITEM_CD":       code,
    }

    res = await fetch.fetch_get(
        path="/uapi/overseas-stock/v1/trading/inquire-psamount",
        tr_id="TTTS3007R",
        params=params
    )

    data = res.get_body().output
    return OverseasStockOrderData(psbl_qty=data["ord_psbl_qty"], psbl_amt=data["ovrs_ord_psbl_amt"])

################################################################################
# 해외 주식의 잔고를 조회 한다.[v1_해외 주식-006]
# - exchange: 해외 거래소 코드 - NYSE:뉴욕, NASD:나스닥, AMEX:아멕스
################################################################################
async def inquire_balance(exchange):
    params = {
        "CANO":         AccessConfig().account_no(),
        "ACNT_PRDT_CD": AccessConfig().product_no(),
        "OVRS_EXCG_CD": exchange,
        "TR_CRCY_CD":   "USD",
        "CTX_AREA_FK200": "", # 연속 조회 검색 조건 200
        "CTX_AREA_NK200": "", # 연속 조회키 200
    }

    res = await fetch.fetch_get(
        path="/uapi/overseas-stock/v1/trading/inquire-balance",
        tr_id="TTTS3012R",
        params=params
    )

    balances = map(lambda data: __set_balance_data(data), res.get_body().output1)
    return list(balances)

def __set_balance_data(data):
    return OverseasStockOrderData(pdno=data["ovrs_pdno"], psbl_qty=data["ord_psbl_qty"])

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

################################################################################
# ---------- 해외 주식의 미체결 내역을 조회 한다.[v1_해외 주식-005]
################################################################################
async def inquire_nccs(excg_cd: str) -> APIResponse:
    params = {
        "CANO":           AccessConfig().account_no(),
        "ACNT_PRDT_CD":   AccessConfig().product_no(),
        "OVRS_EXCG_CD":   excg_cd, # 해외 거래소 코드
        "SORT_SQN":       "DS", # 정렬 순서 - DS:정순, 그외:역순
        "CTX_AREA_FK200": "", # 연속 조회키 200 -
        "CTX_AREA_NK200": "", # 연속 조회 검색 조건 200 -
    }

    return await fetch.fetch_get(
        path="/uapi/overseas-stock/v1/trading/inquire-nccs",
        tr_id="TTTS3018R",
        params=params
    )

async def is_nccs(excg_cd: str) -> bool:
    nccs = await inquire_nccs(excg_cd)
    return len(nccs.get_body().output) == 0

################################################################################
# ---------- 해외 주식의 주문 체결 내역을 조회 한다.[v1_해외 주식-007]
################################################################################
async def inquire_ccld(excg_cd: str, current_date: str) -> APIResponse:
    params = {
        "CANO":         AccessConfig().account_no(),
        "ACNT_PRDT_CD": AccessConfig().product_no(),
        "ORD_STRT_DT":  current_date, # 주문 시작 일자
        "ORD_END_DT":   current_date, # 주문 종료 일자
        "OVRS_EXCG_CD": excg_cd,      # 해외 거래소 코드 - %:전종목, NASD:미국 시장 전체(나스닥, 뉴욕, 아멕스), NYSE:뉴욕, AMEX:아멕스
        "PDNO":           "%",  # 상품 번호 - 전 종목일 경우 "%" 입력
        "SLL_BUY_DVSN":   "00", # 매도/매수 구분 - 00:전체, 01:매도, 02:매수
        "CCLD_NCCS_DVSN": "02", # 체결/미체결 구분 - 00:전체, 01:체결, 02:미체결
        "SORT_SQN":       "DS", # 정렬 순서 - DS:정순, AS:역순
        "ORD_DT":         "",   # 주문 일자 - "" (Null 값 설정)
        "ORD_GNO_BRNO":   "",   # 주문 채번 지점 번호 - "" (Null 값 설정)
        "ODNO":           "",   # 주문 번호 - "" (Null 값 설정)
        "CTX_AREA_NK200": "",   # 연속 조회키 200 -
        "CTX_AREA_FK200": "",   # 연속 조회 검색 조건 200 -
    }

    return await fetch.fetch_get(
        path="/uapi/overseas-stock/v1/trading/inquire-ccnl",
        tr_id="TTTS3035R",
        params=params
    )
