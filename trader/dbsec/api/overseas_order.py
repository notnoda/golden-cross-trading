import json
import trader.dbsec.api.access_api as api

################################################################################
# 실시간(웹소켓) 접속 키를 발급 한다.
################################################################################
async def order(config, stock_code, tp_code, order_qty=1):
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

    res = await api.post(config, path, data)
    if res.status_code == 200:
        data = json.dumps(res.json(), ensure_ascii=False, indent=4)
        return json.loads(data)["Out"]
    else:
        print("Error Code : " + str(res.status_code))
        print(json.dumps(res.text, ensure_ascii=False, indent=4))
        return None

async def order_sell(config, stock_code, order_qty=1):
    return await order(config, stock_code, "1", order_qty=1)

async def order_buy(config, stock_code, order_qty=1):
    return await order(config, stock_code, "2", order_qty=1)
