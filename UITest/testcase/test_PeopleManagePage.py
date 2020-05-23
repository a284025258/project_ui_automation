import allure
import pytest

from UITest.pages.resource_management.PeopleManagePage import PeopleManagePage


@pytest.fixture()
def switch_to_people_management(login_as):
    """切换至人员管理"""
    index_page = login_as("S")
    index_page.driver.refresh()

    with allure.step("切换至人员管理"):
        page = index_page.select_top_menu("统一基础资源管理") \
            .select_aside_menu("人员管理")
        page: PeopleManagePage = page.pm("PeopleManagePage")(page)
    return page


class TestPeopleManagePage:
    def test_query_people(self, switch_to_people_management):
        o_name = ""
        c_type = ""
        j_type = ""
        p_name_or_id = ""

        page = switch_to_people_management
        page.query_people(o_name, c_type, j_type, p_name_or_id)
