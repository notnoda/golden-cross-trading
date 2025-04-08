from trader.kis.bak.kis_config import KisTickChart

def dataframe_sample():
    create_dataframe()
    tick_chart = KisTickChart.instance()
    grouped = tick_chart.get_tick_data(1)
    print(grouped)
    #print(grouped)

def create_dataframe():
    tick_chart = KisTickChart.instance()
    tick_chart.add_tick_data('114233', '55000')
    tick_chart.add_tick_data('114234', '55000')
    tick_chart.add_tick_data('114235', '55000')
    tick_chart.add_tick_data('114236', '54950')
    tick_chart.add_tick_data('114238', '55000')
    tick_chart.add_tick_data('114238', '55000')
    tick_chart.add_tick_data('114241', '55000')
    tick_chart.add_tick_data('114242', '55000')
    tick_chart.add_tick_data('114244', '55000')
    tick_chart.add_tick_data('114244', '55000')
    tick_chart.add_tick_data('114245', '55000')
    tick_chart.add_tick_data('114245', '55000')
    tick_chart.add_tick_data('114246', '55000')
    tick_chart.add_tick_data('114246', '55000')
    tick_chart.add_tick_data('114247', '55000')
    tick_chart.add_tick_data('114247', '54900')
    tick_chart.add_tick_data('114249', '55000')
    tick_chart.add_tick_data('114250', '55000')
    tick_chart.add_tick_data('114250', '55000')
    tick_chart.add_tick_data('114252', '54950')
    tick_chart.add_tick_data('114253', '55000')
    tick_chart.add_tick_data('114253', '55000')
    tick_chart.add_tick_data('114254', '54900')
    tick_chart.add_tick_data('114254', '54900')
    tick_chart.add_tick_data('114254', '54900')
    tick_chart.add_tick_data('114255', '54900')
    tick_chart.add_tick_data('114256', '54950')
    tick_chart.add_tick_data('114256', '55000')
    tick_chart.add_tick_data('114256', '54950')
    tick_chart.add_tick_data('114258', '54900')
    tick_chart.add_tick_data('114259', '55000')
    tick_chart.add_tick_data('114300', '54950')
    tick_chart.add_tick_data('114300', '54900')
    tick_chart.add_tick_data('114301', '54900')
    tick_chart.add_tick_data('114301', '55000')
    tick_chart.add_tick_data('114302', '55000')
    tick_chart.add_tick_data('114302', '55000')
    tick_chart.add_tick_data('114302', '55000')
    tick_chart.add_tick_data('114305', '55000')
    tick_chart.add_tick_data('114306', '55000')
    tick_chart.add_tick_data('114307', '54950')
    tick_chart.add_tick_data('114308', '55000')
    tick_chart.add_tick_data('114309', '54950')
    tick_chart.add_tick_data('114310', '55000')
    tick_chart.add_tick_data('114311', '54950')
    tick_chart.add_tick_data('114311', '54900')
    tick_chart.add_tick_data('114311', '54900')
    tick_chart.add_tick_data('114312', '55000')
    tick_chart.add_tick_data('114313', '55000')
    tick_chart.add_tick_data('114313', '55000')
    tick_chart.add_tick_data('114314', '54950')
    tick_chart.add_tick_data('114315', '54900')
    tick_chart.add_tick_data('114315', '55000')
    tick_chart.add_tick_data('114315', '54900')
    tick_chart.add_tick_data('114316', '54900')
    tick_chart.add_tick_data('114317', '54950')
    tick_chart.add_tick_data('114320', '55000')
    tick_chart.add_tick_data('114320', '55000')
    tick_chart.add_tick_data('114320', '54900')
    tick_chart.add_tick_data('114321', '54900')
    tick_chart.add_tick_data('114322', '55000')
    tick_chart.add_tick_data('114324', '54950')
    tick_chart.add_tick_data('114325', '54950')
    tick_chart.add_tick_data('114326', '55000')
    tick_chart.add_tick_data('114326', '55000')
    tick_chart.add_tick_data('114327', '55000')
    tick_chart.add_tick_data('114328', '54950')
    tick_chart.add_tick_data('114329', '55000')
    tick_chart.add_tick_data('114330', '55000')
    tick_chart.add_tick_data('114334', '55000')
    tick_chart.add_tick_data('114334', '55000')
    tick_chart.add_tick_data('114335', '55000')
    tick_chart.add_tick_data('114335', '55000')
    tick_chart.add_tick_data('114336', '54900')
    tick_chart.add_tick_data('114336', '54900')
    tick_chart.add_tick_data('114337', '54900')
    tick_chart.add_tick_data('114339', '55000')
    tick_chart.add_tick_data('114341', '55000')
    tick_chart.add_tick_data('114342', '54900')
    tick_chart.add_tick_data('114342', '54900')
    tick_chart.add_tick_data('114343', '55000')
    tick_chart.add_tick_data('114344', '54900')
    tick_chart.add_tick_data('114345', '54900')
    tick_chart.add_tick_data('114345', '54900')
    tick_chart.add_tick_data('114346', '55000')
    tick_chart.add_tick_data('114347', '54900')
    tick_chart.add_tick_data('114348', '55000')
    tick_chart.add_tick_data('114350', '55000')
    tick_chart.add_tick_data('114350', '55000')
    tick_chart.add_tick_data('114351', '54900')
    tick_chart.add_tick_data('114351', '55000')
    tick_chart.add_tick_data('114352', '54900')
    tick_chart.add_tick_data('114354', '54900')
    tick_chart.add_tick_data('114354', '55000')
    tick_chart.add_tick_data('114354', '55000')
    tick_chart.add_tick_data('114355', '54900')
    tick_chart.add_tick_data('114356', '54900')
    tick_chart.add_tick_data('114357', '55000')
    tick_chart.add_tick_data('114358', '55000')
    tick_chart.add_tick_data('114359', '55000')

def object_to_string():
    send_data = {
        "header": {
            "approval_key": "self.__approval_key",
            "tr_type": "self.__tr_type",
            "custtype": "P",
            "content-type": "utf-8"
        },
        "body": {
            "input": {
                "tr_id": "self.__tr_id",
                "tr_key": "self.__tr_key"
            }
        }
    }

    print(str(send_data))

def sub_data():
    import pandas as pd

    # 예제 DataFrame 생성
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [5, 6, 7, 8],
        "C": [9, 10, 11, 12]
    })

    # 첫 2개의 행 선택
    subset = df.iloc[2:]
    print(df)
    print("=================")
    print(subset)

if __name__ == "__main__":
    #object_to_string()
    #dataframe_sample()
    sub_data()
