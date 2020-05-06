import logging
from time import sleep

from poium import PageElement

from UITest.pages.BasePage import BasePage
from UITest.pages.HomePage import HomePage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LoginPage(BasePage):
    username = PageElement(describe="用户名输入框", css="input[placeholder='请输入用户名']")
    password = PageElement(describe="密码输入框", css="input[placeholder='请输入密码']")
    login_button = PageElement(describe="登录按钮", css="div.yh-login-btn > button")
    message_box = PageElement(describe="登录提示信息", css=".ant-message")
    quit_button = PageElement(describe="安全退出", xpath="//font[text()='安全退出']")
    slider_button = PageElement(describe="滑动滑块按钮", css=".slider")
    test_flag = PageElement(describe="test-flag", css=".xt-flag-test")

    def login(self, username, password):
        logger.info("登录用户名：>>>{}，登录密码>>>{}".format(username, password))
        self.username.send_keys("")
        self.username.clear()
        self.username.send_keys(username)
        self.password.send_keys("")
        self.password.clear()
        self.password.send_keys(password)
        self.verify()
        self.login_button.click()
        if self.is_login:
            logger.info("登录成功返回主页")
            return HomePage(self.driver)
        else:
            return self

    def verify(self):
        """
        验证码验证实现
        :return:
        """
        while not self.verified:
            self.click_and_hold(self.slider_button)
            self.move_by_offset(250, 0)
            self.release()

    @property
    def verified(self) -> bool:
        """
        判断验证是否成功
        @return: True -> 验证成功
                False -> 验证未成功
        """
        tag = self.slider_button.text == ">"
        return not tag

    @property
    def error_message(self):
        sleep(1)
        msg = self.message_box.text
        logger.info("登录提示信息为>>>{}".format(msg))
        return msg

    @property
    def is_login(self):
        """
        判断是否登录成功
        :return:
        """

        return False if self.quit_button is None else True


class PWDChangeBox(BasePage):
    box = PageElement(describe="修改密码框体", css=".ant-modal-content")
    close_button = PageElement(describe="关闭按钮", css=".ant-modal-close-x")
    new_pwd = PageElement(describe="新密码", css="#resetpwd_form_newPwd")
    confirm_pwd = PageElement(describe="确认密码", css="#resetpwd_form_confirmPwd")
    commit_button = PageElement(describe="确认密码", css="button.ant-btn.ant-btn-primary")

    def change_pwd(self, new_pwd, confirm_pwd=None):
        if confirm_pwd is None:
            confirm_pwd = new_pwd
        self.new_pwd.send_keys(new_pwd)
        self.confirm_pwd.send_keys(confirm_pwd)
        self.commit_button.click()

    def close(self):
        self.close_button.click()
        return LoginPage(self)
