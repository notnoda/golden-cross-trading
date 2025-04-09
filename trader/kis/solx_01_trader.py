from trader.kis.constructors.solx_01_constructor import SolxFirstConstructor

################################################################################
# Trading
################################################################################
def trading(filename):
    constructor = SolxFirstConstructor(filename)

    # 생성
    strategy = constructor.get_strategy_object()

    # 시작
    strategy.start()

    # 대기
    strategy.join()

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    trading("C:/_resources/golden-cross/config/kis-trading-real.yaml")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
