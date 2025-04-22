import asyncio
import datetime
import pandas as pd
import requests
import trader.kis.api.overseas_price_quotations as quotations

from abc import abstractmethod

class BaseChart:
    __close_time = "155500"

    @abstractmethod
    def get_stock_code(self): pass

    @abstractmethod
    def get_df(self, tick_size): pass

    @abstractmethod
    def get_last(self): pass

    @abstractmethod
    def get_length(self): pass

    @abstractmethod
    def is_closed(self): pass

    def check_closed(self, last_time): return last_time > self.__close_time

class MinuteChart(BaseChart):
    __last_time = "000000"

    def __init__(self, code, exchange):
        super().__init__()
        self.__exchange = exchange
        self.__code = code

    def get_stock_code(self): return self.__code

    def get_df(self, tick_size):
        charts = asyncio.run(quotations.inquire_time_chart(self.__exchange, self.__code, tick_size))
        self.__last_time = charts[-1]["xhms"]
        data = []

        for item in charts:
            data.append({
                "open":  float(item["open"]),
                "high":  float(item["high"]),
                "low":   float(item["low"]),
                "close": float(item["last"]),
            })

        return pd.DataFrame(data)

    def get_last(self): pass

    def get_length(self): return 1000

    def is_closed(self): return self.check_closed(self.__last_time)

class TickChart(BaseChart):

    def __init__(self, code, storage):
        super().__init__()
        self.__code = code
        self.__storage = storage

    def get_stock_code(self): return self.__code

    def get_df(self, tick_size): return self.__storage.get_tick_data(tick_size)

    def get_last(self): pass

    def get_length(self): return self.__storage.get_order_seq_no()

    def is_closed(self): return self.__storage.is_closed()

class ApiChart(BaseChart):

    __api_url = "http://127.0.0.1:5000/api"

    def __init__(self, code, name):
        super().__init__()
        self.__code = code
        self.__name = name

        next_day = datetime.datetime.now() + datetime.timedelta(days=1)
        self.__CLOSE_TIME = next_day.strftime("%Y%m%d0350")

    def get_stock_code(self): return self.__code

    def get_df(self, tick_size):
        url = f"{self.__api_url}/stock-df/{self.__name}/{tick_size}"
        temp_df = pd.DataFrame(requests.get(url).json())
        df = pd.DataFrame({
            "open": temp_df["first"],
            "high": temp_df["max"],
            "low": temp_df["min"],
            "close": temp_df["last"],
        })

        return df

    def get_last(self):
        url = f"{self.__api_url}/stock-last/{self.__name}"
        return requests.get(url).json()

    def get_length(self):
        url = f"{self.__api_url}/stock-length/{self.__name}"
        return requests.get(url).json()["length"]

    def is_closed(self):
        curr_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
        return curr_time >= self.__CLOSE_TIME
