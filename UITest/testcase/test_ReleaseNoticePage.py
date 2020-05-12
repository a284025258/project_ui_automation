import allure

from UITest.common.page_manage import pm
from UITest.pages.IndexPage import IndexPage
from UITest.pages.exam_situation_manage.ReleaseNoticePage import ReleaseNoticePage


@allure.feature("考情综合管理->通知公告->通知管理->发布通知")
class TestReleaseNoticePage:
    def test_send_notice(self, login_page):
        """测试发布通知"""
        index_page = login_page.login("D5101", "Sceea@123")
        index_page: IndexPage
        release_notice_page = pm("ReleaseNoticePage")(index_page.select_top_menu("考情综合管理") \
                                                      .select_aside_menu("通知公告") \
                                                      .select_aside_menu("通知管理") \
                                                      .select_aside_menu("发布通知"))
        release_notice_page: ReleaseNoticePage
        my_notice_page = release_notice_page.send_notice("自动化测试发布通知标题", "全部", "自动化测试发布通知内容")
        assert my_notice_page.check_detail("自动化测试发布通知标题").detail_content.text == "自动化测试发布通知内容"
