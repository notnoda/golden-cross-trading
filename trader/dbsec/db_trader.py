import logging
import sys
import trader.utils.logging_utils as logger
import trader.dbsec.api.access_token as access_token
import trader.dbsec.common.read_config as read_config

from trader.dbsec.strategy.strategy_20250701_01 import TradingStrategy

################################################################################
# Trading
################################################################################
def trading(filename):
    config = preprocessing(filename)
    strategy = TradingStrategy(config)

    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    strategy.start() # 시작
    strategy.join() # 대기
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading finish")

def preprocessing(filename):
    config = read_config.read_config(filename)
    logger.file_logger(config["log_path"])
    return access_token.add_access_token(config)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\nconfig 파일경로를 입력해 주세요.")
        sys.exit()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    print(f"config: [{sys.argv[1]}]")
    trading(sys.argv[1])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
