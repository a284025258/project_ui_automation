import json
import re

import allure
import requests

from APITest.common.getSession import session


from APITest.module import ApiTestCaseData, Module, Product
from APITest.util.dictUitl import assert_dict_contain


class TestCase:

    def __init__(self, obj: ApiTestCaseData, param_dict):
        self._param = param_dict
        self.id = obj.id
        self.module_id = obj.module_id
        self.desc = obj.desc
        self.level = obj.level
        self.apipath = obj.apipath
        self.order = obj.order
        self.method = obj.method
        self.req_headers = self._transformation(obj.req_headers)
        self.req_body = self._transformation(obj.req_body)
        self.status_code = obj.status_code
        self.exp_res_body = self._transformation(obj.exp_res_body)

    def run(self) -> bool:
        res = requests.request(self.method, self.url, headers=self.req_headers, json=self.req_body, timeout=5)
        with allure.step("断言响应码"):
            assert self.status_code == res.status_code
        with allure.step("断言内容"):
            return assert_dict_contain(self.exp_res_body, res.json())

    def _transformation(self, s):
        """
        将参数中的${param}转化为param表中的对应的值,如果没有对应的值则转化为空字符串
        :param s: str
        :return: 转化后的dict
        """

        def _trans(match):
            key = match.group()[2:-1]
            return self._param.get(key, '""')

        result = re.subn("\${(.*?)}", _trans, s)

        return json.loads(result[0])

    def _module_id_to_url(self, id_):
        module_ = session.query(Module).get(id_)
        uri = module_.module_path
        host = session.query(Product).get( module_.product_id).host

        return host + uri

    @property
    def url(self):
        return self._module_id_to_url(self.module_id) + self.apipath
