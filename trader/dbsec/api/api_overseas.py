import json
import pandas as pd
import requests
from pandas.core.interchange.dataframe_protocol import DataFrame


################################################################################
# API POST 호출
################################################################################
async def post(config, path, params):
    res = requests.post(
        url=get_base_url(config, path),
        headers=__get_headers(config),
        data=params,
        verify=False
    )

    if res.status_code == 200:
        data = json.dumps(res.json(), ensure_ascii=False, indent=4)
        return json.loads(data)["Out"]
    else:
        print("Error Code : " + str(res.status_code))
        print(json.dumps(res.text, ensure_ascii=False, indent=4))
        return None

################################################################################
# API 기본 도메인
################################################################################
def get_base_url(config, path):
    return config["domain"] + path

################################################################################
# API 헤더
################################################################################
def __get_headers(config):
    return {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {config['access_token']}",
        "cont_yn": "",
        "cont_key": "",
    }

################################################################################
################################################################################
################################################################################

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
################################################################################
################################################################################

################################################################################
# 틱봉 조회
################################################################################
async def chart_tick(config, stock_code, tick_size) -> DataFrame:
    """

    :rtype: object
    """
    path = "/api/v1/quote/overseas-stock/chart/tick"
    params = json.dumps({
        "In": {
            "InputPwDataIncuYn": "Y",
            "InputOrgAdjPrc": "1",
            "dataCnt": "",
            "InputHourClsCode": "0",
            "InputCondMrktDivCode": config["market_code"],
            "InputIscd1": stock_code,
            "InputDate1": config["today"],
            "InputDivXtick": tick_size,
	    }
	})

    data = await post(config, path, params)
    return __get_json_to_dataframe(data)

################################################################################
# API 결과 변환
################################################################################
def __get_json_to_dataframe(data):
    df = pd.DataFrame(data)
    df.columns = [ "hour", "date", "close", "open", "high", "low", "volumns" ]
    return df

################################################################################
################################################################################
################################################################################

################################################################################
# 해외주식 주문
################################################################################
async def order_sell(config, stock_code, order_qty=1):
    return await __order(config, stock_code, "1", order_qty)

async def order_buy(config, stock_code, order_qty=1):
    return await __order(config, stock_code, "2", order_qty)

async def __order(config, stock_code, tp_code, order_qty=1):
    path = "/api/v1/trading/overseas-stock/order"
    params = json.dumps({
        "In": {
            "AstkIsuNo" : stock_code,
            "AstkBnsTpCode" : tp_code, #해외주식매매구분코드(1:매도, 2:매수)
            "AstkOrdprcPtnCode" : "2", #해외주식호가유형코드(1:지정가, 2:시장가)
            "AstkOrdCndiTpCode" : "1", #해외주식주문조건구분코드
            "AstkOrdQty" : order_qty, #해외주식주문수량
            "AstkOrdPrc" : 0, #해외주식주문가격(시장가주문시: 0)
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
            "QrySrtDt": config["today"], #조회시작일자
            "QryEndDt": config["today"], #조회종료일자
            "AstkIsuNo": stock_code, #해외주식종목번호
            "AstkBnsTpCode": 0, #해외주식매매구분코드(0:전체, 1:매도, 2:매수)
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
    return filter(lambda data : data["OrdNo"] == order_no, history)

################################################################################
# 체결금액조회
################################################################################
async def transaction_amount(config, stock_code, order_no):
    list = await transaction_history(config, stock_code, order_no)
    if len(list) == 0: return 0
    return list[0]["AstkExecAmt"]

################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    domain = "https://openapi.dbsec.co.kr:8443"
    appkey = "PS1P3OIOWi3Su7vW9mL1mXpKfy5njebrUFAV"
    secretkey = "3RnDV1inhKS8FhMQ8nqI0lftUtc9xMYI"

    #get_access_token(domain, appkey, secretkey)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
