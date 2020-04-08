import allure
import pytest


class TestLogin:
    """
    测试登录功能
    """

    @allure.severity(allure.severity_level.NORMAL)
    def test_login_fail_message(self, loginPage, logData):
        """
        测试登录失败时的提示是否正确
        """
        loginPage.refresh_verify_code()

        loginPage.login(logData["username"], logData["password"], logData["verify_code"])
        with allure.step("断言错误消息"):
            assert logData["check_text"] == loginPage.error_message
        with allure.step("断言登录状态"):
            assert not loginPage.is_login
        loginPage.screenshots()

    @pytest.mark.skip
    def test_login_success(self):
        pass
