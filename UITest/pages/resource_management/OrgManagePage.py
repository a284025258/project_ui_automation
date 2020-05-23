import logging
import re
from time import sleep

import allure

from UITest.common.po_base import El, Page, Els
from UITest.controls.DropDownBox import DropDownBox
from UITest.controls.Table import Table
from UITest.controls.TreeDropDownBox import TreeDropDownBox
from UITest.pages.IndexPage import IndexPage
from UITest.utils.selection import select_el

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

school_org_list = ["小学", "初中", "高中", "完中（初中高中）", "中职", "大学", "其他"]


class OrgManagePage(IndexPage):
    """部门管理页面"""

    def switch_tab(self, tab_name):
        with allure.step(f"切换至{tab_name}"):
            sleep(1)
            self.action.click(text=tab_name)

            modules = {
                "机构信息维护": OrgInfoMaintainPage,
                "部门信息维护": DepartmentInfoMaintainPage,
                "下级机构管理": SubOrgManagePage
            }
            return modules[tab_name](self)


class OrgInfoMaintainPage(OrgManagePage):
    """机构信息维护页面"""

    # 基本信息
    org_name = El("机构名称", css="#OrgName")
    org_code = El("机构代码", css=".form-control-static")
    org_type = El("机构类型", x='//label[contains(text(),"机构类型")]/following-sibling::div/p')
    area = El("行政区划", x='//label[contains(text(),"行政区划")]/following-sibling::div/p')
    org_count = El("编制人数", css="#EditCount")
    org_alias = El("机构简称", css="#OrgAlias")
    glkqmc = El("考区名称", css="#GLKQMC")
    duty_tel = El("联系电话", css="#DutyTel")
    address = El("地址", css="#Address")

    # 其他信息
    contact_name = El("机构联系人", css="#tempSearch_ContactName")
    contact_tel = El("机构联系人电话", css="#p_contacTel")
    technician_name = El("技术负责人", css="#tempSearch_TechnicianName")
    technician_tel = El("技术负责人电话", css="#p_TechnicianTel")
    longitude = El("经度", css="#Longitude")
    latitude = El("维度", css="#Latitude")

    search_technician_name = El("机构联系人搜索按钮", css='#demo-tabs-box-1 span.input-group-addon-ContactName')
    search_technician_name_box = El("机构联系人搜索框", mode="V", x='(//*[contains(@class,"panel combo-p")])[1]')

    search_contact_name = El("技术负责人搜索按钮", css='#demo-tabs-box-1  span.input-group-addon-TechnicianName')
    search_contact_name_box = El("技术负责人搜索框", mode="V", x='(//*[contains(@class,"panel combo-p")])[2]')

    save_btn = El("保存按钮", css="#orgEditSave")

    def search_contact(self, name):
        """搜索机构联系人"""
        with allure.step(f"搜索机构联系人:{name}"):
            self.contact_name.clear()
            self.contact_name.send_keys(name)
            info = Table(self.search_contact_name_box).info
            logger.info(info)
            self.screenshot_in_allure()
        return info

    def search_technician(self, name):
        """搜索机构负责人"""
        with allure.step(f"搜索机构负责人:{name}"):
            self.technician_name.clear()
            self.search_technician_name.click()
            self.technician_name.send_keys(name)
            logger.info(Table(self.search_technician_name_box).info)
            self.screenshot_in_allure()

    @property
    def base_info(self):
        """基础信息"""
        _info = dict()

        _info["机构名称"] = self.org_name.get_attribute("value")
        _info["机构代码"] = self.org_code.text
        _info["机构类别"] = self.org_type.text
        _info["行政区划"] = self.area.text
        _info["编制人数"] = self.org_count.get_attribute("value")
        _info["机构简称"] = self.org_alias.get_attribute("value")
        _info["考区名称"] = self.glkqmc.get_attribute("value")
        _info["联系电话"] = self.duty_tel.get_attribute("value")
        _info["地址"] = self.address.get_attribute("value")

        return _info

    @property
    def other_info(self):
        """其他信息"""
        _info = dict()

        _info["机构联系人"] = self.contact_name.get_attribute("value")
        _info["机构联系人电话"] = self.contact_tel.text
        _info["技术负责人"] = self.technician_name.get_attribute("value")
        _info["技术负责人电话"] = self.technician_tel.text
        _info["经度"] = self.longitude.get_attribute("value")
        _info["维度"] = self.latitude.get_attribute("value")

        return _info


class DepartmentInfoMaintainPage(OrgManagePage):
    """部门信息维护"""

    add_department_btn = El("新增部门按钮", css="#btnAddDepartment")
    info_table = El("信息表", css="#divTemplate table")

    def del_department(self, d_name):
        with allure.step(f"删除{d_name}部门"):
            val = f'//*[text()="{d_name}"]/parent::tr//*[text()="删 除"]'
            self.click(x=val)
            self.click(x='//a[text()="删除"]')
        return self

    def click_add_department_btn(self):
        with allure.step("点击新增部门按钮"):
            self.click(el=self.add_department_btn)
        return self.NewDepartment(self)

    def get_tr(self, info):
        sleep(0.5)
        return Table(self.info_table).get_row(info)

    @property
    def table_info(self):

        return Table(self.info_table).info

    class NewDepartment(Page):
        department_name = El("部门名称", mode="I", css="#Name")
        department_type = El("部门类型下拉框", css=".dropdown-menu.open")
        department_type_opener = El("部门类型下拉框激活", css="button[data-id]")
        exam_projects = Els("分管考试项目", css="#dv_EtId label")
        submit_btn = El("保存", css="button[type='submit']")
        msg = El("信息框内容", css="div.layui-layer-padding")
        confirm_btn = El("确认按钮", css=".layui-layer-btn0")

        def add_department(self, info):
            """
            添加部门
            @param info = {
                "d_name":部门名称,
                "d_type":部门类别,
                "d_domain":[部门分管考试项目]
            }
             department_name: 部门名称
             department_type: 部门类别  ["管理部门","业务部门","技术部门","综合部门","后勤部门"]
             exam_projects: 部门分管考试项目
            ["普通高考", "成人高考", "研究生考试", "自考", "学业水平考试", "计算机等级考试",
             "英语四六级B级考试", "中小学教师资格考试", "英语等级考试（PETS）", "书画等级考试（CCPT）",
             "高校教师技能考试", "高校自主选拔测试", "高校教师理论考试", "剑桥少儿英语（YLE）"]

            @return:
            """

            department_name = info["d_name"]
            department_type = info["d_type"]
            exam_projects = info["d_domain"]

            self.switch_to_frame(locator="main-body", switch_out=False)
            with allure.step("添加部门"):
                self.click(self.department_name)
                self.department_name.send_keys(department_name)

                DropDownBox(self.department_type, self.department_type_opener).select(department_type)
                if exam_projects:
                    for exam_project in exam_projects:
                        el = select_el(self.exam_projects, exam_project)
                        self.click(el=el)
                self.screenshot_in_allure()

                self.click(el=self.submit_btn)
                logger.info(f"提示信息：{self.msg.text}")
                self.screenshot_in_allure()
                self.click(el=self.confirm_btn)
                self.switch_to_frame()
            # 加载信息过慢
            sleep(3)
            return DepartmentInfoMaintainPage(self)


class SubOrgManagePage(OrgManagePage):
    """下级机构管理"""
    # 搜索框
    query_org_drop_box = El("管理机构下拉列表", css="#orgtree_value_layer")
    query_org_drop_box_opener = El("管理机构下拉列表激活框", css="#orgtree_name")

    query_org_type_drop_box = El("机构类型下拉列表", css="#orgtypetree_value_layer")
    query_org_type_drop_box_opener = El("机构类型下拉列表", css="#orgtypetree_name")

    query_org_btn = El("查询按钮", css="#btnQuery")
    search_org_name_input = El("机构名称搜索输入框", css="#orgSearch")
    search_org_name_btn = El("机构名称搜索按钮", css="#btnSearch")
    # 内容
    info_table = El("机构管理表", css="#divOrgContent")
    # 新增机构
    add_org_btn = El("新增机构按钮", id="btnAddOrg")

    def click_add_org_btn(self):
        self.add_org_btn.click()
        return SubOrgManagePage.NewOrgPage(self)

    @property
    def org_name_compliance(self):
        """
        判断机构名称是否合规，通过机构名称前的标号进行判断
        @return:
        """
        i = self.table.info
        s_org_names = self.table.info["机构名称"]
        org_nums = list(map(lambda s: re.findall(r"\d+", s)[0], s_org_names))
        org_num = re.findall(r"\d+", self.org_name)[0]
        for item in org_nums:
            if not item.startswith(org_num):
                return False
        else:
            return True

    @property
    def org_type_compliance(self):
        """判断机构类型是否合规"""
        if self.org_type == "全部":
            # 若选择为全部，则直接返回True
            return True
        org_types = self.table.info["机构类型"]
        if len(org_types) == 0:
            # 判断没有搜索到，则直接返回True
            return True
        if self.org_type == "学校":
            # 搜索为学校，判断表中类型是否为c_list中的值

            for org_type in org_types:
                if org_type not in school_org_list:
                    return False
            else:
                return True
        else:
            # 搜索为固定
            if len(set(org_types)) != 1:
                # 不止一种返回False
                return False
            return self.org_type == org_types[0]

    @property
    def table(self):
        return Table(self.info_table)

    @property
    def org_type(self):
        """机构类型"""
        return TreeDropDownBox(self.query_org_type_drop_box, self.query_org_type_drop_box_opener).value

    @property
    def org_name(self):
        """机构名称"""
        return TreeDropDownBox(self.query_org_drop_box, self.query_org_drop_box_opener).value

    def select_org(self, *org_names):
        tag = True
        for i, org_name in enumerate(org_names, 1):
            if i == len(org_names):
                tag = False
            self._select_org(org_name, tag)

    def select_org_type(self, *org_types):
        tag = True
        for i, org_type in enumerate(org_types, 1):
            if i == len(org_types):
                tag = False
            self._select_org_type(org_type, tag)

    def _select_org(self, org_name, _open=False):
        """
        选择管理机构
        @param _open: 展开机构
        @param org_name: 机构名称
        @return:
        """
        tree = TreeDropDownBox(self.query_org_drop_box, self.query_org_drop_box_opener)
        tree.open(org_name) if _open else tree.select(org_name)
        return self

    def _select_org_type(self, org_type, _open=False):
        """
        选择机构类型
        @param _open: 展开机构类型
        @param org_type: 机构类型
        @return:
        """
        tree = TreeDropDownBox(self.query_org_type_drop_box, self.query_org_type_drop_box_opener)
        tree.open(org_type) if _open else tree.select(org_type)

        return self

    def search_org(self, org_name):
        """按机构名称搜索"""
        self.search_org_name_input.clear()
        self.search_org_name_input.send_keys(org_name)
        self.search_org_name_btn.click()
        return self

    class NewOrgPage(Page):
        """新增机构弹出界面"""
        frame_el = El("弹出框定位", css="#main-body")

        org_type_select = El("机构类型选择", x='//*[@data-id="OrgType"]/following::div[1]')
        org_type_select_opener = El("机构类型选择激活器", css='[data-id="OrgType"]')

        school_type_select = El("学校类型选择", x='//*[@data-id="SchoolType"]/following::div[1]')
        school_type_opener = El("学校类型选择激活器", css='[data-id="SchoolType"]')

        org_code_input = El("机构代码输入框", css="#OrgDisplayCode")
        org_name_input = El("机构名称输入框", css="#OrgName")
        org_alias_input = El("机构简称输入框", css="#OrgAlias")
        org_area_input = El("考区名称", mode="V", css="#GLKQMC")

        submit_btn = El("保存按钮", css='[type="submit"]')
        confirm_btn = El("确认按钮", x='//*[text()="确定"]')

        _org_account = El("机构账号", css="#label_account")

        @property
        def org_account(self):
            return self._org_account.text

        def add_org_school(self, school_type, org_num, org_name, org_ab, area_name=""):
            """
            添加学校类型的机构
            @param school_type: 学校类型
            @param org_num: 机构编号
            @param org_name: 机构名称
            @param org_ab:机构简称
            @param area_name:区域名称 || 大学才有
            @return:
            """
            with allure.step("添加学校类型的机构"):
                self.switch_to_frame(self.frame_el, switch_out=False)
                self.select_org_type("学校")
                assert school_type in school_org_list
                DropDownBox(self.school_type_select, self.school_type_opener).select(school_type)
                self.org_code_input.send_keys(org_num)
                self.org_name_input.send_keys(org_name)
                self.org_alias_input.send_keys(org_ab)
                if area_name and school_type == "大学":
                    self.org_area_input.send_keys(area_name)
                self.click(el=self.submit_btn)
                self.click(el=self.confirm_btn)
                self.switch_to_frame()
            return SubOrgManagePage(self)

        def select_org_type(self, val):
            DropDownBox(self.org_type_select, self.org_type_select_opener).select(val)
