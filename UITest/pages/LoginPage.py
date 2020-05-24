import logging
import os
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from UITest.common.po_base import El, Page
from UITest.config import WEB_ROLE_CONF
from UITest.utils.get_verify_code import get_verify_code
from config import STATIC_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LoginPage(Page):
    username = El("用户名输入框", name="myuser")
    password = El("密码输入框", css="input[placeholder='请输入密码']")
    login_button = El("登录按钮", css="div.yh-login-btn > button")
    message_box = El("登录提示信息", css=".ant-message", mode="V")
    verify_box = El("验证码输入框", x="//*[@placeholder='请输入验证码']")
    verify_img = El("验证码图片", css="img[alt]")
    test_flag = El("登陆页面的测试条", css=".xt-flag-test")

    def login(self, username, password):
        logger.info("登录用户名：>>>{}，登录密码>>>{}".format(username, password))
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.verify()
        if self.is_login:
            logger.info("登录成功返回主页")
            return self.pm("IndexPage")(self)
        else:
            return self

    def login_as_role(self, role_name):
        """通过配置的角色名登陆"""
        info = WEB_ROLE_CONF[role_name]
        return self.login(*info)

    def verify(self, max_time=30):
        """
        验证码验证实现
        """
        if max_time == 0:
            raise RuntimeError("验证码重试次数过多")
        self.verify_img.click()
        tmp_png_name = os.path.join(STATIC_DIR, "tmp/tmp.png")
        self.verify_img.screenshot(tmp_png_name)
        verify_code = get_verify_code(tmp_png_name)
        self.verify_box.send_keys(verify_code)
        self.login_button.click()
        sleep(0.5)
        if self.is_login:
            return True
        max_time -= 1
        return self.verify(max_time)

    @property
    def error_message(self):
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
            self.login_button
        except NoSuchElementException:
            return True
        return False

    class PWDChangeBox(Page):
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
