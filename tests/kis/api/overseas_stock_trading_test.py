import asyncio
import tests.const.test_data_values as conf
import trader.kis.api.overseas_stock_trading as trading

async def inquire_balance(exchange, code):
    ord_psbl_qty: int = 0

    for data in await trading.inquire_balance(exchange):
        if data.pdno == code: ord_psbl_qty += data.psbl_qty

    print("================================================================================")
    print(ord_psbl_qty)
    print("================================================================================")

async def inquire_psamount(exchange, code):
    data = await trading.inquire_psamount(exchange, code, 15.10)
    print("================================================================================")
    print(data)
    print("================================================================================")

if __name__ == "__main__":
    is_real: bool = True # 실전: True, 모의: False
    config = conf.get_test_config(is_real)

    exchange = "AMS"
    code = "SOXS"

    #asyncio.run(inquire_balance(exchange, code))
    asyncio.run(inquire_psamount(exchange, code))

