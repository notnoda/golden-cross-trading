import yaml
import market.api.token.db_token as db_token
import trader.commons.utils as utils

class DbConfig:

    def __init__(self):
        return

    def get(self, filename):
        config = self.get_trading(filename)
        config["token"] = self.get_token(config)

        tick_date = config["tick_date"] if "tick_date" in config else ""
        config["tick_date"] = utils.add_date(-1) if tick_date == "" else tick_date

        return config

    def get_token(self, config):
        return db_token.get_token(config["domain"], config["appkey"], config["secretkey"], config["token_path"])

    def get_trading(self, filename):
        with open(filename, encoding="UTF-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        config.update(self.get_secret(config["secret_path"]))
        return config

    def get_secret(self, filename):
        with open(filename, encoding="UTF-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        return config
