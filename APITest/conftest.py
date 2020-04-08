import logging
from json import JSONDecodeError

import allure
import pytest
import requests

from APITest.config import SYS_CONF
from APITest.util.AESUtil import AESUtil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture(scope='class')
def token():
    url = SYS_CONF.get("EXWSP").get('host')
    key = SYS_CONF.get("EXWSP").get('key')
    post_data = {"data": {
        "userid": "45",
        "appid": "EXWSP",
        "password": AESUtil(key).encrypt("12345678")
    }}

    return _get_token(url, post_data)


def get_test_data():
    return [{"method": "POST",
             "url": "http://10.4.3.137:8000/jf_exwsp/login/sysLogin",
             "json": {"version": "2.3",
                      "data": {
                          "accountName": "IhO7A59owMc=",
                          "accountPwd": "B5qdcH8gr8rLR2nn8f7llA==",
                          "verifyCode": "09934"},
                      "alias": "jyzy",
                      "token": "",
                      "orgCode": "32011500001"},
             "expect": {"code": "400", "data": None, "message": "系统异常", "result": False, "total": 0,
                        "version": "1.0.0"}}], ["test"]


@pytest.fixture(params=get_test_data()[0], ids=get_test_data()[1])
def ApiData(request):
    return request.param


def _get_token(url, data, token_path=None, method="POST"):
    """
    获取token
    :param url:
    :param data:
    :param token_path:
    :param method:
    :return:
    """
    with allure.step("获取token"):
        if token_path is None:
            token_path = ["data", "token"]
        with allure.step("建立连接"):
            try:
                res = requests.request(method, url, json=data)
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
