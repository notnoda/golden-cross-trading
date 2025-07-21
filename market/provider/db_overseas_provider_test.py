import asyncio
from market.config.db_config import DbConfig
from market.api.rest.db_rest import DbRest
from market.provider.db_overseas_provider import DbOverseasProvider

async def test(filename):
    config = DbConfig().get(filename)
    rest = DbRest(config["domain"], config["token"])
    provider = DbOverseasProvider(rest, config["market_code"], config["tick_date"])

    data = await provider.chart("SOXL", 10)
    print(data)

if __name__ == '__main__':
    filename = "C:/_resources/golden-cross/config/db-trading.yaml"

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test start")
    asyncio.run(test(filename))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test end")
