from time import sleep

import allure
from poium import PageElement

from UITest.Pages.BasePage import BasePage
from UITest.Pages.HomePage import HomePage


class LoginPage(BasePage):
    username = PageElement(describe="用户名输入框", css="input[placeholder='请输入用户名']")
    password = PageElement(describe="密码输入框", css="input[placeholder='请输入密码']")
    verify_code = PageElement(describe="验证码输入框", css="input[placeholder='请输入验证码']")
    login_button = PageElement(describe="登录按钮", css="div.yh-login-btn > button")
    message_box = PageElement(describe="登录提示信息", css=".ant-message")
    verify_code_img = PageElement(describe="验证码图片", css="img[alt='']")
    quit_button = PageElement(describe="安全退出", xpath="//font[text()='安全退出']")

    def login(self, username, password, verify_code):
        self.logger.info("登录用户名：》{}《，登录密码》{}《，输入的验证码》{}《".format(username, password, verify_code))
        with allure.step("尝试登录"):
            self.username.clear()
            self.username.send_keys(username)
            self.password.clear()
            self.password.send_keys(password)
            self.verify_code.clear()
            self.verify_code.send_keys(verify_code)
            self.login_button.click()
        if self.is_login:
            with allure.step("登录成功返回主页"):
                self.logger.info("登录成功返回主页")
                return HomePage(self.driver)
        else:
            return self

    def refresh_verify_code(self):
        self.logger.info("刷新验证码")
        self.verify_code_img.click()
        sleep(0.2)

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
