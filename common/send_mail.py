import time

import yagmail

from config import Mail_Conf


async def send_test_report(s_time, e_time, runtime, result_list):
    """
    发送邮件
    :param s_time:
    :param e_time:
    :param runtime:
    :param result_list:
    :return:
    """

    # TODO 网易邮箱存在垃圾邮件拦截机制，使发送邮件失败，先使用QQ邮箱，不行自己搭建SMTP服务器
    # jfjyreportsender@foxmail.com jfjy2020 使用QQ邮箱发送报告
    if Mail_Conf["enable"]:
        contents = ['本邮件由系统自动发出无需回复',
                    f'本次测试开始时间：{s_time}，结束时间：{e_time}，共持续{runtime}。',
                    f"本次共执行{sum(result_list)}个用例,其中通过{result_list[0]}个，失败{result_list[1]}个，跳过{result_list[2]}个",
                    f'<a href="{Mail_Conf["report_link"]}">点击查看详细报告</a>',
                    "附件为简报",
                    Mail_Conf['html_file']]
        with yagmail.SMTP(user="jfjytestsender@163.com", password="KEKURWHXLJGLUFPK",
                          host="smtp.163.com", smtp_ssl=True) as yag:
            yag.send(Mail_Conf["send_to"], f'测试报告{time.strftime("%Y-%m-%d")}', contents)
