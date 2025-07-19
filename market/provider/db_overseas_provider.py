import json
import pandas as pd

from pandas.core.interchange.dataframe_protocol import DataFrame

class DbOverseasProvider:

    def __init__(self, rest, market_code, tick_date):
        self.rest = rest

    # 틱봉을 조회 한다.
    async def chart_tick(self, stock_code, tick_size) -> DataFrame:
        return self.rest.chart_tick(stock_code, tick_size)
