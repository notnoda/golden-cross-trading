import logging
import json
import pandas as pd
import requests

from pandas.core.interchange.dataframe_protocol import DataFrame

# SSL 경고 무시
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

################################################################################
# API POST 호출
################################################################################
async def post(config, path, params):

    url = config["domain"] + path
    res = requests.post(
        url=url,
        headers=__get_headers(config),
        data=params,
        verify=False
    )

    if res.status_code == 200:
        try:
            data = json.dumps(res.json(), ensure_ascii=False, indent=4)
            return json.loads(data)["Out"]
        except:
            logging.error(res)
            return None
    else:
        print("Error Code : " + str(res.status_code))
        print(json.dumps(res.text, ensure_ascii=False, indent=4))
        return None

# API 헤더
def __get_headers(config):
    return {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {config['access_token']}",
        "cont_yn": "",
        "cont_key": "",
    }

################################################################################
# 현재가 조회
################################################################################
async def inquiry_price(config, stock_code):
    path = "/api/v1/quote/overseas-stock/inquiry/price"
    params = json.dumps({
        "In": {
            "InputCondMrktDivCode": config["market_code"],
            "InputIscd1": stock_code,
	    }
	})

    return await post(config, path, params)

################################################################################
# 틱봉 조회
################################################################################
async def chart_tick(config, stock_code, tick_size) -> DataFrame:
    path = "/api/v1/quote/overseas-stock/chart/tick"
    params = json.dumps({
        "In": {
            "InputPwDataIncuYn": "Y",
            "InputOrgAdjPrc": "1",
            "dataCnt": "",
            "InputHourClsCode": "0",
            "InputCondMrktDivCode": config["market_code"],
            "InputIscd1": stock_code,
            "InputDate1": config["srtDt"],
            "InputDivXtick": str(tick_size),
	    }
	})

    data = await post(config, path, params)
    df = pd.DataFrame(data)
    df.columns = [ "hour", "date", "close", "open", "high", "low", "volumns" ]
    return df.sort_index(ascending=False)

################################################################################
# 해외주식 주문
################################################################################
async def order(config, stock_code, tp_code, order_price, order_qty=1):
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

    return await post(config, path, params)

################################################################################
# 체결내역조회
################################################################################
async def transaction_history(config, stock_code, order_no=None):
    path = "/api/v1/trading/overseas-stock/inquiry/transaction-history"
    params = json.dumps({
        "In": {
            "QrySrtDt": config["srtDt"], #조회시작일자
            "QryEndDt": config["endDt"], #조회종료일자
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

    history = await post(config, path, params)
    if order_no is None: return history
    return list(filter(lambda data : data["OrdNo"] == int(order_no), history))

################################################################################
