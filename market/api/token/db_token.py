import datetime
import logging
import json
import requests
import yaml

################################################################################
# 접근 토큰을 읽는다.
################################################################################
def get_token(domain, appkey, secretkey, save_path):
    try:
        # 토큰이 저장된 파일 읽기
        with open(save_path, encoding='UTF-8') as file:
            infos = yaml.load(file, Loader=yaml.FullLoader)

        expired_date = str(infos["token_expired"])
        current_date = datetime.datetime.today().strftime("%Y%m%d%H%M%S")

        # 저장된 토큰 만료 일자 체크 (만료 일시 > 현재 일시 인경우 보관 토큰 리턴)
        if expired_date > current_date: return infos["access_token"]
        else: return access_token(domain, appkey, secretkey, save_path)
    except Exception as e:
        logging.error(e)
        return access_token(domain, appkey, secretkey, save_path)

################################################################################
# 접근 토큰을 발급 받는다.
################################################################################
def access_token(domain, appkey, secretkey, save_path):
    template = "{0}/oauth2/token?appkey={1}&appsecretkey={2}&grant_type=client_credentials&scope=oob"
    url = template.format(domain, appkey, secretkey)
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }

    res = requests.post(url, headers=headers, verify=False)
    if res.status_code != 200:
        error_message = "Error Code : " + str(res.status_code) + " | " + res.text
        print(error_message)
        return None

    data = json.loads(res.text)
    #print("response code : ", str(res.status_code))
    #print("액세스토큰이 발급되었습니다.[{0}]".format(data["token"]))
    return write_token(save_path, data["access_token"])

################################################################################
# 발급 된 토큰을 저장한다.
################################################################################
def write_token(save_path, token):
    expired_date = datetime.datetime.now() + datetime.timedelta(hours=12)

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(f'access_token: {token}\n')
        f.write(f'token_expired: {expired_date.strftime("%Y%m%d%H%M%S")}\n')

    return token

################################################################################
