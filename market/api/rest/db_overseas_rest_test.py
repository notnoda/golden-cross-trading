import asyncio
from market.config.db_config import DbConfig
from market.api.rest.db_overseas_rest import DbOverseasRest

async def test(filename):
    config = DbConfig().get(filename)
    rest = DbOverseasRest(config["domain"], config["token"], config["market_code"], "")

    data = await rest.history("SOXL", 1437)
    #price = asyncio.run(broker.sell("SOXL", 0))
    print(data)

if __name__ == '__main__':
    filename = "C:/_resources/golden-cross/config/db-trading.yaml"

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test start")
    asyncio.run(test(filename))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test end")
