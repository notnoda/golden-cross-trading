import yaml
import market.api.db_token as db_token
import trader.commons.utils as utils

from dataclasses import dataclass

@dataclass
class Config:
    domain: str
    appkey: str
    secretkey: str
    token: str
    start_date: str
    end_date: str
    tick_date: str

def get_config(filename):
    properties = get_properties(filename)
    secret = get_secret(properties["secret_path"])
    token = db_token.get_token(secret["domain"], secret["appkey"], secret["secretkey"], properties["token_path"])

    start_date = properties["start_date"] if "start_date" in properties else ""
    start_date = utils.get_date() if start_date == "" else start_date

    end_date = properties["end_date"] if "end_date" in properties else ""
    end_date = utils.add_date(1) if end_date == "" else end_date

    tick_date = properties["tick_date"] if "tick_date" in properties else ""
    tick_date = utils.add_date(-1) if tick_date == "" else tick_date

    return Config(
        domain=secret["domain"],
        appkey=secret["appkey"],
        secretkey=secret["secretkey"],
        token=token,
        start_date=start_date,
        end_date=end_date,
        tick_date=tick_date,
    )

def get_properties(filename):
    with open(filename, encoding="UTF-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config

def get_secret(filename):
    with open(filename, encoding="UTF-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> read_config start")
    config = get_config("C:/_resources/golden-cross/config/db-trading.yaml")
    print(config)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> read_config end")
