import trader.kis.api.fetch as fetch

from trader.kis.api.response import APIResponse

################################################################################
# 거래소 코드를 변환 한다.
################################################################################
def transform_exchange(exchange):
    if   exchange == "NASD": return "NYS" # 뉴욕
    elif exchange == "NYSE": return "NAS" # 나스닥
    elif exchange == "AMEX": return "AMS" # 아멕스
    else: return exchange

################################################################################
# 해외 주식 현재 체결가[v1_해외 주식-009]
# - exchange: 거래소 코드 - NYS:뉴욕, NAS:나스닥, AMS:아멕스
# - code:     종목 코드
################################################################################
async def get_current_price(exchange, code):
    params = {
        "AUTH": "",
        "SYMB": code,
        "EXCD": transform_exchange(exchange),
    }

    res: APIResponse = await fetch.fetch_get(
        path="/uapi/overseas-price/v1/quotations/price",
        tr_id="HHDFS00000300",
        params=params
    )

    price = res.get_body().output["last"]
    return 0.0 if price == "" else float(price)

################################################################################
# 해외 주식 분봉 조회[v1_해외 주식-030]
# - exchange: 거래소 코드 - NYS:뉴욕, NAS:나스닥, AMS:아멕스
# - code:     종목 코드
# - minute:   분갭(분단위 - 1: 1분봉, 2: 2분봉, ...)
################################################################################
async def inquire_time_chart(exchange, code, minute="3"):
    params = {
        "AUTH": "",
        "SYMB": code,
        "EXCD": transform_exchange(exchange),
        "NMIN": minute,
        "PINC": "1"
    }

    res = await fetch.fetch_get(
        path="/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice",
        tr_id="HHDFS76950200",
        params=params
    )

    ticks = res.get_body().output2[::-1]
    return ticks
