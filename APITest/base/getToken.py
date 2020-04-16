import logging
from json import JSONDecodeError

import allure
import requests
from jsonpath import jsonpath

from APITest.config import SYS_CONF, ROLE_CONF
from APITest.util.AESUtil import AESUtil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_token(role_name):
    """
    获取token
    :param role_name:角色名
    :return:
    """
    account = ROLE_CONF[role_name][0]
    password = ROLE_CONF[role_name][1]
    appID = ROLE_CONF[role_name][2]
    host = SYS_CONF[appID]['host']
    key = SYS_CONF[appID]['key']
    authPath = "/sso/static/login"
    token_path = "$.data.token"
    post_data = {"data": {
        "userid": account,
        "appid": appID,
        "password": AESUtil(key).encrypt(password)
    }}
    with allure.step("获取token"):
        with allure.step("建立连接"):
            try:
                res = requests.request("POST", host + authPath, json=post_data)
            except ConnectionError as exc:
                logger.error(exc)
                raise exc
        with allure.step("json转换"):
            try:
                _token = res.json().copy()
            except JSONDecodeError as exc:
                logger.error(exc)
                raise exc
        token = jsonpath(_token, token_path)
        if token:
            logger.info("获取到的token为:{}".format(token[0]))
            return f'"{token[0]}"'
        else:
            logger.warning("没有获取到token，返回空字符串")
            return '""'
