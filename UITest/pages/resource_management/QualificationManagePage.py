from UITest.common.po_base import El
from UITest.pages.IndexPage import IndexPage


class QualificationManagePage(IndexPage):
    """资质管理页面"""
    __page_name = "资质管理"

    def switch_tab(self, tab_name):
        tabs = {
            "标准化考点": StandardizedExamSiteTab,
            "普通考点": OrdinaryExamSiteTab,
            "报名点": RegistrationPointTab,
            "评卷点": AssessmentPointTab,
        }

        return tabs[tab_name](self)


class StandardizedExamSiteTab(IndexPage):

    def query_exam_site(self):
        pass

    def search_exam_site(self):
        pass


class MaxInTab(IndexPage):
    exam_items_select_opener = El("考试项目", css='#div_ExamProject button[data-id="cboExamProject"]')
    exam_items_selects = El("考试项目菜单", mode="V", x='//button[@data-id="cboExamProject"]/parent::div//div')

    def select_exam_item(self, item_name):
        """
        选择考试项目名称
        :param item_name: 考试项目名称
        :return:
        """
        self.exam_items_select_opener.click()
        el = self.exam_items_selects.find_element_by_xpath(f".//a[text()='{item_name}']")
        self.click(el=el)
        return self

    @property
    def exam_item(self):
        """考试项目"""
        return self.exam_items_select_opener.get_attribute("title")

    def select_management_org(self, org_name):
        pass


class OrdinaryExamSiteTab(MaxInTab):
    pass


class RegistrationPointTab(MaxInTab):
    pass


class AssessmentPointTab(MaxInTab):
    pass
