import logging
import re

from poium import PageElement, PageElements

from UITest.pages.BasePage import BasePage
from UITest.pages.IndexPage import IndexPage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class IndexPageMaxIn:
    pass


class UserInfoBox(BasePage):
    """
    个人信息   右上角点击后
    """
    close_button = PageElement(describe="关闭按钮", css=".ant-modal-close-x")
    base_info_box = PageElement(describe="基本信息框", css="#uinfo_form .ant-col.ant-col-14")
    submit_button = PageElement(describe="保存按钮", css="#uinfo_form button")
    # 界面问题导致的代码问题
    other_info_box_title = PageElement(describe="其他信息框标题", css="#uinfo_form .ant-row.xt-uinfo-header")
    other_info_box_info = PageElement(describe="其他信息框内容", css="#uinfo_form .ant-row.xt-uinfo-text")
    _cell = PageElements(describe="内容", context=True, css="div.ant-col")

    @property
    def base_info(self) -> dict:
        """
        通过对innerHTML的读取，将内容作为字典返回
        fixme 如果改变页面布局可能需要该改代码
        @return: info_
        """
        raw_info = self.base_info_box.get_attribute('innerHTML')

        _ = [re.sub("[\u3000（： ]", "", info) for info in re.findall(">(.*?)<", raw_info) if info]
        # _ = ['姓名', '王华', '性别', '男', '民族', '汉族', '验证状态', '已认证', '身份验证', '通过', '照片合规', '通过',
        # '人脸比对', '通过', '）', '办公电话', '联系电话', '邮箱']
        div_info = _[:-4]
        info_ = dict(zip(div_info[::2], div_info[1::2]))
        # info_ = {'姓名': '王华', '性别': '男', '民族': '汉族', '验证状态': '已认证',
        # '身份验证': '通过', '照片合规': '通过', '人脸比对': '通过'}

        input_info = re.findall("value=\"(.*?)\"", raw_info)
        # input_info = ['07715320540', '18100771469', '']
        info_.update(dict(zip(_[-3:], input_info)))

        return info_

    @property
    def other_info(self) -> dict:
        titles = [el.text for el in self._cell(self.other_info_box_title)]
        info = [el.text for el in self._cell(self.other_info_box_title)]

        return dict(zip(titles, info))

    def close_box(self):
        """
        关闭弹出框
        @return:
        """
        self.close_button.click()
        return IndexPage(self)


class PassWordChangeBox(BasePage):
    """
    修改密码框
    """
    old_password_box = PageElement(describe="旧密码", id_="resetpwd_form_oldPwd")
    new_password_box = PageElement(describe="新密码", id_="resetpwd_form_newPwd")
    confirm_password_box = PageElement(describe="确认新密码", id_="resetpwd_form_confirmPwd")
    change_password_submit_button = PageElement(describe="提交", xpath='//button[contains(string(),"提")]')
    change_password_cancel_button = PageElement(describe="取消", xpath='//button[contains(string(),"消")]')
    close_button = PageElement(describe="关闭按钮", css='button[aria-label="Close"]')

    def change_password(self, old, new, confirm_password=None):
        """
        重置密码
        @param old: 旧密码
        @param new: 新密码
        @param confirm_password: 确认密码为空时为新密码
        @return:
        """
        self.old_password_box.clear()
        self.old_password_box.send_keys(old)
        self.new_password_box.clear()
        self.old_password_box.send_keys(new)
        self.confirm_password_box.clear()
        if confirm_password is None:
            self.confirm_password_box.send_keys(new)
        else:
            self.confirm_password_box.send_keys(confirm_password)
        self.change_password_submit_button.click()

    def close_box(self):
        self.close_button.click()
        return IndexPage(self)
