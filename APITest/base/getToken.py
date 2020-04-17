import logging

import requests
from jsonpath import jsonpath
from requests.auth import AuthBase

from APITest.base.badconfexc import BadConfException
from APITest.config import SYS_CONF, ROLE_CONF
from APITest.util.AESUtil import AESUtil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TokenAuth(AuthBase):
    def __init__(self, role_name):
        """
        :param role_name:
        """
        self.role_name = role_name

    def __call__(self, r):
        r.headers['token'] = _get_token(self.role_name)
        return r


def _get_token(role_name):
    """
    获取token
    :param role_name:角色名
    :return:
    """
    if not role_name:
        return ""
    # 通过配置文件中的
    try:
        account = ROLE_CONF[role_name][0]
        password = ROLE_CONF[role_name][1]
        appID = ROLE_CONF[role_name][2]
        host = SYS_CONF[appID]['host']
        key = SYS_CONF[appID]['key']
    except KeyError:
        raise BadConfException(f"请检查配置文件中是否有-->{role_name}")
    authPath = "/sso/static/login"
    token_path = "$.data.token"
    post_data = {"data": {
        "userid": account,
        "appid": appID,
        "password": AESUtil(key).encrypt(password)
    }}

    res = requests.request("POST", host + authPath, json=post_data)
    _token = res.json().copy()
    logger.info("获取到的鉴权接口返回值为:{}".format(_token))

    token = jsonpath(_token, token_path)
    if token:
        logger.info("获取到的token为:{}".format(token[0]))
        return token[0]
    else:
        logger.warning("没有获取到token，返回空字符串")
        return ''
