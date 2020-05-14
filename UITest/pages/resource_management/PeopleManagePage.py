from UITest.common.po_base import El, Els
from UITest.pages.IndexPage import IndexPage
from UITest.utils.selection import select_el


class PeopleManagePage(IndexPage):
    org_select = Els('部门选择', x='//*[@id="select"]/div[3]//li')
    type_select = Els('编制类型选择', x='//*[@id="select"]/div[4]//li')

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
