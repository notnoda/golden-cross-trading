import trader.dbsec.api.access_token as access_token
import trader.dbsec.common.read_config as read_config

from trader.dbsec.strategy.strategy_20250612_01 import StrategyAverages

################################################################################
# Trading
################################################################################
def trading(filename):
    config = preprocessing(filename)
    strategy = StrategyAverages(config)

    # 시작
    strategy.start()

    # 대기
    strategy.join()

def preprocessing(filename):
    config = read_config.read_config(filename)
    return access_token.add_access_token(config)

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    trading("C:/_resources/golden-cross/config/db-trading.yaml")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
