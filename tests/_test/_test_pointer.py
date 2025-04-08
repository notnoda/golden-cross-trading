import time

from trader.base.base_thread import BaseThread
from trader.kis.stream.tick_chart_storage import TickChartStorage

# -----------------------------------------------------------------------------
# TestTickChart 객체 생성 빌더
# -----------------------------------------------------------------------------
class TestTickChart(BaseThread):

    def __init__(self, tick_main: TickChartStorage, tick_sub: TickChartStorage):
        super().__init__()
        self.__temp_count: int = 0
        self.__tick_main = tick_main
        self.__tick_sub = tick_sub

    def execute(self):
        counter: int = 0

        while counter < 50:
            print('>>>>>>>>>>>>>>>>>>>>')
            print(f'counter = {counter}')
            print(f'tick_main = {self.__tick_main.get_order_no()}')
            print(f'tick_sub = {self.__tick_sub.get_order_no()}')

            counter += 1
            time.sleep(0.5)

# -----------------------------------------------------------------------------
# TestTickChart 객체 생성 빌더
# -----------------------------------------------------------------------------
class TestTickChartBuilder:
    def __init__(self):
        self.tick_main = None
        self.tick_sub = None

    def set_tick_main(self, tick_main):
        self.tick_main = tick_main
        return self

    def set_tick_sub(self, tick_sub):
        self.tick_sub = tick_sub
        return self

    def build(self):
        if not all([self.tick_main, self.tick_sub]):
            raise ValueError("모든 필드를 설정해야 합니다!")
        return TestTickChart(self.tick_main, self.tick_sub)
