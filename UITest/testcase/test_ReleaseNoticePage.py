import allure
import pytest

from UITest.common.faker_info import f
from UITest.common.page_manage import pm


@pytest.fixture()
def switch_to_notice_page(login_as):
    """切换至发布通知界面"""
    index_page = login_as("D")
    index_page.driver.refresh()

    with allure.step("切换至发布通知界面"):
        page = index_page.select_top_menu("考情综合管理") \
            .select_aside_menu("通知公告") \
            .select_aside_menu("通知管理") \
            .select_aside_menu("发布通知")
        release_notice_page = pm("ReleaseNoticePage")(page)

    yield release_notice_page


@allure.severity(allure.severity_level.NORMAL)
@allure.feature("考情综合管理->通知公告->通知管理->发布通知")
class TestReleaseNoticePage:

    def test_send_notice(self, switch_to_notice_page):
        """测试发布通知"""
        with allure.step("发布通知"):
            title = "测试标题" + f.sentence(3)
            content = "测试内容\n" + f.text(500)
            my_notice_page = switch_to_notice_page.send_notice(title, "全部", content)
        with allure.step("检查通知发布情况"):
            page = my_notice_page.check_detail(title)
            page.screenshot_in_allure("检查通知发布情况")
        assert content in page.detail_content.text

    def test_send_notice2(self, switch_to_notice_page):
        """测试发布通知2"""
        with allure.step("发布通知"):
            title = "测试标题" + f.sentence(3)[:-1]
            content = "测试内容\n" + f.sentence(100)[:-1]
            my_notice_page = switch_to_notice_page.send_notice(title, "全部", content)
        with allure.step("检查通知发布情况"):
            page = my_notice_page.check_detail(title)
            page.screenshot_in_allure("检查通知发布情况")
        assert content in page.detail_content.text
