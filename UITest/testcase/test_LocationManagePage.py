import logging

import pytest

from UITest.common.faker_info import f
from UITest.pages.resource_management.LocationManagePage import LocationManagePage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestLocationManagePage:
    """物理场所管理测试用例"""

    @pytest.mark.dev
    @pytest.mark.run(order=1)
    def test_add_build(self, switch_to_page):
        """测试添加场所建筑"""
        test_info = {
            "建筑名称": "自动测试楼" + f.sentence(), "楼层总数": "5"
        }
        page: LocationManagePage = switch_to_page("物理场所管理")
        table = page.click_site_building_management_button() \
            .add_build(test_info).table
        info = table.get_row(test_info["建筑名称"])
        assert info

    @pytest.mark.dev
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("i", range(10))
    def test_add_place(self, switch_to_page, i):
        """测试添加十个建筑"""
        test_info = {
            "场所类型": "标准化考场", "场所名称": "自动测试楼", "楼层": "1层", "房间信息": "100" + str(i),
            "默认座次": "66666"
        }

        page: LocationManagePage = switch_to_page("物理场所管理")
        page.click_add_site_button() \
            .add_site(test_info)
