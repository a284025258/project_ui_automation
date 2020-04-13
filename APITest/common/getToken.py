import logging
from json import JSONDecodeError

import allure
import requests

from APITest.config import SYS_CONF, ROLE_CONF
from APITest.util.AESUtil import AESUtil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_token(roleName):
    """
    获取token
    :param roleName:角色名
    :return:
    """
    account = ROLE_CONF[roleName][0]
    password = ROLE_CONF[roleName][1]
    appID = ROLE_CONF[roleName][2]
    host = SYS_CONF[appID]['host']
    key = SYS_CONF[appID]['key']
    authPath = "/sso/static/login"
    token_path = ["data", "token"]
    post_data = {"data": {
        "userid": account,
        "appid": appID,
        "password": AESUtil(key).encrypt(password)
    }}
    with allure.step("获取token"):
        with allure.step("建立连接"):
            try:
                res = requests.request("POST", host+authPath, json=post_data)
            except ConnectionError as exc:
                logger.error(exc)
                raise exc
        with allure.step("json转换"):
            try:
                _token = res.json().copy()
            except JSONDecodeError as exc:
                logger.error(exc)
                raise exc
        for path in token_path:
            _token = _token.get(path, {})
        if _token == {}:
            logger.warning("没有获取到token，返回空字符串")
        else:
            logger.info("获取到的token为:{}".format(_token))
        token = _token if _token != {} else ""

        return token
