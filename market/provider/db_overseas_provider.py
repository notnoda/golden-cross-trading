import json
import pandas as pd

from pandas.core.interchange.dataframe_protocol import DataFrame

from market.base.provider import Provider
from market.base.rest import Rest

class DbOverseasProvider(Provider):

    def __init__(self, rest: Rest, market_code: str, tick_date: str):
        self.rest = rest
        self.market_code = market_code
        self.tick_date = tick_date

    async def chart(self, stock_code: str, tick_size: int) -> DataFrame:
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
