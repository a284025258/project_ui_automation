import os

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# 放置driver的路径
DRIVER_DIR = os.path.join(STATIC_DIR, 'driver')
# 放置错误截图的路径
IMG_DIR = os.path.join(STATIC_DIR, 'img')
# ChromeDriver的对路径
DRIVER_CHROME = os.path.join(DRIVER_DIR, 'chromedriver.exe')
# 接口测试用例路径
APITESTCASE_HOME = os.path.join(BASE_DIR, 'APITest/testcase.py')
# 界面测试用例路径
UITESTCASE_HOME = os.path.join(BASE_DIR, 'UITest/testcase')
# pytest生成测试xml结果
REPORT_XML_DIR = os.path.join(BASE_DIR, 'report/xml')
# allure生成报告路径
REPORT_HTML_DIR = os.path.join(BASE_DIR, 'report/html')


# 邮件设置
REPORT_HTML_FILE = os.path.join(STATIC_DIR, 'report.html')
REPORT_LINK = "http://10.4.3.142:8080/report/index.html"
Mail_Conf = {
    "enable": False,
    "html_file": REPORT_HTML_FILE,
    "report_link": REPORT_LINK,
    "send_to": ['ymangz@foxmail.com', ]
}


# 数据库配置
DATABASES = 'mysql+pymysql://root:root@10.4.3.142:3306/test?charset=utf8'

# 系统配置
API_SYS_CONF = {
    # appId:{"key":sys_key,"host":ip:port}
    "EXWSP": {"key": "85CCQWE456SXXSD6", "host": "http://10.20.5.176:9020"},
    "EXSEM": {"key": "26955CE335EBB4D8", "host": "http://10.20.5.171:9020"},
    "EXEPM": {"key": "2182BF36BD32ACC9", "host": "http://10.20.5.171:9020"},
    "EXSMS": {"key": "DBCCFDC43E99FE4A", "host": "http://10.4.3.131:8020/EXSMS/service"},
}
# 角色配置
API_ROLE_CONF = {
    # roleName : (account,password,appID)
    "sys_admin": ("superuser1", "Jfkj@123", "EXSMS")
}
