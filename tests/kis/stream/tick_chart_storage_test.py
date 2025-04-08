from trader.kis.stream.tick_chart_storage import TickChartStorage

################################################################################
# Storage 생성
################################################################################
def get_storage(name: str, length: int = 4000):
    __storage = TickChartStorage(name)

    for i in range(1, length):
        __storage.add_tick_data([
            [f'{str(i).zfill(6)}', i]
        ])

    return __storage

################################################################################
# main 실행
################################################################################
if __name__ == "__main__":
    storage = get_storage("TEST")
    df = storage.get_tick_data(100)
    print("============================================================")
    print(df)
    print(storage.is_enough_count(10, 34))
    print("============================================================")

