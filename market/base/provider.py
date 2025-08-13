from abc import ABC, abstractmethod
from pandas.core.interchange.dataframe_protocol import DataFrame

class Provider(ABC):

    @abstractmethod
    async def chart(self, stock_code, tick_size) -> DataFrame:
        pass
