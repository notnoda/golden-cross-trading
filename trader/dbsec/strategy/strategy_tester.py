import asyncio
import logging

from trader.dbsec.base.base_strategy import BaseStrategy

# -----------------------------------------------------------------------------
# StrategyAverages
# -----------------------------------------------------------------------------
class StrategyAverages(BaseStrategy):
    __DELAY_TIME = 3
    __PROFIT_RATE = 1.04
    __LOSS_RATE = 0.998

    __TICK1 = [10, [5, 20, 30, 60]]
    __TICK2 = [60, [5, 10, 20]]

    def __init__(self, config):
        super().__init__(config)
        self.__config = config
        self.__stock_code = config["stock_long"]
        #self.__stock_code = config["stock_short"]

    def execute(self):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy Start")

        try:
            data = asyncio.run(self.__call_position())
            #data = asyncio.run(self.__put_position())
            print(data)
        except Exception as e:
            print(e)
            logging.error(e)

        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Strategy End")

    ################################################################################
    # 매수 시점을 판단 한다.
    ################################################################################
    async def __call_position(self):
        return await self.buy_stock(self.__stock_code)

    ################################################################################
    # 주식을 매도 한다.
    ################################################################################
    async def __put_position(self):
        await self.sell_stock(self.__stock_code)
        return False

# -----------------------------------------------------------------------------
# end of class StrategyAverages
# -----------------------------------------------------------------------------
