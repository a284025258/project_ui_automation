import logging

import allure
import requests

from APITest.util.dictUitl import assert_dict_contain

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCase:

    def __init__(self, case_info):
        self.info = case_info

    def run(self) -> bool:
        with allure.step("发送请求"):
            res = requests.request(self.info["method"], self.info["url"], headers=self.info["req_headers"],
                                   json=self.info["req_body"], timeout=5)
            logger.info(f"{res.json()}")
        with allure.step("断言响应码"):
            logger.info(f"断言响应码{self.info['status_code']}=={res.status_code}")
            assert self.info["status_code"] == res.status_code, '断言响应码'
        with allure.step("断言内容"):
            return assert_dict_contain(self.info["exp_res_body"], res.json())

    def __str__(self):
        return str(self.info)

    __repr__ = __str__
