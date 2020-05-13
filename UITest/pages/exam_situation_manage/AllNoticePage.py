import logging

from selenium.webdriver.common.keys import Keys

from UITest.common.po_base import El
# from UITest.controls.Table import Table
from UITest.pages.IndexPage import IndexPage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AllNoticePage(IndexPage):
    """
    考情综合管理-->全部通知
    """
    all_notice_table = El("通知表格", css="table")
    notice_search_box = El("通知搜索", css="div.hf-ai-serBox input")

    def search_notice(self, arg):
        self.notice_search_box.send_keys(arg)
        self.notice_search_box.send_keys(Keys.ENTER)
        return self

    @property
    def table(self):
        return
        # return Table(self.all_notice_table)

    def check_detail(self, notice):
        self.find_element("xpath", "//div[@title='{}']".format(notice)).click()
        return self.pm("NoticeDetailPage")(self)
