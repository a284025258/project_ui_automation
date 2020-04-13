import argparse
import os

import pytest

from config import APITESTCASE_HOME, REPORT_XML_DIR, REPORT_HTML_DIR


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--module', dest='module', nargs='*', type=str, help='test area of module.')
    parser.add_argument('-l', '--level', dest='level', nargs='*', type=int,
                        help='test case level will be run.')
    parser.add_argument('-p', '--path', dest='api_path', nargs='*', type=str, help='apipath')
    return parser.parse_args()


global RUN_MODULE
global RUN_LEVEL
global RUN_PATH
RUN_MODULE = setup().module
RUN_LEVEL = setup().level
RUN_PATH = setup().api_path



if __name__ == '__main__':
    pytest.main(["-vv", "-s", APITESTCASE_HOME, "--color=no", f"--alluredir={REPORT_XML_DIR}"])
    os.system(f"allure generate --clean {REPORT_XML_DIR} -o {REPORT_HTML_DIR}")

