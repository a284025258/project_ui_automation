import allure
import pytest

from UITest.common.page_manage import pm
from UITest.pages.IndexPage import IndexPage
from UITest.pages.resource_management.OrgManagePage import OrgManagePage


@pytest.mark.parametrize("r_name", ["S", "D", "X"])
@pytest.fixture()
def index_page(login_as, r_name):
    """切换至机构管理"""

    _page = login_as(r_name)
    _page.driver.refresh()
    _page: IndexPage
    return _page


@allure.feature("流程测试")
class TestFlow:
    """流程测试"""
    @allure.story("测试新增部门->新增人员->添加用户")
    def test_flow_new_org_new_department_add_people(self,index_page):
        """测试新增部门->新增人员->添加用户"""
        page=index_page.select_top_menu("统一资源管理").select_aside_menu("机构管理")
        page=pm("OrgManagePage")(page)
        page:OrgManagePage
        page.switch_tab("部门信息维护").click_add_department_btn().add_department(

        )
        pass
