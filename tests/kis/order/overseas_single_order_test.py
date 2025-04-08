import asyncio
import tests.const.test_data_values as conf

from trader.kis.order.overseas_single_order import OverseasSingleOrder

def get_stock_order():
    is_real: bool = True # 실전: True, 모의: False
    conf.get_test_config(is_real)
    return OverseasSingleOrder("AMEX", 1)

def buy(stock_order, stock_code):
    purchase_price = asyncio.run(stock_order.buy(stock_code))
    print(f"{purchase_price} buy end")

def sell(stock_order, stock_code):
    asyncio.run(stock_order.sell(stock_code))
    print("sell end")

if __name__ == "__main__":
    stock_order = get_stock_order()
    #buy(stock_order, "SOXL")
    sell(stock_order, "SOXL")
