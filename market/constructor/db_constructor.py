from market.config.db_config import DbConfig
from market.api.rest.db_rest import DbRest
from market.broker.db_overseas_broker import DbOverseasBroker
from market.provider.db_overseas_provider import DbOverseasProvider

def test(filename):
    config = DbConfig().get(filename)
    rest = DbRest(config["domain"], config["token"])
    broker = DbOverseasBroker(rest, config["market_code"])
    provider = DbOverseasProvider(rest, config["market_code"], config["tick_date"])
    strategy = ""
    return


if __name__ == '__main__':
    filename = "C:/_resources/golden-cross/config/db-trading.yaml"

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test start")
    test(filename)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test end")
