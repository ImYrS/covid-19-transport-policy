"""
    @Author: ImYrS Yang
    @Date: 2022/5/24
    @Copyright: ImYrS Yang
    @Description: 
"""

import os
from typing import Optional
from json import dumps

import requests

from modules import common

os.environ['NO_PROXY'] = '*'


class Policy:
    def __init__(self):
        self.app_id = 'NcApplication'
        self.token = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
        self.nonce = '123456789abcdefg'
        self.paas_id = 'zdww'
        self.wif_nonce = 'QkjjtiLM2dCratiA'
        self.wif_paas_id = 'smt-application'
        self.t = str(common.timestamp(ms=False))
        self.param_sign = common.hash256(self.t + self.token + self.nonce + self.t).upper()
        self.header_sign = common.hash256(self.t + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvC' + self.wif_nonce + self.t).upper()
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'bmfw.www.gov.cn',
            'Origin': 'http://www.gov.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-wif-nonce': self.wif_nonce,
            'x-wif-paasid': self.wif_paas_id,
            'x-wif-signature': self.header_sign,
            'x-wif-timestamp': self.t,
        }

    def do(self, params: dict, key: Optional[str] = '6C3C60DC1BF54982A54D5A8CB4D1817D') -> Optional[list]:
        """发起请求"""
        json = {
            **{
                'appId': self.app_id,
                'key': key,
                'nonceHeader': self.nonce,
                'paasHeader': self.paas_id,
                'signatureHeader': self.param_sign,
                'timestampHeader': self.t,
            },
            **params
        }

        r = requests.post('https://bmfw.www.gov.cn/bjww/interface/interfaceJson', json=json, headers=self.headers)

        return None if r.status_code != 200 else r.json()['data']

    def city_list(self):
        """获取城市列表"""
        return self.do({'flag': '11'}, key='cd4faa2f4c0bdeb4cfd6093769f36482')

    def city(self, code: str):
        """获取城市数据"""
        return self.do({'code': code}, key='6C3C60DC1BF54982A54D5A8CB4D1817D')

    def city_contact(self, code: str):
        return self.do({'code': code}, key='DBA46CF0828D4730AAE4B855FBE417CD')


if __name__ == '__main__':
    print(dumps(Policy().city('440100'), ensure_ascii=False, indent=4, sort_keys=True))
