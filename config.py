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

# 数据库配置
DATABASES = 'mysql+pymysql://root:root@10.4.3.142:3306/test?charset=utf8'
