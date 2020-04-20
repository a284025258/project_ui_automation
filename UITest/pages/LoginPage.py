from time import sleep

import allure
from poium import PageElement

from UITest.pages.BasePage import BasePage
from UITest.pages.HomePage import HomePage


class LoginPage(BasePage):
    username = PageElement(describe="用户名输入框", css="input[placeholder='请输入用户名']")
    password = PageElement(describe="密码输入框", css="input[placeholder='请输入密码']")
    login_button = PageElement(describe="登录按钮", css="div.yh-login-btn > button")
    message_box = PageElement(describe="登录提示信息", css=".ant-message")
    quit_button = PageElement(describe="安全退出", xpath="//font[text()='安全退出']")
    slider_button = PageElement(describe="滑动滑块按钮", css=".slider")

    def login(self, username, password):
        self.logger.info("登录用户名：》{}《，登录密码》{}《".format(username, password))
        with allure.step("尝试登录"):
            self.username.clear()
            self.username.send_keys(username)
            self.password.clear()
            self.password.send_keys(password)
            self.verify()
            self.login_button.click()
        if self.is_login:
            with allure.step("登录成功返回主页"):
                self.logger.info("登录成功返回主页")
                return HomePage(self.driver)
        else:
            return self

    def verify(self):
        """
        验证码验证实现
        :return:
        """
        self.click_and_hold(self.slider_button)
        self.move_by_offset(220, 0)
        self.release()

    @property
    def error_message(self):
        sleep(0.5)
        msg = self.message_box.text
        self.logger.info("登录提示信息为》{}《".format(msg))
        return msg

    @property
    def is_login(self):
        """
        判断是否登录成功
        :return:
        """
        with allure.step("断言登录情况"):
            return False if self.quit_button is None else True
