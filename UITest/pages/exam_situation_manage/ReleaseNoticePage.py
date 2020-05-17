from time import sleep

import allure

from UITest.common.po_base import El, Els
from UITest.pages.IndexPage import IndexPage


class ReleaseNoticePage(IndexPage):
    """
    考情综合管理-->发布通知
    """
    title = El("通知标题", css="input.ant-input")
    range = Els("接收范围", css=".gwj-InfoPub-checkbox.ant-checkbox-wrapper input")
    content = El("通知内容", css=".w-e-text")
    commit = El("发送", css="button.ant-btn.ant-btn-primary")
    dismiss = El("取消", css=".iconfont.icon-quxiao")
    recommit = El("确认发送", x="//*[text()='确 定']/..",visible=True)

    def choice_range(self, *args):
        index = {"全部": 0, "市级": 1,
                 "区县级": 2, "考点级": 3, }
        for choice in args:
            self.range[index[choice]].click()

    def send_notice(self, title, range_, content):
        self.title.send_keys(title)
        self.choice_range(range_)
        self.content.send_keys(content)
        self.screenshot_in_allure("发送通知")
        self.commit.click()
        sleep(0.5)
        self.recommit.click()
        return self.pm("MyNoticePage")(self)
