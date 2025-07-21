import logging
import json
import requests
import time

# SSL 경고 무시
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class DbRest:

    def __init__(self, domain, token):
        self.domain = domain
        self.token = token

    async def post(self, path, params, name="Out"):
        time.sleep(0.5)

        res = requests.post(
            url=self.get_url(path),
            headers=self.get_header(),
            data=params,
            verify=False
        )

        if res.status_code == 200:
            try:
                data = json.loads(json.dumps(res.json(), ensure_ascii=False, indent=4))
                if data["rsp_cd"] != "00000": logging.info(data["rsp_msg"]);
                return data[name]
            except:
                logging.error(f"post: {res}")
                logging.error(f"path: {path}")
                return None
        else:
            print("Error Code : " + str(res.status_code))
            print(json.dumps(res.text, ensure_ascii=False, indent=4))
            return None

    def get_url(self, path):
        return self.domain + path

    def get_header(self):
        return {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self.token}",
            "cont_yn": "",
            "cont_key": "",
        }
