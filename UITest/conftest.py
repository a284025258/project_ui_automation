import allure
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from UITest.common.page_manage import pm
from UITest.common.po_base import Page
from UITest.config import Driver_Path, Start_Url, HandLess
from config import WEB_ROLE_CONF

page = None  # 全局page对象


@pytest.fixture(scope="module", params=WEB_ROLE_CONF.keys())
def index_page(login_as, request):
    """登陆后页面装置"""
    index_page = login_as(request.param)
    return index_page


@pytest.fixture(scope="session")
def login_as(browser):
    """登陆装置"""

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


@pytest.fixture()
def switch_to_page(index_page):
    """切换至页面菜单"""

    def _switch_to_page(page_name):
        index_page.driver.refresh()
        with allure.step(f"切换至{page_name}"):
            page = index_page.select_top_menu(0) \
                .select_aside_menu(page_name)
        return page.pm(page_name)(page)

    return _switch_to_page


@pytest.fixture(scope='session')
def browser():
    """浏览器启动装置"""
    global page
    if page is None:
        options = Options()
        options.headless = HandLess
        options.add_argument('--no-sandbox')
        if options.headless:
            options.add_argument('--window-size=1920,1080')
        else:
            options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')  # 忽略https报错
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        with Chrome(Driver_Path, options=options) as browser:
            page = Page(browser)
            yield page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    hook函数失败用例截图添加装置
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
