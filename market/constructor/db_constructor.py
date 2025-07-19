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

    # URL정보
    #domain: https: // openapi.dbsec.co.kr: 8443

    # Appkey(f), Appsecret(f)
    #appkey: "PS1P3OIOWi3Su7vW9mL1mXpKfy5njebrUFAV"
    #secretkey: "3RnDV1inhKS8FhMQ8nqI0lftUtc9xMYI"
    #token_path: "C:/_resources/golden-cross/config/db-token-real.yaml"  # 토큰 경로(f)



    return


if __name__ == '__main__':
    filename = "C:/_resources/golden-cross/config/db-trading.yaml"

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test start")
    test(filename)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> sample test end")
