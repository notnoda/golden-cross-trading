import logging
import json
import pandas as pd
import requests
import time
import market.conf.config as conf
from market.rest.db_overseas_rest import DbOverseasRest

if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading start")
    config = conf.get_config("C:/_resources/golden-cross/config/db-trading.yaml")
    rest = DbOverseasRest(config)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>> trading end")

