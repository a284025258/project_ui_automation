from poium import PageElements

from UITest.pages.BasePage import BasePage
from UITest.utils.selection import select_el


class PeopleManagePage(BasePage):
    org_select = PageElements(describe='部门选择', xpath='//*[@id="select"]/div[3]//li')
    type_select = PageElements(describe='编制类型选择', xpath='//*[@id="select"]/div[4]//li')

    def select_org(self, by):
        """
        选择部门
        @param by:
        @return:
        """
        el = select_el(self.org_select, by)
        el.click()

    def select_type(self, by):
        """
        选择编制类型
        @param by:
        @return:
        """
        el = select_el(self.type_select, by)
        el.click()
