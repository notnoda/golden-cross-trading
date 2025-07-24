import yaml

class BaseConfig:

    def get_config(self, filename, secret_key):
        config = self.get_trading(filename, secret_key)
        return config

    def get_trading(self, filename, secret_key):
        with open(filename, encoding="UTF-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        config.update(self.get_secret(config[secret_key]))
        return config

    def get_secret(self, filename):
        with open(filename, encoding="UTF-8") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        return config
