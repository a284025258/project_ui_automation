import logging

import requests
from jsonpath import jsonpath

from APITest.base.interface.base_api import ABCAuthAPIBase
from APITest.config import SYS_CONF, TimeoutTime
from APITest.util.AESUtil import AESUtil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class JF_EXWSP_4_0AuthApi(ABCAuthAPIBase):
    """
    EXWSP
    EXSMS
    综合考务管理系统4.0鉴权API实现
    """

    path = None
    token_path = "$.data.token"

    def __init__(self, account, password, appid):
        self._res = None
        self.account = account
        self.password = password
        self.appid = appid

    def _send(self):
        if self.appid == "EXWSP":
            return self._send_to_EXWSP()
        elif self.appid == "EXSMS":
            return self._send_to_EXSMS()
        else:
            raise ValueError(f"{self.appid}不支持")

    def _send_to_EXWSP(self):
        self.path = "/sso/static/login"
        data_to_post = {"data": {
            "userid": self.account,
            "appid": self.appid,
            "password": AESUtil(self.key).encrypt(self.password)
        }}
        logger.info(f"url-->{self.host + self.path}")
        logger.info(f"json-->{data_to_post}")
        res = requests.post(self.host + self.path, json=data_to_post, timeout=TimeoutTime)
        return res

    def _send_to_EXSMS(self):
        self.path = "/api/sso/login"
        data_to_post = {"data": {
            "userId": self.account,
            "password": AESUtil(self.key).encrypt(self.password).upper()
        }}
        logger.info(f"url-->{self.host + self.path}")
        logger.info(f"json-->{data_to_post}")
        res = requests.post(self.host + self.path, json=data_to_post, timeout=TimeoutTime)
        return res

    @property
    def res(self):
        if self._res:
            return self._res
        else:
            self._res = self._send()
            return self._res

    @property
    def token(self):
        _token = jsonpath(self.res.json(), self.token_path)
        if _token:
            logger.info("获取到的token为:{}".format(_token[0]))
            return _token[0]
        else:
            logger.warning("没有获取到token，返回空字符串")
            return ""

    @property
    def host(self):
        host = SYS_CONF[self.appid]['host']
        return host

    @property
    def key(self):
        _key = SYS_CONF[self.appid]['key']
        return _key


if __name__ == '__main__':
    print(JF_EXWSP_4_0AuthApi("45", "12345678", "EXWSP").token)
