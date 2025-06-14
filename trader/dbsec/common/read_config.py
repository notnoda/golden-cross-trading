import yaml
from datetime import datetime

def read_config(filename):
    with open(filename, encoding="UTF-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config["today"] = "20250613" #TODO - datetime.now().strftime("%Y%m%d")
    return add_secret(config)

def add_secret(config):
    with open(config["secret_path"], encoding="UTF-8") as f:
        config_secret = yaml.load(f, Loader=yaml.FullLoader)

    config["domain"] = config_secret["domain"]
    config["appkey"] = config_secret["appkey"]
    config["secretkey"] = config_secret["secretkey"]
    config["token_path"] = config_secret["token_path"]
    config["account_no"] = config_secret["account_no"]
    config["product_no"] = config_secret["product_no"]
    return config

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> read_config start")
    config = read_config("C:/_resources/golden-cross/config/db-trading.yaml")
    print(config)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> read_config end")
