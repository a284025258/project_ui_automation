from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from UITest.common.po_base import El, Page, Els
from UITest.pages.IndexPage import IndexPage
from UITest.utils.selection import select_el


class OrgManagePage(IndexPage):
    """部门管理页面"""

    def switch_tab(self, tab_name):
        self.click(By.XPATH, f"//*[text()='{tab_name}']")
        return self


class OrgInfoMaintainPage(OrgManagePage):
    """机构信息维护页面"""

    # 基本信息
    org_name = El("机构名称", css="#OrgName")
    org_code = El("机构代码", css="#OrgName")
    org_type = El("机构类别",
                  css="#demo-tabs-box-1 > fieldset:nth-child(2) > div > div:nth-child(1) > div:nth-child(2) > div > p")
    area = El("行政区划",
              css="#demo-tabs-box-1 > fieldset:nth-child(2) > div > div:nth-child(1) > div:nth-child(4) > div > p")
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
            self.department_name.send_keys(department_name)
            Select(self.department_type).select_by_visible_text(department_type)
            if exam_projects:
                for exam_project in exam_projects:
                    select_el(self.exam_projects, exam_project)


class SubOrgManagePage(OrgManagePage):
    """下级机构管理"""
    add_org_btn = El("新增机构", id="btnAddOrg")
    org_type_select = El("机构类型选择", id="OrgType")

    def select_org_type(self, text):
        Select(self.org_type_select).select_by_visible_text(text)
