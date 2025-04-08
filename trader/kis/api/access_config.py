import json
import logging

import requests
import yaml
import trader.kis.api.access_urls as urls

from datetime import datetime

# -----------------------------------------------------------------------------
# - SingletonMeta
# -----------------------------------------------------------------------------
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
# end of class SingletonMeta

# -----------------------------------------------------------------------------
# - AccessConfig
# -----------------------------------------------------------------------------
class AccessConfig(metaclass=SingletonMeta):
    __access_token: str = None
    __expired: str = None

    def __init__(self, config=None):
        access_urls = urls.get_urls(config["mode"])

        # 접속 정보
        self.__api_url = access_urls.get_api_url()
        self.__ws_url  = access_urls.get_ws_url()
        self.__app_key = config["app_key"]    # 앱키
        self.__app_secret = config["app_secret"] # 앱 시크릿 키

        # 계좌 정보
        self.__account_no = config["account_no"] # 계좌 번호
        self.__product_no = config["product_no"] # 상품 번호

        # 토큰 저장 정보
        self.__save_path = config["token_path"]
        self.__access_token, self.__expired_date = read_token(self.__save_path, self.__api_url, self.__app_key, self.__app_secret)

    def api_url(self, path): return f"{self.__api_url}{path}"
    def ws_url(self):     return self.__ws_url
    def app_key(self):    return self.__app_key
    def app_secret(self): return self.__app_secret

    def account_no(self): return self.__account_no
    def product_no(self): return self.__product_no

    def access_token(self):
        if self.__expired_date > datetime.today(): return self.__access_token
        else: return issue_token(self.__save_path, self.__api_url, self.__app_key, self.__app_secret)[1]
# end of class AccessConfig

################################################################################
# AccessConfig - config 파일을 읽어 생성 한다.
################################################################################
def instance_access_file(filename):
    with open(filename, encoding="UTF-8") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return AccessConfig(config)

################################################################################
# 접근 토큰을 읽는다.
################################################################################
def read_token(save_path, api_url, app_key, app_secret):
    try:
        # 토큰이 저장된 파일 읽기
        with open(save_path, encoding='UTF-8') as file:
            token_infos = yaml.load(file, Loader=yaml.FullLoader)

        expired_date = token_infos['token_expired']

        # 저장된 토큰 만료 일자 체크 (만료 일시 > 현재 일시 인경우 보관 토큰 리턴)
        if expired_date > datetime.today(): return token_infos["access_token"], expired_date
        else: return issue_token(save_path, api_url, app_key, app_secret)
    except Exception as e:
        logging.error(e)
        return issue_token(save_path, api_url, app_key, app_secret)

################################################################################
# 접근 토큰을 발급 한다.
################################################################################
def issue_token(save_path, api_url, app_key, app_secret):
    access_token, token_expired = get_token(api_url=api_url, app_key=app_key, app_secret=app_secret)
    expired_date = datetime.strptime(token_expired, '%Y-%m-%d %H:%M:%S')

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(f'access_token: {access_token}\n')
        f.write(f'token_expired: {token_expired}\n')

    return access_token, expired_date

################################################################################
# 접근 토큰을 조회 한다.
################################################################################
def get_token(app_key, app_secret, api_url):
    params = {
        "grant_type": "client_credentials",
        "appkey":     app_key,
        "appsecret":  app_secret,
    }

    res = requests.post(f"{api_url}/oauth2/tokenP", data=json.dumps(params))  # 토큰 발급
    if res.status_code != 200:  # 토큰 정상 발급
        return None # TODO - 에러 처리

    import trader.utils.other_utils as utils
    data = utils.get_json_to_object(res.json())
    return data.access_token, data.access_token_token_expired
