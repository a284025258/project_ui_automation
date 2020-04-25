import os

import pytest
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from UITest.config import Start_Url
from UITest.pages.LoginPage import LoginPage


@pytest.fixture(scope='session')
def loginPage(browser):
    browser.get(Start_Url)
    loginPage = LoginPage(browser)
    return loginPage


@pytest.fixture(scope='session')
def browser():
    options = ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--disable-infobars')
    browser = Chrome(chrome_options=options)
    yield browser
    browser.quit()


@pytest.fixture(params=[{"username": "", "password": "", "check_text": "请输入用户名"},
                        {"username": "45", "password": "", "check_text": "请输入密码"},
                        {"username": "45", "password": "12345678", "check_text": "请输入验证码"},
                        {"username": "45", "password": "12345678", "check_text": "验证码错误或已过期"},
                        {"username": "0000000", "password": "0000000", "check_text": "账号不存在或密码无效"},
                        ], ids=["不填写账户名，密码和验证码",
                                "只填写账户名",
                                "只填写账户名密码",
                                "填写错误验证码",
                                "不存在账号"])
def login_data(request):
    return request.param

# todo 待完善
driver = None


#  module confest
# 初始化用例
@pytest.fixture(scope='module', autouse=False)
def Sys_user_manage_page():
    global driver
    if driver is None:
        driver = Sys_user_manage('Chrome')
        driver.login('superadmin', '123456')
    yield driver
    print('结束用例')
    driver.close_Browser()
    driver = None


# confest.py中定义截图函数
def _fail_picture():
    driver.fail_picture()


# 编写钩子函数
# 失败用例自动截图函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    hook pytest失败
    :param item:
    :param call:
    :return:
    '''
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        _fail_picture()  # 调用截图函数

