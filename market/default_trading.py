import sys

from market.config.db_config import DbConfig
from market.api.rest.db_rest import DbRest
from market.broker.dummy_broker import DummyBroker
from market.provider.db_overseas_provider import DbOverseasProvider
from market.strategy.dummy_strategy import DummyStrategy
from market.worker.default_worker import DefaultWorker
from market.default_executor import DefaultExecutor

def getWorker(filename):
    config = DbConfig().get(filename)
    rest = DbRest(config["domain"], config["token"])
    broker = DummyBroker(rest, config["market_code"])
    provider = DbOverseasProvider(rest, config["market_code"], config["tick_date"])
    strategy = DummyStrategy(provider, config["stock_long"], config["stock_short"])
    return DefaultWorker(broker, strategy, config["order_qty"])

def execute(worker):
    executor = DefaultExecutor(worker)
    executor.run()
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("\nconfig 파일경로를 입력해 주세요.")
        sys.exit()

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    print(f"config: [{sys.argv[1]}]")
    worker = getWorker(sys.argv[1])
    execute(worker)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
