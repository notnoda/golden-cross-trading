import yaml
import trader.commons.utils as utils

def read_config(filename):
    with open(filename, encoding="UTF-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    start_date = config["start_date"] if "start_date" in config else ""
    config["srtDt"] = utils.get_date() if start_date == "" else start_date

    end_date = config["end_date"] if "end_date" in config else ""
    config["endDt"] = utils.add_date(1) if end_date == "" else end_date

    tick_date = config["tick_date"] if "tick_date" in config else ""
    config["tickDt"] = utils.add_date(-1) if tick_date == "" else tick_date

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
