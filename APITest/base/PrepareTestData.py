import json
import logging
import re

from sqlalchemy import or_

from APITest.base.TestCase import TestCase
from APITest.util.get_session import get_session
from APITest.config import SYS_CONF
from APITest.module import ApiTestCaseData, Param, Module, Product

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _prepare_url(app_id, url):
    return SYS_CONF[app_id]['host'] + url


class PrepareTestData:
    """
    获取测试数据数据,
    PrepareTestData(product_name, module_name, level, apipath).get_data()
    """

    CaseBase = ApiTestCaseData
    ParamBase = Param

    def __init__(self, product_name=None, module_name=None, level=None, apipath=None):
        """

        :param product_name: 一级模块名
        :param module_name: 二级模块名
        :param level: 用例等级
        :param apipath: 接口路径
        """

        self.product_name = product_name or []
        self.module_name = module_name or []
        self.level = level or []
        self.apipath = apipath or []
        self._conn = get_session()
        # 参数表中的参数全量读取为字典
        self._param = self.get_param()

    def get_param(self):
        """
        获取参数表中的数据
        :return:
        """

        query_set = self._conn.query(self.ParamBase).all()
        self._conn.close()
        data = {_parma.key: _parma.value for _parma in query_set}
        logger.info(f'参数表中数据为{data}')
        return data

    def get_case_desc(self):
        """
        获取用例描述
        :return:
        """
        return [case['desc'] for case in self._get_base_test_data()]

    def get_data(self):
        """
        获取数据，并转化数据格式
        :return:
        """
        result = self._get_base_test_data()
        for case in result:
            case["req_body"] = self._transformation(case["req_body"])
            case["exp_res_body"] = self._transformation(case["exp_res_body"])
            case["url"] = _prepare_url(case["appid"], case["url"])
        return [TestCase(case_info) for case_info in result]

    def _get_base_test_data(self):
        """获取原始数据"""
        sql = self._conn.query(Product.product_name.label("pname"), Product.appid, Module.appid.label("mname"),
                               ApiTestCaseData.role_name, ApiTestCaseData.desc,
                               (Module.module_path + ApiTestCaseData.apipath).label("url"),
                               ApiTestCaseData.method,
                               ApiTestCaseData.req_headers, ApiTestCaseData.req_body, ApiTestCaseData.status_code,
                               ApiTestCaseData.exp_res_body, ApiTestCaseData.enable) \
            .join(Module, ApiTestCaseData.module_id == Module.id) \
            .join(Product, Module.product_id == Product.id) \
            .filter(or_(*[Product.product_name == p_name for p_name in self.product_name])) \
            .filter(or_(*[Module.appid == m_name for m_name in self.module_name])) \
            .filter(or_(*[ApiTestCaseData.level == level for level in self.level])) \
            .filter(or_(*[ApiTestCaseData.apipath == apipath for apipath in self.apipath])) \
            .order_by(ApiTestCaseData.order.desc())
        _results = sql.all()
        self._conn.close()
        columns = [
            'pname', 'appid', 'mname', 'role_name',
            'desc', 'url', 'method', 'req_headers',
            'req_body', 'status_code', 'exp_res_body', 'enable'
        ]

        results = [i or "" for i in [_result for _result in _results]]
        dict_results = [dict(zip(columns, result)) for result in results]
        return dict_results

    def _transformation(self, s):
        """
        将参数中的${param}转化为param表中的对应的值,如果没有对应的值则转化为空字符串
        :param s: str
        :return: 转化后的dict
        """
        if s is None:
            s = "{}"

        def _trans(match):
            key = match.group()[2:-1]
            return self._param.get(key, '""')

        result = re.subn(r"\${(.*?)}", _trans, s)

        return json.loads(result[0])


if __name__ == '__main__':
    p = PrepareTestData().get_data()

    print(p[0].run())
