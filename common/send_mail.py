import time

import yagmail

from config import REPORT_HTML_FILE, REPORT_URL, Mail


def send_test_report(s_time, e_time, runtime, result_list):
    """
    发送邮件
    :param s_time:
    :param e_time:
    :param runtime:
    :param result_list:
    :return:
    """
    if Mail:
        contents = ['本邮件由系统自动发出无需回复',
                    f'本次测试开始时间：{s_time}，结束时间：{e_time}，共持续{runtime}。',
                    f"本次共执行{sum(result_list)}个用例,其中通过{result_list[0]}个，失败{result_list[1]}个，跳过{result_list[2]}个",
                    f'<a href="{REPORT_URL}">点击查看详细报告</a>',
                    "附件为简报",
                    REPORT_HTML_FILE]
        with yagmail.SMTP(user="jfjytestsender@163.com", password="KEKURWHXLJGLUFPK",
                          host="smtp.163.com", smtp_ssl=True) as yag:
            yag.send('ymangz@foxmail.com', f'测试报告{time.strftime("%Y-%m-%d")}', contents)
