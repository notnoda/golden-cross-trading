import requests
import json
import trader.utils.other_utils as utils

from trader.kis.api.access_config import AccessConfig

################################################################################
# 실시간(웹소켓) 접속 키를 발급 한다.
################################################################################
def get_approval():
    headers = {
        "Content-Type": "application/json",
        "charset":      "UTF-8",
    }
    params = {
        "grant_type": "client_credentials",
        "appkey":      AccessConfig().app_key(), # 앱키
        "secretkey":   AccessConfig().app_secret(), # 앱 시크릿 키
    }

    res = requests.post(AccessConfig().api_url("/oauth2/Approval"), data=json.dumps(params), headers=headers)  # 토큰 발급
    if res.status_code != 200:  # 토큰 정상 발급
        return None # TODO - 에러 처리

    return utils.get_json_to_object(res.json())

def get_approval_key():
    approval = get_approval()
    return approval.approval_key
