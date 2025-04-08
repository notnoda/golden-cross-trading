import yaml
import trader.utils.logging_utils as logger

from trader.kis.api.access_config import AccessConfig

# ------------------------------------------------------------------------------
# - BaseConstructor
# ------------------------------------------------------------------------------
class BaseConstructor:

    def __init__(self, filename: str):
        with open(filename, encoding="UTF-8") as f:
            self.__config = yaml.load(f, Loader=yaml.FullLoader)

        AccessConfig(self.__config)
        logger.file_logger(self.__config["log_path"])

    def get_config(self): return self.__config

# end of class BaseConstructor
