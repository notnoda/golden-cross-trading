import json
import logging
import requests

from trader.kis.api.access_config import AccessConfig
from trader.kis.api.response import APIResponse

################################################################################
# API Get 방식 으로  호출 한다.
################################################################################
async def fetch_get(path, tr_id, params):
    headers = __get_headers(tr_id)
    res = requests.get(AccessConfig().api_url(path), params=params, headers=headers)
    return __get_result(res)

################################################################################
# API Post 방식 으로  호출 한다.
################################################################################
async def fetch_post(path, tr_id, params):
    headers = __get_headers(tr_id)
    res = requests.post(AccessConfig().api_url(path), headers=headers, data=json.dumps(params))
    return __get_result(res)

################################################################################
# 헤더 정보를 생성 한다.
################################################################################
def __get_headers(tr_id):
    return {
        "content-type": "application/json",
        "authorization": f"Bearer {AccessConfig().access_token()}",
        "appkey": AccessConfig().app_key(),
        "appsecret": AccessConfig().app_secret(),
        "tr_id": tr_id,
        "custtype": "P",
        #"hashkey": "",
    }

################################################################################
# 호출 결과를 생성 한다.
################################################################################
def __get_result(res):
    if res.status_code == 200:
        api_res = APIResponse(res)
        api_res.print_fail()
        return api_res
    else:
        logging.error("Error Code : " + str(res.status_code) + " | " + res.text)
        return None
