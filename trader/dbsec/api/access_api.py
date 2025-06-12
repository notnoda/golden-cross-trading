import requests
import json

def get_base_url(config, path):
    return config["domain"] + path

def get_headers(config):
    return {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {config['access_token']}",
        "cont_yn": "",
        "cont_key": "",
    }

async def post(config, path, data):
    return requests.post(
        url=get_base_url(config, path),
        headers=oauth.get_headers(config),
        data=data,
        verify=False
    )


if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    domain = "https://openapi.dbsec.co.kr:8443"
    appkey = "PS1P3OIOWi3Su7vW9mL1mXpKfy5njebrUFAV"
    secretkey = "3RnDV1inhKS8FhMQ8nqI0lftUtc9xMYI"

    #get_access_token(domain, appkey, secretkey)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")
