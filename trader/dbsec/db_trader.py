import logging
import trader.utils.logging_utils as logger
import trader.dbsec.api.access_token as access_token
import trader.dbsec.common.read_config as read_config

from trader.dbsec.strategy.strategy_20250612_01 import StrategyAverages

################################################################################
# Trading
################################################################################
def trading(filename):
    config = preprocessing(filename)
    strategy = StrategyAverages(config)

    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    strategy.start() # 시작
    strategy.join() # 대기
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading finish")

def preprocessing(filename):
    config = read_config.read_config(filename)
    logger.file_logger(config["log_path"])
    return access_token.add_access_token(config)

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    trading("C:/_resources/golden-cross/config/db-trading.yaml")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
