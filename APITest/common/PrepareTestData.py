import json
import logging
import re

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from APITest.common.TestCase import TestCase
from APITest.common.getToken import _get_token
from APITest.module import ApiTestCaseData, Param
from config import DATABASES

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PrepareTestData:
    """
    获取测试数据数据,
    PrepareTestData(product_name:list, module_name:list, level:list, apipath:list).get_data()
    """

    CaseBase = ApiTestCaseData
    ParamBase = Param

    base_sql = r"""
    SELECT
    p.product_name pname,p.appid appid,m.appid mname ,t.`desc` ,CONCAT(p.`host`,m.module_path,t.apipath) url,
    t.method,t.req_headers,t.req_body,t.status_code,t.exp_res_body
    FROM
    api_testcase_data t
    JOIN module m ON t.module_id = m.id
    JOIN product p ON m.product_id = p.id
    WHERE 1=1
    """

    def __init__(self, product_name=None, module_name=None, level=None, apipath=None):
        """

        :param product_name: 一级模块名
        :param module_name: 二级模块名
        :param level: 用例等级
        :param apipath: 接口路径
        """

        self.product_name = product_name
        self.module_name = module_name
        self.level = level
        self.apipath = apipath
        self._conn = get_session()
        self._update_token()  # token 更新
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
            case["req_headers"] = self._transformation(case["req_headers"])
            case["req_body"] = self._transformation(case["req_body"])
            case["exp_res_body"] = self._transformation(case["exp_res_body"])

        return [TestCase(case_info) for case_info in result]

    @property
    def execute_sql(self):
        """
        最终执行的sql
        :return:
        """
        sql = self.base_sql
        if self.product_name:
            sql += "and p.product_name in ('{}')".format("','".join(self.product_name))
        if self.module_name:
            sql += "and m.appid in ('{}')".format("','".join(self.module_name))
        if self.level:
            sql += "and t.`level` in ('{}')".format("','".join(self.level))
        if self.apipath:
            sql += "and m.apipath in ('{}')".format("','".join(self.apipath))
        sql += "ORDER BY t.`order` DESC"
        return sql

    def _get_base_test_data(self):
        """获取原始数据"""
        res_rows = self._conn.execute(text(self.execute_sql)).fetchall()
        self._conn.close()
        result = [dict(zip(result.keys(), result)) for result in res_rows]
        return result

    def _transformation(self, s):
        """
        将参数中的${param}转化为param表中的对应的值,如果没有对应的值则转化为空字符串
        :param s: str
        :return: 转化后的dict
        """

        def _trans(match):
            key = match.group()[2:-1]
            return self._param.get(key, '""')

        result = re.subn(r"\${(.*?)}", _trans, s)

        return json.loads(result[0])

    def _update_token(self):
        """
        根据参数表中尾部带有_token的字段进行token更新
        :return:
        """
        param_list = self._conn.query(self.ParamBase).filter(self.ParamBase.key.endswith('_token')).all()
        for param in param_list:
            old = param.value
            new = _get_token(param.key[:-6])
            param.value = new
            logger.info(f"{param.key}更新<{old}>为<{new}>")
        self._conn.commit()
        self._conn.close()


def get_session():
    engine = create_engine(DATABASES, encoding="utf-8")
    session_maker = sessionmaker(bind=engine)
    return session_maker()


if __name__ == '__main__':
    p = PrepareTestData().get_data()

    print(p[0].run())
