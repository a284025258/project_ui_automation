import pytest
from selenium.webdriver import Chrome

from UITest.Pages.LoginPage import LoginPage
from config import DRIVER_CHROME




@pytest.fixture(scope='session')
def loginPage():
    driver = Chrome(DRIVER_CHROME)
    driver.get("http://10.4.3.137:8000/exwsp_web/#/login")
    loginPage = LoginPage(driver)
    yield loginPage
    loginPage.quit()


@pytest.fixture(params=[{"username": "", "password": "", "verify_code": "", "check_text": "请输入用户名"},
                        {"username": "45", "password": "", "verify_code": "", "check_text": "请输入密码"},
                        {"username": "45", "password": "12345678", "verify_code": "",
                         "check_text": "请输入验证码"},
                        {"username": "45", "password": "12345678", "verify_code": "000",
                         "check_text": "验证码错误或已过期"},
                        {"username": "0000000", "password": "0000000", "verify_code": "000",
                         "check_text": "账号不存在或密码无效"},
                        ], ids=["不填写账户名，密码和验证码",
                                "只填写账户名",
                                "只填写账户名密码",
                                "填写错误验证码",
                                "不存在账号"])
def logData(request):
    return request.param
