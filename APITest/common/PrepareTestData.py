from sqlalchemy import or_

from APITest.common.TestCase import TestCase
from APITest.common.getSession import session
from APITest.module import ApiTestCaseData, Param


class PrepareTestData:
    """
    获取测试数据数据,PrepareTestData(module_id, level, apipath).get_data()
    """

    CaseBase = ApiTestCaseData
    ParamBase = Param

    def __init__(self, module_id=None, level=None, apipath=None):
        """

        :param module_id:
        :param level:
        :param apipath:
        """

        self.module_id = module_id
        self.level = level
        self.apipath = apipath
        self._conn = session
        # 参数表中的参数全量读取为字典
        self._param = {_parma.key: _parma.value for _parma in self._conn.query(self.ParamBase).all()}

    def get_case_desc(self):
        return [case.desc for case in self.get_data()]

    def get_data(self):
        """
        获取数据，并转化数据格式
        :return:
        """
        return [TestCase(case, self._param) for case in self._get_base_test_data()]

    def _get_base_test_data(self):
        """获取原始数据"""
        query_set = self._conn.query(self.CaseBase)
        query_set = self.filter_data(query_set, self.CaseBase.module_id, self.module_id)
        query_set = self.filter_data(query_set, self.CaseBase.level, self.level)
        query_set = self.filter_data(query_set, self.CaseBase.apipath, self.apipath)
        return query_set.all()

    def filter_data(self, query_set, column, filter_):
        """
        筛选数据
        :param query_set:
        :param column: 列
        :param filter_: 筛选用的值
        :return:
        """
        if filter_:
            if isinstance(filter_, list):
                # 列表格式数据采取OR连接
                query_set = query_set.filter(or_(*[column == fil for fil in filter_]))
            else:
                query_set = query_set.filter(column == filter_)
        return query_set


if __name__ == '__main__':
    p = PrepareTestData().get_data()

    print(p[0].run())
