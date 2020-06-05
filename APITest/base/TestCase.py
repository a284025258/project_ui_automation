import json
import logging
from json.decoder import JSONDecodeError

import allure
import requests

from APITest.base.authentication import JF_CEMS_4_0_TokenAuth
from APITest.util.dictUitl import assert_dict_contain
from config import TimeoutTime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCase:

    def __init__(self, case_info):
        self.info = case_info

    def run(self) -> bool:
        with allure.step("获取请求"):
            logger.info(f'发送报文为{json.dumps(self.info["req_body"])}')
            res = requests.request(self.info["method"],
                                   self.info["url"],
                                   headers=self.info["req_headers"],
                                   json=self.info["req_body"],
                                   auth=JF_CEMS_4_0_TokenAuth(self.info["role_name"]),
                                   timeout=TimeoutTime)
            try:
                logger.info(f"响应信息{json.dumps(res.json(), ensure_ascii=False)}")
            except JSONDecodeError as exc:
                logger.error("响应json化失败，输出部分原始信息")
                logger.error(res.text[:200])
                raise exc
        with allure.step("断言响应码"):
            logger.info(f"断言响应码{self.info['status_code']}=={res.status_code}")
            assert self.info["status_code"] == res.status_code, \
                f"断言响应码失败{self.info['status_code']}!={res.status_code}"
        with allure.step("断言内容"):
            return assert_dict_contain(self.info["exp_res_body"], res.json())

    def __str__(self):
        return str(self.info)

    __repr__ = __str__
