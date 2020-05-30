import allure
import pytest

from UITest.common.faker_info import f
from UITest.config import UploadImg
from UITest.pages.IndexPage import IndexPage
from UITest.pages.resource_management.OrgManagePage import OrgManagePage
from UITest.pages.resource_management.PeopleManagePage import PeopleManagePage
from common.utils.IDnumber import generate_id


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
            "部门名称": "测试机构添加" + f.sentence(1),
            "部门类别": "管理部门",
            "部门分管考试项目": ["普通高考", "成人高考", "研究生考试", "自考", "学业水平考试", "计算机等级考试", "英语四六级B级考试", "中小学教师资格考试",
                         "英语等级考试（PETS）", "书画等级考试（CCPT）", "高校教师技能考试", "高校自主选拔测试", "高校教师理论考试", "剑桥少儿英语（YLE）"]
        },

            "编制类型": "在编",
            "基础信息": {
                "姓名": f.name(), "身份证号": generate_id(), "性别": "",
                "婚否": "未婚", "出生日期": f.date(), "民族": "汉族",
                "邮箱": f.email(), "办公电话": f.phone_number(), "联系电话": f.phone_number(),
                "上传头像图片地址": UploadImg
            },
            "其他信息": {
                "部门": "管理部门", "学历": "请选择", "职务": f.job(),
                "学位": "学士", "职称": "讲师", "政治面貌": "中共党员",
                # 借调、临时人员独有
                "原工作单位": "", "借调有效期": "",

        }

        }
        page = index_page.select_top_menu(0).select_aside_menu("机构管理")
        page: OrgManagePage
        # 添加部门
        page.switch_tab("部门信息维护").click_add_department_btn().add_department(test_info["机构信息"])
        page.screenshot_in_allure("添加部门")
        page.select_aside_menu("人员管理")
        page: PeopleManagePage
        page.click_add_people_btn()\
            .choose_compilation_type(test_info["编制类型"])\
            .input_base_info(test_info["基础信息"])\
            .input_other_info(test_info["其他信息"])

        pass
