"""
资源管理 - 人员管理 - 测试
"""
import allure
import pytest

from UITest.common.page_manage import pm


@allure.feature("资源管理->人员管理")
class TestPeopleManagement:

    @pytest.fixture(autouse=True)
    def index(self, base_page):
        self.page = pm("IndexPage")(base_page).select_top_menu("资源管理").select_aside_menu("人员管理")

    def test_add_people(self):
        """
        增加人员
        @return:
        """
        pass
