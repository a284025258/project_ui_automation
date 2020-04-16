import datetime
import time

from common.send_mail import send_test_report


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

    send_test_report(begin, end, runtime.strftime("%H:%M:%S"), [passed, failed, skipped])
