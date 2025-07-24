import commons.utils as utils
import market.api.token.db_token as db_token

from market.config.config import BaseConfig

class DbConfig(BaseConfig):

    def get(self, filename):
        config = self.get_config(filename, "secret_path")
        config["token"] = self.get_token(config)

        tick_date = config["tick_date"] if "tick_date" in config else ""
        config["tick_date"] = utils.add_date(-1) if tick_date == "" else tick_date

        return config

    def get_token(self, config):
        domain = config["domain"]
        appkey = config["appkey"]
        secretkey = config["secretkey"]
        token_path = config["token_path"]
        return db_token.get_token(domain, appkey, secretkey, token_path)
