import logging
import re
from random import randint

import allure
import pytest

from UITest.common.faker_info import f
from UITest.common.page_manage import pm
from UITest.pages.resource_management.OrgManagePage import OrgManagePage, SubOrgManagePage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.fixture()
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
        """新增部门后删除该部门"""
        d_name = "测试机构" + f.sentence(3)
        d_type = "综合部门"
        d_domain = "上半年英语四六级B级考试", "剑桥少儿英语", "统一考试"

        page = switch_to_org_management.switch_tab("部门信息维护")
        info = page.click_add_department_btn() \
            .add_department(d_name, d_type, *d_domain) \
            .get_tr(d_name)
        logger.info(f"行信息:{info}")
        page.screenshot_in_allure()
        assert info
        assert d_type in info
        assert set(d_domain) == set(info[3].split("、"))
        page.del_department(d_name)
        page.screenshot_in_allure()
        assert page.get_tr(d_name) is None

    @allure.story("下级机构管理")
    def test_search_department(self, switch_to_org_management):
        """搜索机构"""
        org_name = "都江堰"
        page = switch_to_org_management.switch_tab("下级机构管理")
        s_org_names = page.search_org(org_name).table.info["机构名称"]
        for s_org_name in s_org_names:
            assert org_name in s_org_name

    @allure.story("下级机构管理")
    def test_query_department(self, switch_to_org_management):
        """查询机构"""
        org_list = ["四川省教育考试院", "成都市教育考试院", "都江堰市教育考试中心", "四川省都江堰中学"]
        org_type_list = ["学校", "高中"]
        page = switch_to_org_management.switch_tab("下级机构管理")
        page: SubOrgManagePage
        with allure.step("查询机构"):
            # 选择管理机构
            if org_list:
                with allure.step("选择管理机构"):
                    page.select_org(*org_list)
            select_org_num = re.findall(r"\d+", page.org_name)[0]
            logger.info(f"选择的机构的名称：{page.org_name}")
            logger.info(f"选择的机构的编号：{select_org_num}")
            # 选择机构类型
            if org_type_list:
                with allure.step("机构类型"):
                    page.select_org_type(*org_type_list)
            logger.info(f"选择的机构的类型：{page.org_type}")
            # 进行搜索
            page.query_org_btn.click()
        with allure.step("结果判断"):
            assert page.org_name_compliance
            assert page.org_type_compliance

    @allure.story("下级机构管理")
    def test_add_org(self, switch_to_org_management):
        """新增学校机构"""
        school_type = "高中"
        org_num = f"{randint(1, 100):03d}"
        org_name = "测试机构" + f.sentence(5)
        org_ab = "测试机构缩写" + f.sentence(2)
        area_name = "测试考区名称" + f.sentence(2) if school_type == "大学" else ""
        page: SubOrgManagePage
        page = switch_to_org_management.switch_tab("下级机构管理")
        info = page.click_add_org_btn() \
            .add_org_school(school_type, org_num, org_name, org_ab, area_name) \
            .search_org(org_name).table.info
        logger.info(info)
        assert info
        for i in info["机构名称"]:
            assert org_name in i
        for i in info["机构类型"]:
            assert school_type in i
