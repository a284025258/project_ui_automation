import logging
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from UITest.pages.BasePage import BasePage

from UITest.common.po_base import El

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LoginPage(BasePage):
    username = El("用户名输入框", name="myuser")
    password = El("密码输入框", name="loginpassword")
    login_button = El("登录按钮", css="div.yh-login-btn > button")
    message_box = El("登录提示信息", css=".ant-message")
    verify_box = El("验证码", xpath="//*[placeholder='请输入验证码']")
    test_flag = El("登陆页面的测试条", css=".xt-flag-test")

    def login(self, username, password):
        logger.info("登录用户名：>>>{}，登录密码>>>{}".format(username, password))
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.verify()
        self.login_button.click()
        if self.is_login:
            logger.info("登录成功返回主页")
            return self.pm("IndexPage")(self)
        else:
            return self

    def verify(self):
        """
        验证码验证实现
        """
        self.verify_box.click()
        input("输入验证码后敲回车")

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
        try:
            self.driver.find_element_by_css_selector("div.yh-login-btn > button")
        except NoSuchElementException:
            return True
        return False


class PWDChangeBox(BasePage):
    box = El("修改密码框体", css=".ant-modal-content")
    close_button = El("关闭按钮", css=".ant-modal-close-x")
    new_pwd = El("新密码", css="#resetpwd_form_newPwd")
    confirm_pwd = El("确认密码", css="#resetpwd_form_confirmPwd")
    commit_button = El("确认密码", css="button.ant-btn.ant-btn-primary")

    def change_pwd(self, new_pwd, confirm_pwd=None):
        if confirm_pwd is None:
            confirm_pwd = new_pwd
        self.new_pwd.send_keys(new_pwd)
        self.confirm_pwd.send_keys(confirm_pwd)
        self.commit_button.click()

    def close(self):
        self.close_button.click()
        return LoginPage(self)
