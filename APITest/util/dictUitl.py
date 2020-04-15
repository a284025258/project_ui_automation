"""
字典工具，用于将字典转换为路径字典的形式，例如：

{"data":{"deep":["deepData1","deepData2"]}}
输出会以空列表、空字典、字符串、数字、None、bool为停止节点
(['data', 'deep', 0],"deepData1")
(['data', 'deep', 1],"deepData2")
"""
import logging

import allure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def assert_dict_contain(dict1, dict2):
    """
    判断前面的字典是否被后面字典包含，
    :param dict1: 字典
    :param dict2: 字典
    :return: bool
    """
    with allure.step("判断>{} 是否被>{} 包含".format(dict1, dict2)):
        if dict1 == {} and dict2 != {}:
            logger.info("空字典设置默认为错误")
            assert False
        return _dict_in(dict1, dict2)


def _traverse(_obj, path=None):
    """
    递归输出嵌套的列表和字典的值
    参考:https://cloud.tencent.com/developer/ask/144215
    :param _obj: 字典或者列表
    :param path: 路径
    :return:
    """
    if not path:
        path = []
    if isinstance(_obj, dict):
        if not _obj:
            yield path, {}
        for x in _obj.keys():
            local_path = path[:]
            local_path.append(x)
            for node in _traverse(_obj[x], local_path):
                yield node
    elif isinstance(_obj, list):
        if not _obj:
            yield path, []
        for x in range(len(_obj)):
            local_path = path[:]
            local_path.append(x)
            for node in _traverse(_obj[x], local_path):
                yield node
    else:
        yield path, _obj


def _dict_in(dict1, dict2):
    """
    判断前面的字典是否被在后面的字典包含
    :param dict1:
    :param dict2:
    :return:
    """
    for i, j in _traverse(dict1):
        with allure.step("断言数据存在路径>{},对应的值为:>{}".format(i, j)):
            assert_obj = dict2.copy()
            for path in i:
                try:
                    assert_obj = assert_obj[path]
                except (IndexError, KeyError):
                    logger.info(f"不存在{i}")
                    assert False

            assert j == assert_obj
