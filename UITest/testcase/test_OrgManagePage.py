import logging
import re

import allure
import pytest

from UITest.common.faker_info import f
from UITest.common.page_manage import pm
from UITest.pages.resource_management.OrgManagePage import OrgManagePage, SubOrgManagePage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture(scope="module")
def switch_to_org_management(login_as):
    """切换至机构管理"""
    index_page = login_as("S")
    index_page.driver.refresh()

    with allure.step("切换至机构管理"):
        page = index_page.select_top_menu("统一基础资源管理") \
            .select_aside_menu("机构管理")
        page: OrgManagePage = pm("OrgManagePage")(page)
    return page


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("统一基础资源管理->机构管理")
class TestOrgManagePage:
    @allure.story("机构信息维护")
    def test_check_info(self, switch_to_org_management):
        """机构信息维护，部门信息检查"""
        page = switch_to_org_management.switch_tab("机构信息维护")
        base_info = page.base_info
        logger.info(base_info)
        other_info = page.other_info
        logger.info(other_info)
        page.screenshot_in_allure()

        assert base_info
        assert other_info

    @allure.story("部门信息维护")
    def test_add_department(self, switch_to_org_management):
        """新增部门"""
        d_name = "测试机构" + f.sentence(2)
        d_type = "综合部门"
        d_domain = "上半年英语四六级B级考试", "剑桥少儿英语", "统一考试"

        page = switch_to_org_management.switch_tab("部门信息维护")
        info = page.click_add_department_btn() \
            .add_department(d_name, d_type, *d_domain) \
            .get_tr(d_name)
        logger.info(f"行信息:{info}")
        assert info
        assert d_type in info
        assert set(d_domain) == set(info[3].split("、"))

    @allure.story("下级机构管理")
    def test_query_department(self, switch_to_org_management):
        org_name = "都江堰"
        page = switch_to_org_management.switch_tab("下级机构管理")
        s_org_names = page.search_org(org_name).get_table_info()["机构名称"]
        for s_org_name in s_org_names:
            assert org_name in s_org_name

    @allure.story("下级机构管理")
    def test_search_department(self, switch_to_org_management):
        org_list = ["四川省教育考试院", "成都市教育考试院", "都江堰市教育考试中心", "四川省都江堰中学"]
        org_type_list = ["学校", "高中"]
        page = switch_to_org_management.switch_tab("下级机构管理")
        page: SubOrgManagePage
        if org_list:
            with allure.step("选择管理机构"):
                page.select_org(*org_list)
            select_org_num = re.findall(r"\d+", page.query_org_drop_box_opener.get_attribute("value"))[0]
        if org_type_list:
            with allure.step("机构类型"):
                page.select_org_type(*org_type_list)
            getter = page.query_org_type_drop_box_opener.get_attribute
            select_org_type = getter("value") or "全部"
        page.query_org_btn.click()

        s_org_names = page.get_table_info()["机构名称"]
        s_org_types = page.get_table_info()["机构类型"]

        assert s_org_names

    @allure.story("下级机构管理")
    def test_add_department(self, switch_to_org_management):
        page = switch_to_org_management.switch_tab("下级机构管理")
