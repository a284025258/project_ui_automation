import argparse
import os

import pytest

from config import APITESTCASE_HOME, REPORT_XML_DIR, REPORT_HTML_DIR


def setup():
    """
    启动脚本设置
    :return:
    """
    parser = argparse.ArgumentParser(description="接口测试启动程序")
    parser.add_argument('-p', '--product', dest='product', nargs='*', type=str, help='执行测试的一级模块名.')
    parser.add_argument('-m', '--module', dest='module', nargs='*', type=str, help='执行测试的模块名.')
    parser.add_argument('-l', '--level', dest='level', nargs='*', choices=[1, 2, 3], type=int,
                        help='执行的用例等级在1 2 3中选择')
    parser.add_argument('-a', '--apipath', dest='api_path', nargs='*', type=str, help='执行的api路径,例如/path/to/api')

    return parser.parse_args()


global RUN_PRODUCT
global RUN_MODULE
global RUN_LEVEL
global RUN_PATH

RUN_PRODUCT = setup().product
RUN_MODULE = setup().module
RUN_LEVEL = setup().level
RUN_PATH = setup().api_path

if __name__ == '__main__':
    pytest.main(["-vv", "-s", APITESTCASE_HOME, "--color=no", f"--alluredir={REPORT_XML_DIR}"])
    os.system(f"allure generate  {REPORT_XML_DIR} -o {REPORT_HTML_DIR} --clean")
