import argparse
import os

import pytest

from config import APITESTCASE_HOME, REPORT_XML_DIR, REPORT_HTML_DIR, REPORT_HTML_FILE, REPORT_LINK


def setup():
    """
    启动脚本设置
    :return:
    """
    parser = argparse.ArgumentParser(description="接口测试启动程序")
    parser.add_argument('mode', help="脚本模式,s:starttest")
    parser.add_argument('-p', '--product', dest='product', nargs='*', type=str, help='执行测试的一级模块名.')
    parser.add_argument('-m', '--module', dest='module', nargs='*', type=str, help='执行测试的模块名.')
    parser.add_argument('-l', '--level', dest='level', nargs='*', choices=["1", "2", "3"], type=str,
                        help='执行的用例等级在1 2 3中选择')
    parser.add_argument('-a', '--apipath', dest='api_path', nargs='*', type=str, help='执行的api路径,例如/path/to/api')

    return parser.parse_args()


# 获取启动配置
RUN_PRODUCT = setup().product
RUN_MODULE = setup().module
RUN_LEVEL = setup().level
RUN_PATH = setup().api_path

if __name__ == '__main__':

    if setup().mode in ["s", "starttest"]:
        pytest.main([
            APITESTCASE_HOME, "-q", "-vv",
            f"--html={REPORT_HTML_FILE}", "--self-contained-html",
            "--color=no", f"--alluredir={REPORT_XML_DIR}", "--clean-alluredir",
            # "--reruns=1", "--reruns-delay=1",
            # "--tests-per-worker", "auto",
            # "--workers","auto"
        ])
        os.system(f"allure serve -h 0.0.0.0 -p 8080 {REPORT_XML_DIR}")
