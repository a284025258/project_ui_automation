import asyncio
import datetime
import time

import pytest

from APITest.base.PrepareTestData import PrepareTestData
from common.send_mail import send_test_report
from manage import RUN_MODULE, RUN_LEVEL, RUN_PATH, RUN_PRODUCT

ptd = PrepareTestData(RUN_PRODUCT, RUN_MODULE, RUN_LEVEL, RUN_PATH)


@pytest.fixture(params=ptd.get_data(), ids=ptd.get_case_desc())
def ApiData(request):
    return request.param


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    执行完后的钩子函数用于发送邮件报告
    :param terminalreporter:
    :param exitstatus:
    :param config:
    :return:
    """
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(terminalreporter._sessionstarttime))
    end = time.strftime("%Y-%m-%d %H:%M:%S")
    runtime = datetime.datetime.utcfromtimestamp(time.time() - terminalreporter._sessionstarttime)

    asyncio.run(send_test_report(begin, end, runtime.strftime("%H:%M:%S"), [passed, failed, skipped]))
