import json
import pandas as pd
import requests

################################################################################
# API POST 호출
################################################################################
async def post(config, path, data):
    res = requests.post(
        url=get_base_url(config, path),
        headers=__get_headers(config),
        data=data,
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
    data = json.dumps({
        "In": {
            "InputCondMrktDivCode": config["market_code"],
            "InputIscd1": stock_code,
	    }
	})

    return await post(config, path, data)

################################################################################
################################################################################
################################################################################

################################################################################
# 틱봉 조회
################################################################################
async def chart_tick(config, stock_code, tick_size):
    path = "/api/v1/quote/overseas-stock/chart/tick"
    data = json.dumps({
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

    res = await post(config, path, data)
    return __get_json_to_dataframe(res)

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
# 주식 매매
################################################################################
async def order_sell(config, stock_code, order_qty=1):
    return await __order(config, stock_code, "1", order_qty)

async def order_buy(config, stock_code, order_qty=1):
    return await __order(config, stock_code, "2", order_qty)

async def __order(config, stock_code, tp_code, order_qty=1):
    path = "/api/v1/trading/overseas-stock/order"
    data = json.dumps({
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

    return await post(config, path, data)

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    domain = "https://openapi.dbsec.co.kr:8443"
    appkey = "PS1P3OIOWi3Su7vW9mL1mXpKfy5njebrUFAV"
    secretkey = "3RnDV1inhKS8FhMQ8nqI0lftUtc9xMYI"

    #get_access_token(domain, appkey, secretkey)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
