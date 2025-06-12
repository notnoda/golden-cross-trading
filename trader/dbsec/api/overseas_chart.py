import json
import trader.dbsec.api.access_api as api

################################################################################
# 실시간(웹소켓) 접속 키를 발급 한다.
################################################################################
async def chart_tick(config, market_code, stock_code, tick_size):
    path = "/api/v1/quote/overseas-stock/chart/tick"
    data = json.dumps({
        "In": {
            "InputPwDataIncuYn": "Y",
            "InputOrgAdjPrc": "1",
            "dataCnt": "",
            "InputHourClsCode": "0",
            "InputCondMrktDivCode": market_code,
            "InputIscd1": stock_code,
            "InputDate1": config["today"],
            "InputDivXtick": tick_size,
	    }
	})

    res = await api.post(config, path, data)
    if res.status_code == 200:
        data = json.dumps(res.json(), ensure_ascii=False, indent=4)
        return json.loads(data)["Out"]
    else:
        print("Error Code : " + str(res.status_code))
        print(json.dumps(res.text, ensure_ascii=False, indent=4))
        return None
