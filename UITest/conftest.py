import allure
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from UITest.common.page_manage import pm
from UITest.common.po_base import Page
from UITest.config import Driver_Path, Start_Url, WEB_ROLE_CONF

page = None


@pytest.fixture(scope="module", params=WEB_ROLE_CONF.keys())
def index_page(login_as, request):
    """登陆"""
    index_page = login_as(request.param)
    return index_page


@pytest.fixture(scope="session")
def login_as(browser):
    """登陆fixture"""

    def _login_as(role_name, do_login=True):
        with allure.step("登陆"):
            _page = pm("LoginPage")(browser)
            _page.driver.get(Start_Url)
            if _page.is_login:
                _page.logout()
            if do_login:
                return _page.login_as_role(role_name)
            return _page

    return _login_as


@pytest.fixture(scope='session')
def browser():
    global page
    if page is None:
        options = Options()
        options.headless = True
        if options.headless:
            options.add_argument('--window-size=1920,1080')
        else:
            options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')  # 忽略https报错
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        with Chrome(Driver_Path,options=options) as browser:
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
