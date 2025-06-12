import json
import logging
import requests

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
# end of class SingletonMeta

class ApiCaller(metaclass=SingletonMeta):

    def __init__(self, url, config=None):
        self.__api_url = url

    def __get_path(self, path):
        return self.__api_url + path

    async def get(self, path, headers, params):
        res = requests.get(self.__get_path(path), params=params, headers=headers)
        return res

    async def post(self, path, headers, params):
        res = requests.post(self.__get_path(path), headers=headers, data=json.dumps(params))
        return res
