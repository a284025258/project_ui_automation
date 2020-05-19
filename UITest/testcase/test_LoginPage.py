import allure
import pytest

from UITest.config import WEB_ROLE_CONF

@pytest.mark.skip()
@allure.severity(allure.severity_level.BLOCKER)
@allure.feature("首页->登陆")
class TestLoginPage:

    @pytest.mark.parametrize("role", WEB_ROLE_CONF.keys())
    @pytest.mark.run(order=-1)
    def test_login(self, role, login_as):
        login_page = login_as(role)
        assert login_page.is_login
