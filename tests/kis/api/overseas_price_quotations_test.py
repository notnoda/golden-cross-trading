import asyncio
import trader.kis.api.overseas_price_quotations as overseas
import tests.const.test_data_values as conf

async def get_current_price(exchange, code):
    price = await overseas.get_current_price(exchange, code)
    print("================================================================================")
    print(price)
    print("================================================================================")

async def inquire_time_chart(exchange, code):
    res = await overseas.inquire_time_chart(exchange, code, "3")
    print("================================================================================")
    print(res)
    print("================================================================================")

if __name__ == "__main__":
    is_real = False # real = True, tests = False
    conf.get_test_config(is_real)

    exchange = "AMS"
    code = "SOXS"

    #asyncio.run(get_current_price(exchange, code))
    asyncio.run(inquire_time_chart(exchange, code))
