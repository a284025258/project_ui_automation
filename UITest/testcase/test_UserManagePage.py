import pytest


class TestUserManagePage:

    def test_query_user(self, switch_to_page):
        """测试查询用户"""
        test_info_dict = {"部门": "测试机构", "编制类型": "聘用"}
        page = switch_to_page("用户管理")
        assert page.query_user(test_info_dict).info_complite

    @pytest.mark.skip("未完成")
    def test_add_user(self, switch_to_page):
        """添加用户"""
        role_name = ""
        page = switch_to_page("用户管理")
        print(page.click_user_add_btn().table.info)
        assert True
