import allure
import pytest

from UITest.common.faker_info import f
from UITest.common.page_manage import pm
from UITest.pages.IndexPage import IndexPage
from UITest.pages.resource_management.OrgManagePage import OrgManagePage


@pytest.fixture()
def index_page(index_page):
    """切换至机构管理"""

    index_page.driver.refresh()
    index_page: IndexPage
    return index_page


@allure.feature("流程测试")
class TestFlow:
    """流程测试"""

    @allure.story("测试新增部门->新增人员->添加用户")
    def test_flow_new_org_new_department_add_people(self, index_page):
        """测试新增部门->新增人员->添加用户"""
        test_info = {
            "d_name": "测试机构" + f.sentence(3),
            "d_type": "综合部门",
            "d_domain": ["上半年英语四六级B级考试", "剑桥少儿英语", "统一考试"]
        }
        page = index_page.select_top_menu("统一资源管理").select_aside_menu("机构管理")
        page = pm("OrgManagePage")(page)
        page: OrgManagePage
        page.switch_tab("部门信息维护").click_add_department_btn().add_department(test_info)

        pass
