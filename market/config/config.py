import yaml
import trader.commons.utils as utils

def get_config(filename):
    config = get_properties(filename)
    #config["token"] = db_token.get_token(config["domain"], config["appkey"], config["secretkey"], config["token_path"])

    start_date = config["start_date"] if "start_date" in config else ""
    config["start_date"] = utils.get_date() if start_date == "" else start_date

    end_date = config["end_date"] if "end_date" in config else ""
    config["end_date"] = utils.add_date(1) if end_date == "" else end_date

    tick_date = config["tick_date"] if "tick_date" in config else ""
    config["tick_date"] = utils.add_date(-1) if tick_date == "" else tick_date

    return config

def get_properties(filename):
    with open(filename, encoding="UTF-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config.update(get_secret(config["secret_path"]))
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
