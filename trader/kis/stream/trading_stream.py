import logging
import json
import sys
import time
import asyncio
import traceback
import websockets
import trader.kis.api.oauth as oauth
import trader.kis.stream.stream_indexer as stream

from datetime import datetime
from trader.base.base_thread import BaseThread
from trader.errors.trading_error import TradingOrderCloseError
from trader.kis.api.access_config import AccessConfig
from trader.kis.stream.tick_chart_storage import TickChartStorage
from trader.kis.stream.stream_indexer import BaseStreamIndexer

# -----------------------------------------------------------------------------
# - StockTradingStream
# -----------------------------------------------------------------------------
class StockTradingStream(BaseThread):

    def __init__(self, indexer: BaseStreamIndexer, storages: [str, TickChartStorage]):
        super().__init__()

        # 접속 정보
        self.__ws_url = AccessConfig().ws_url()

        # Stream 위치 정보
        self.__tr_id: str = indexer.get_tr_id()
        self.__array_length: int = indexer.get_length()
        self.__index_time:   int = indexer.get_time()
        self.__index_price:  int = indexer.get_price()

        # 데이터 저장소
        self.__storages: [str, TickChartStorage] = storages

    ###########################################################################
    # 실행 진입점
    ###########################################################################
    def execute(self):
        try:
            logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> run")
            asyncio.run(self.__connect())
        except KeyboardInterrupt:
            logging.error(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> KeyboardInterrupt[Stream] 발생!")
            logging.error(traceback.format_exc())
            sys.exit(-100)
        except Exception:
            logging.error(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Exception[Stream] 발생!")
            logging.error(traceback.format_exc())
            sys.exit(-200)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> StockTradingStream end")

    ###########################################################################
    # 주식 가격 정보를 저장 한다.
    ###########################################################################
    async def __connect(self):
        try:
            logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> connect: {datetime.now()}")
            send_list = self.__get_send_list()
            storages = self.__storages

            async with websockets.connect(self.__ws_url, ping_interval=None) as websocket:
                for send_data in send_list:
                    await websocket.send(send_data)
                    await asyncio.sleep(0.5)
                    logging.info(f"Input Command is :{send_data}")

                while True:
                    data = await websocket.recv()
                    status = data[0]

                    if status == "0":
                        values = data.split("|")[3].split("^")
                        storages[values[0]].add_tick_data(self.__get_data_set(values))
                    elif status != "1":
                         if await self.__is_except_case(data, websocket): break
        except TradingOrderCloseError as e:
            return
        except Exception as e:
            logging.error(f"Exception Raised({datetime.now()}): {e}")
            logging.error('Connect Again!')
            time.sleep(0.1)

            # 웹소켓 다시 시작
            await self.__connect()

    ###########################################################################
    # Websocket 접속 정보를 생성 한다.
    ###########################################################################
    def __get_send_list(self):
        approval_key = oauth.get_approval_key()
        send_list = []

        for key in self.__storages.keys():
            send_list.append('{"header":{"approval_key": "%s","custtype":"P","tr_type":"1","content-type":"utf-8"},"body":{"input":{"tr_id":"%s","tr_key":"%s"}}}' % (approval_key, self.__tr_id, key))

        return send_list

    ###########################################################################
    # Websocket 데이터 중 필요 정보를 추출 한다.
    ###########################################################################
    def __get_data_set(self, values):
        index = 0
        count = len(values)

        stock_info = []
        while count > index:
            stock_info.append([values[index + self.__index_time], values[index + self.__index_price]])
            index += self.__array_length

        return stock_info

    ###########################################################################
    # Websocket 데이터 중 예외인 경우 처리 한다.
    ###########################################################################
    async def __is_except_case(self, data, websocket) -> bool:
        json_object = json.loads(data)

        if json_object["header"]["tr_id"] == "PINGPONG":
            await websocket.pong(data)
        else:
            rt_header = json_object["header"]
            rt_tr_key = rt_header["tr_key"]

            rt_body = json_object["body"]
            rt_cd = rt_body["rt_cd"]
            rt_msg1 = rt_body["msg1"]

            if rt_cd == '0':  # 정상일 경우 처리
                rt_tr_id = rt_header["tr_id"]
                rt_key = rt_body["output"]["key"]
                rt_iv = rt_body["output"]["iv"]

                logging.info(f"### RETURN CODE [ {rt_tr_key} ][ {rt_cd} ] MSG [ {rt_msg1} ]")
                logging.info(f"### TR ID [{rt_tr_id}] KEY[{rt_key}] IV[{rt_iv}]")
            else:  # 에러일 경우 처리
                if json_object["body"]["msg1"] != 'ALREADY IN SUBSCRIBE':
                    logging.info(f"### ERROR RETURN CODE [ {rt_tr_key} ][ {rt_cd} ] MSG [ {rt_msg1} ]")
                return True

        time.sleep(1)
        return False

# end of class StockTradingStream

# -----------------------------------------------------------------------------
# StockTradingStreamBuilder 객체 생성 빌더
# -----------------------------------------------------------------------------
class StockTradingStreamBuilder:
    def __init__(self):
        self.tr_id = None
        self.storages = None

    def set_tr_id(self, tr_id):
        self.tr_id = tr_id
        return self

    def set_storages(self, storages):
        self.storages = storages
        return self

    def build(self):
        if not all([self.tr_id, self.storages]): raise ValueError("모든 필드를 설정 해야 합니다!")
        return StockTradingStream(stream.get_stream_indexer(self.tr_id), self.storages)

# end of class StockTradingStreamBuilder
