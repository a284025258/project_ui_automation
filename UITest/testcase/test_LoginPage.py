import allure
import pytest
from selenium.common.exceptions import NoSuchElementException

from UITest.config import WEB_ROLE_CONF


@allure.feature("首页->登陆")
class TestLoginPage:
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("role", WEB_ROLE_CONF.keys())
    @pytest.mark.run(order=-1)
    def test_login(self, role, login_as):
        """登陆用例"""
        login_page = login_as(role)
        assert login_page.is_login

    @allure.severity(allure.severity_level.NORMAL)
    def test_test_flag_is_not_presence(self, login_as):
        """测试标志不存在,此用例区分测试环境与生产环境"""
        page = login_as("", do_login=False)
        with pytest.raises(NoSuchElementException):
            print(page.test_flag)
