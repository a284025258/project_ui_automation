import allure
import requests

from APITest.util.dictUitl import assert_dict_contain


class TestCase:

    def __init__(self, case_info):
        self.info = case_info

    def run(self) -> bool:
        with allure.step("发送请求"):
            res = requests.request(self.info["method"], self.info["url"], headers=self.info["req_headers"],
                                   json=self.info["req_body"], timeout=5)
        with allure.step("断言响应码"):
            assert self.info["status_code"] == res.status_code, '断言响应码'
        with allure.step("断言内容"):
            return assert_dict_contain(self.info["exp_res_body"], res.json())
