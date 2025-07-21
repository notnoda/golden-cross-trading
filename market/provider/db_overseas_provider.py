import json
import pandas as pd

from pandas.core.interchange.dataframe_protocol import DataFrame

class DbOverseasProvider:

    def __init__(self, rest, market_code, tick_date):
        self.rest = rest
        self.market_code = market_code
        self.tick_date = tick_date

    # 틱봉을 조회 한다.
    async def chart(self, stock_code, tick_size) -> DataFrame:
        path = "/api/v1/quote/overseas-stock/chart/tick"
        params = json.dumps({
            "In": {
                "InputPwDataIncuYn": "Y",
                "InputOrgAdjPrc": "1",
                "dataCnt": "500",
                "InputHourClsCode": "0",
                "InputCondMrktDivCode": self.market_code,
                "InputIscd1": stock_code,
                "InputDate1": self.tick_date,
                "InputDivXtick": str(tick_size),
            }
        })

        data = await self.rest.post(path, params)
        df = pd.DataFrame(data)
        df.columns = ["hour", "date", "close", "open", "high", "low", "volumns"]
        return df.sort_index(ascending=False)
