import allure
import pytest

from UITest.common.faker_info import f
from UITest.pages.IndexPage import IndexPage
from UITest.pages.resource_management.OrgManagePage import OrgManagePage
from UITest.pages.resource_management.PeopleManagePage import PeopleManagePage


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
        test_info = {"机构信息": {
            "d_name": "测试机构添加" + f.sentence(1),
            "d_type": "管理部门",
            "d_domain": ["普通高考", "成人高考", "研究生考试", "自考", "学业水平考试", "计算机等级考试", "英语四六级B级考试", "中小学教师资格考试",
                         "英语等级考试（PETS）", "书画等级考试（CCPT）", "高校教师技能考试", "高校自主选拔测试", "高校教师理论考试", "剑桥少儿英语（YLE）"]
        },
            "": {},
            "a": {},

        }
        page = index_page.select_top_menu(0).select_aside_menu("机构管理")
        page: OrgManagePage
        # 添加部门
        page.switch_tab("部门信息维护").click_add_department_btn().add_department(test_info["机构信息"])
        page.screenshot_in_allure("添加部门")
        page.select_aside_menu("人员管理")
        page: PeopleManagePage
        page.click_add_people_btn().input_base_info().input_other_info()

        pass
