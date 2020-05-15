from selenium.webdriver.support.select import Select

from UITest.common.po_base import El, Page, Els
from UITest.controls.TreeDropDownBox import TreeDropDownBox
from UITest.pages.IndexPage import IndexPage
from UITest.utils.selection import select_el


class OrgManagePage(IndexPage):
    """部门管理页面"""

    def switch_tab(self, tab_name):
        self.click(text=tab_name)
        return self


class OrgInfoMaintainPage(OrgManagePage):
    """机构信息维护页面"""

    # 基本信息
    org_name = El("机构名称", css="#OrgName")
    org_code = El("机构代码", css="#OrgName")
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

    save_btn = El("保存按钮", css="#orgEditSave")

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

    class NewDepartment(Page):
        department_name = El("部门名称", css="#Name")
        department_type = El("部门类型", css="#DeptTypeCode")
        exam_projects = Els("分管考试项目", css="#dv_EtId label")
        submit_btn = El("保存", css="button[type='submit']")

        def add_department(self, department_name, department_type, *exam_projects):
            """添加部门"""
            self.department_name.send_keys(department_name)

            Select(self.department_type).select_by_visible_text(department_type)

            if exam_projects:
                for exam_project in exam_projects:
                    el = select_el(self.exam_projects, exam_project)
                    el.click()
            self.submit_btn.click()


class SubOrgManagePage(OrgManagePage):
    """下级机构管理"""
    # 搜索框
    search_org_name_btn = El("机构名称搜索按钮", css="#btnSearch")
    search_org_name_input = El("机构名称搜索输入框", css="#orgSearch")
    query_org_drop_box = El("管理机构下拉列表", css="#orgtree_value_layer")
    query_org_drop_box_opener = El("管理机构下拉列表激活框", css="#orgtree_name")
    query_org_type_drop_box = El("机构类型下拉列表", css="#orgtypetree_value_layer")
    query_org_type_drop_box_opener = El("机构类型下拉列表", css="#orgtypetree_name")

    add_org_btn = El("新增机构", id="btnAddOrg")
    org_type_select = El("机构类型选择", id="OrgType")

    def select_org(self, org_name, _open=False):
        """
        选择管理机构
        @param _open: 展开机构
        @param org_name: 机构名称
        @return:
        """
        tree = TreeDropDownBox(self.query_org_drop_box, self.query_org_type_drop_box_opener)
        tree.open(org_name) if _open else tree.select(org_name)
        return self

    def select_org_type(self, org_type, _open=False):
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
        """新增机构"""

        org_type_select = El("机构类型选择", css="#OrgType")
        org_type_select_opener = El("机构类型选择", css="#OrgType")

        def select_org_type(self, text):
            pass
