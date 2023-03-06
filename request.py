import requests
import config
import json


# 网络请求类
class Request:
    url = config.Conf.get_config("config", "url")
    header={"Content-Type": "application/json"}

    def __init__(self):
        pass

    def get(self, param=''):
        res = requests.get(url=self.url + param,headers=self.header)
        if res.status_code == 200:
            d = json.loads(res.text)
            return d
        else:
            print("[GET]接口请求失败")
            exit(0)
            return {}

    def post(self, api, data=None):
        if data is None:
            data = {}
        res = requests.post(url=self.url + api,headers=self.header,json=data)
        if res.status_code == 200:
            d = json.loads(res.text)
            return d
        else:
            print("[POST]接口请求失败")
            exit(0)
            return {}

    def set_header(self,key,value):
        self.header[key] = value