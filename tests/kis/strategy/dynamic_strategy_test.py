import tests.const.test_data_values as conf
import tests.analyze.analyze_utils_data as adata
import trader.analyze.analysis_utils as analysis

from trader.kis.chart.chart import ApiChart
from trader.kis.strategy.dynamic_strategy import DynamicStrategy
from trader.kis.order.overseas_single_order import OverseasSingleOrder

def get_strategy():
    is_real: bool = True # 실전: True, 모의: False
    config = conf.get_test_config(is_real)

    return (
        DynamicStrategy(
            stock_order=OverseasSingleOrder(
                exchange="",
                order_qty=10
            ),
            storages=[
                ApiChart(
                    code="SOLX",
                    name="SOLX",
                )
            ]
        )
    )

def price_lowest_point(strategy):
    df = adata.get_test_df()
    lowest_point = strategy.price_lowest_point(df["close"])
    print(lowest_point)

def sar_point_data(strategy):
    sar_df = analysis.add_analyze_sar(adata.get_test_df())
    sar_data = strategy.sar_point_data(sar_df["sar_long"])
    print(len(sar_data))
    print(sar_data)

def check_rised_slope(strategy):
    sar_df = analysis.get_analyze_sar(adata.get_test_df())
    sar_data = strategy.check_rised_slope(sar_df)
    print(len(sar_data))
    print(sar_data)

if __name__ == "__main__":
    strategy = get_strategy()
    #price_lowest_point(strategy)
    #sar_point_data(strategy)
    check_rised_slope(strategy)
