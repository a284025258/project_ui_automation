import allure

from UITest.common.page_manage import pm
from UITest.pages.IndexPage import IndexPage


@allure.feature("考情综合管理->通知公告->通知管理->发布通知")
class TestReleaseNoticePage:
    def test_send_notice(self,login_page):
        """测试发布通知"""
        index_page=login_page.login("D5101","Sceea@123")
        index_page:IndexPage
        index_page.select_top_menu("考情综合管理")\
            .select_aside_menu("通知公告")
        pm("ReleaseNoticePage")
