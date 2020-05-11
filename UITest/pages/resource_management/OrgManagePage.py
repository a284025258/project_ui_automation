from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from UITest.common.po_base import El
from UITest.pages.BasePage import BasePage


class OrgManagePage(BasePage):

    def switch_tab(self, tab_name):
        self.find_element(By.XPATH, f"//*[text()='{tab_name}']").click()


class SubOrgManagePage(BasePage):
    add_org_btn = El("新增机构", id="btnAddOrg")

    org_type_select =El("机构类型选择",id="OrgType")

    def select_org_type(self,text):
        Select(self.org_type_select).select_by_visible_text(text)