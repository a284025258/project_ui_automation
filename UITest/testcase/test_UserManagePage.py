import allure
import pytest

from UITest.pages.resource_management.UserManagePage import UserManagePage


@pytest.fixture(scope="module")
def switch_to_page(login_as):
    """切换页面"""
    index_page = login_as("S")
    index_page.driver.refresh()

    with allure.step("切换至用户管理"):
        page = index_page.select_top_menu("统一基础资源管理") \
            .select_aside_menu("用户管理")
        page: UserManagePage = page.pm("UserManagePage")(page)
    return page


class TestUserManagePage:

    def test_query_user(self, switch_to_page):
        """测试查询用户"""
        test_info_dict = {"部门": "测试机构", "编制类型": "聘用"}
        page = switch_to_page
        assert page.query_user(test_info_dict).info_complite

    def test_add_user(self, switch_to_page):
        page = switch_to_page
        print(page.click_user_add_btn().table.info)
        assert True
