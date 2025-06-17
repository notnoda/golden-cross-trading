import asyncio

import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.access_token as access_token
import trader.dbsec.api.api_overseas as api
import trader.dbsec.common.read_config as read_config

################################################################################
# Trading
################################################################################
def trading(filename):
    config = preprocessing(filename)

    df = asyncio.run(api.chart_tick(config, config["stock_long"], "100"))
    df = analysis.add_moving_average_ema(df, 5)
    print(type(df))
    print(df)

    #constructor = SolxFirstConstructor(filename)

    # 생성
    #strategy = constructor.get_strategy_object()

    # 시작
    #strategy.start()

    # 대기
    #strategy.join()

def preprocessing(filename):
    config = read_config.read_config(filename)
    return access_token.add_access_token(config)

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    trading("C:/_resources/golden-cross/config/db-trading.yaml")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
