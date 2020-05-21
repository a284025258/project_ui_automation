import allure
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from UITest.common.page_manage import pm
from UITest.common.po_base import Page
from UITest.config import Driver_Path, Start_Url

page = None


@pytest.fixture(scope="session")
def login_as(browser):
    def _login_as(role_name):
        with allure.step("登陆"):
            _page = pm("LoginPage")(browser)
            # _page._clear_cache()
            _page.driver.get(Start_Url)
            return _page.login_as_role(role_name)
    return _login_as


@pytest.fixture(scope='session')
def browser():
    global page
    if page is None:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        # options.add_argument("no-sandbox")
        options.add_argument('--ignore-certificate-errors')  # 忽略https报错
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        with Chrome(Driver_Path, options=options) as browser:
            page = Page(browser)
            yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    hook函数失败用例截图添加
    @param item:
    @param call:
    @return:
    """
    global page
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test calls, not setup/teardown
    if rep.failed:
        # 失败时进行错误截图添加
        if page is not None:
            page.screenshot_in_allure("错误截图")
