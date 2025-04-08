import logging
from collections import namedtuple

# -----------------------------------------------------------------------------
# - API 호출 응답에 필요한 처리 공통 함수
# -----------------------------------------------------------------------------
class APIResponse:
    def __init__(self, resp):
        self.__res = resp
        self.__res_code = resp.status_code
        self.__header = self.__set_header()
        self.__body = self.__set_body()
        self.__rt_cd = self.__body.rt_cd
        self.__code = self.__body.msg_cd
        self.__message = self.__body.msg1

    def __set_header(self):
        fld = dict()
        for x in self.__res.headers.keys():
            if x.islower(): fld[x] = self.__res.headers.get(x)
        _th_ = namedtuple("header", fld.keys())

        return _th_(**fld)

    def __set_body(self):
        _tb_ = namedtuple("body", self.__res.json().keys())
        return _tb_(**self.__res.json())

    def get_response(self):
        return self.__res

    def get_res_code(self):
        return self.__res_code

    def get_header(self):
        return self.__header

    def get_body(self):
        return self.__body

    def get_body_fvalue(self, fn_value):
        return fn_value(self.__body)

    def get_code(self):
        return self.__code

    def get_message(self):
        return self.__message

    def is_ok(self):
        return self.__rt_cd == "0"

    def print_all(self):
        logging.info("<Header>")
        for x in self.__header._fields:
            logging.info(f"\t-{x}: {getattr(self.get_header(), x)}")
        logging.info("<Body>")
        for x in self.__body._fields:
            logging.info(f"\t-{x}: {getattr(self.__body, x)}")

    def print_fail(self):
        if self.__rt_cd != "0": self.print_all()

    def print_error(self, url):
        logging.info("-------------------------------\nError in response: ", self.__res_code, " url=", url)
        logging.info("rt_cd : ", self.__rt_cd, "/ msg_cd : ",self.__code, "/ msg1 : ",self.__message)
        logging.info("-------------------------------")

# end of class APIResp
