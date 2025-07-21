import asyncio
from market.config.db_config import DbConfig
from market.api.rest.db_rest import DbRest
from market.broker.db_overseas_broker import DbOverseasBroker

async def test(filename):
    config = DbConfig().get(filename)
    rest = DbRest(config["domain"], config["token"])
    broker = DbOverseasBroker(rest, config["market_code"])

    #price = await broker.buy("SOXL", 0)
    #price = await broker.sell("SOXL", 0)
    print(price)

if __name__ == '__main__':
    filename = "C:/_resources/golden-cross/config/db-trading.yaml"

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test start")
    asyncio.run(test(filename))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test end")
