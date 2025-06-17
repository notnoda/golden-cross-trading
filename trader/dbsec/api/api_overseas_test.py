import asyncio

import trader.dbsec.api.access_token as access_token
import trader.dbsec.api.api_overseas as api
import trader.dbsec.common.read_config as read_config

def get_config(filename):
    config = read_config.read_config(filename)
    return access_token.add_access_token(config)

################################################################################
################################################################################
################################################################################

def inquiry_price(config, stock_code):
    data = asyncio.run(api.inquiry_price(config, stock_code))
    print(data)

def order_buy(config, stock_code):
    data = asyncio.run(api.order_market_buy(config, stock_code))
    print(data)

def order_sell(config, stock_code):
    data = asyncio.run(api.order_market_sell(config, stock_code))
    print(data)

def transaction_history(config, stock_code, order_no=1270):
    data = asyncio.run(api.transaction_history(config, stock_code, order_no))
    print(data)

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> api_overseas test start")
    filename = "C:/_resources/golden-cross/config/db-trading.yaml"
    config = get_config(filename)

    # 매수주문
    order_sell(config, "SOXL")

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> api_overseas test end")
