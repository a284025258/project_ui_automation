from time import sleep

import allure
import pytest


@allure.feature("测试登陆页")
class TestLogin:
    """
    测试登录功能
    """

    @allure.severity(allure.severity_level.NORMAL)
    def test_login_fail_message(self, login_page, login_data):
        """
        测试登录失败时的提示是否正确
        """

        login_page.login(login_data["username"], login_data["password"])
        with allure.step("断言错误消息"):
            assert login_data["check_text"] == login_page.error_message
        with allure.step("断言登录状态"):
            assert not login_page.is_login
        sleep(1)

    @pytest.mark.skip
    def test_login_success(self):
        pass
