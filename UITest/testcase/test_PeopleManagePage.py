import allure
import pytest

from UITest.common.faker_info import f
from UITest.config import UploadImg


@allure.severity(allure.severity_level.CRITICAL)
class TestPeopleManagePage:
    def test_query_people(self, switch_to_page):
        """测试查询人员功能"""
        test_info_dict = {
            "部门": "信息技术处", "编制类型": "在编",
            "工作状态": "正常", "人员": ""
        }
        page = switch_to_page("人员管理")
        page.query_people(test_info_dict)
        assert page.info_compliance

    def test_add_people(self, switch_to_page):
        """测试增加人员"""
        test_info_dict = {
            "编制类型": "在编",
            "基础信息": {
                "姓名": f.name(), "身份证号": f.ssn(), "性别": "",
                "婚否": "未婚", "出生日期": f.date(), "民族": "汉族",
                "邮箱": f.email(), "办公电话": f.phone_number(), "联系电话": f.phone_number(),
                "上传头像图片地址": UploadImg
            },
            "其他信息": {
                "部门": "测试", "学历": "请选择", "职务": f.job(),
                "学位": "学士", "职称": "讲师", "政治面貌": "中共党员",
                # 借调、临时人员独有
                "原工作单位": "", "借调有效期": "",
            }
        }
        page = switch_to_page("人员管理")
        page = page.click_add_people_btn() \
            .choose_compilation_type(test_info_dict["编制类型"]) \
            .input_base_info(test_info_dict["基础信息"]) \
            .input_other_info(test_info_dict["其他信息"]) \
            .query_people({"人员": test_info_dict["基础信息"]["姓名"]})

        assert page.info_compliance

    @pytest.mark.parametrize("s", range(200))
    @pytest.mark.skip
    def test_only_add_people(self, switch_to_page, s):
        """增加人员"""
        test_info_dict = {
            "编制类型": "在编",
            "基础信息": {
                "姓名": f.name(), "身份证号": f.ssn(), "性别": "",
                "婚否": "未婚", "出生日期": f.date(), "民族": "汉族",
                "邮箱": f.email(), "办公电话": f.phone_number(), "联系电话": f.phone_number(),
                "上传头像图片地址": UploadImg
            },
            "其他信息": {
                "部门": "测试", "学历": "请选择", "职务": f.job(),
                "学位": "学士", "职称": "讲师", "政治面貌": "中共党员",
                # 借调、临时人员独有
                "原工作单位": "", "借调有效期": "",
            }
        }
        page = switch_to_page("人员管理")
        page = page.click_add_people_btn() \
            .choose_compilation_type(test_info_dict["编制类型"]) \
            .input_base_info(test_info_dict["基础信息"]) \
            .input_other_info(test_info_dict["其他信息"])
