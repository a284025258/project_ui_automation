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
    # options.add_argument(
    #     'user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7;
    #     zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML,
    #     like Gecko) Version/4.0 Mobile Safari/533.1"')
    # options.binary_location=DRIVER_CHROME
    options.add_argument('--headless')
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
