import logging
import pandas as pd

from datetime import datetime
from trader.errors.trading_error import TradingOrderCloseError

# -----------------------------------------------------------------------------
# - Tick Chart Data
# -----------------------------------------------------------------------------
class TickChartStorage:
    __order_seq_no = 0
    __trading_time = "000000"
    __next_step = ""

    def __init__(self, name: str, close_time: str = "155500"):
        self.__name = name
        self.__close_time = close_time
        self.__tick_df = pd.DataFrame([{
            "order_no": pd.Series(dtype="int"),
            "trading_time": pd.Series(dtype="str"),
            "stock_price": pd.Series(dtype="float"),
        }])

    ###########################################################################
    # 매매 정보를 생성할 틱의 최소 갯수 여부를 판단 한다.
    ###########################################################################
    def is_enough_count(self, tick_count: int, min_tick: int = 34):
        # 틱 갯수 확인
        min_count = tick_count * min_tick
        return self.__order_seq_no >= min_count

    ###########################################################################
    # 주문 순번(틱 생성 갯수)을 반환 한다.
    ###########################################################################
    def get_order_seq_no(self): return self.__order_seq_no

    ###########################################################################
    # 다음 단계 실행 여부를 확인 한다.
    ###########################################################################
    def get_next_step(self): return self.__next_step
    def set_next_step(self, next_step: str): self.__next_step = next_step

    ###########################################################################
    # 매매 중단 여부를 확인 한다.
    ###########################################################################
    def is_closed(self):
        return self.__trading_time >= self.__close_time

    ###########################################################################
    # 주문 정보를 저장 한다.
    ###########################################################################
    def add_tick_data(self, trading_data):
        for trading_time, stock_price in trading_data:
            self.__tick_df.loc[self.__order_seq_no] = {
                "order_no": self.__order_seq_no + 1,
                "trading_time": trading_time,
                "stock_price": float(stock_price),
            }

            if self.__order_seq_no % 300 == 0:
                self.__trading_time = trading_time
                print(f"tick storage [{datetime.now()}] - [{self.__name}] [{self.__order_seq_no}] [{trading_time}] [{stock_price}]")
                if self.is_closed(): raise TradingOrderCloseError()

            self.__order_seq_no += 1

    ###########################################################################
    # 틱 정보를 생성 하여 반환 한다.
    ###########################################################################
    def get_tick_data(self, tick_count: int):
        max_no = self.__order_seq_no
        std_no = max_no // tick_count

        work_df = self.__tick_df.copy()
        work_df["group_no"] = std_no - ((max_no - work_df["order_no"]) // tick_count)
        work_df["seq_no"] = tick_count - (max_no - work_df["order_no"]) % tick_count

        df = work_df.groupby(["group_no"]).agg({
            "stock_price": ["first", "max", "min", "last"]
        })["stock_price"]

        df.columns = ["open", "high", "low", "close"]

        return df

# end of class TickChartStorage
