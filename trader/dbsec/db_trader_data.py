import asyncio
import trader.analyze.analysis_utils as analysis
import trader.dbsec.api.api_overseas as api
import trader.dbsec.api.access_token as access_token
import trader.dbsec.common.read_config as read_config

################################################################################
# Trading
################################################################################
def trading(filename):
    config = access_token.add_access_token(read_config.read_config(filename))
    df = asyncio.run(api.chart_tick(config, "SOXL", 60))
    df = analysis.add_ichimoku(df)

    #print(df)
    for index, row in df.iterrows():
        print(f"{index}\t{row['date']}\t{row['hour']}\t{row['open']}\t{row['high']}\t{row['low']}\t{row['close']}\t{row['ichimoku_span1']}\t{row['ichimoku_span2']}")


if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    trading("C:/_resources/golden-cross/config/db-trading.yaml")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
