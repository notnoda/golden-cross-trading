
class RestProvider:

    def __init__(self, config):
        self.__config = config
        return

    async def call(self, stock_code, tick_count):
        df = await api.chart_tick(self.__config, stock_code, tick_size)
        return
