import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from UITest.config import Start_Url, Driver_Path
from UITest.pages.BasePage import BasePage
from UITest.pages.LoginPage import LoginPage

page = None


@pytest.fixture(scope='session')
def login_page(base_page):
    login_page = LoginPage(base_page)
    login_page.driver.get(Start_Url)
    return login_page


@pytest.fixture(scope='session')
def base_page():
    global page
    if page is None:
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        with Chrome(Driver_Path, chrome_options=options) as browser:
            page = BasePage(browser)
            yield page


@pytest.fixture(params=[
    {"username": "45", "password": "", "check_text": "请输入密码"},
    {"username": "45", "password": "12345678", "check_text": "请输入验证码"},
    {"username": "45", "password": "12345678", "check_text": "验证码错误或已过期"},
    {"username": "0000000", "password": "0000000", "check_text": "账号不存在或密码无效"},
], ids=["只填写账户名",
        "只填写账户名密码",
        "填写错误验证码",
        "不存在账号"])
def login_data(request):
    return request.param


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    hook函数失败用例截图添加
    @param item:
    @param call:
    @return:
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        # 失败时进行错误截图添加
        page.screenshots("错误截图")
