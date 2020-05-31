"""
todo 四川暂时不需要这个页面
"""
from UITest.common.po_base import El
from UITest.controls.Table import Table
from UITest.controls.TreeDropDownBox import TreeDropDownBox
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

    # 搜索框
    query_org_drop_box = El("管理机构下拉列表", css="#orgtree_value_layer")
    query_org_drop_box_opener = El("管理机构下拉列表激活框", css="#orgtree_name")

    query_org_type_drop_box = El("机构类型下拉列表", css="#orgtypetree_value_layer")
    query_org_type_drop_box_opener = El("机构类型下拉列表", css="#orgtypetree_name")

    _table = El("资质表格", css='table')

    @property
    def table(self):
        """资质表格"""
        return Table(self._table)

    @property
    def _org_type_tree(self):
        """机构-类型-树形下拉框"""
        return TreeDropDownBox(self.query_org_type_drop_box, self.query_org_type_drop_box_opener)

    @property
    def _org_name_tree(self):
        """机构-名称-树形下拉框"""
        return TreeDropDownBox(self.query_org_drop_box, self.query_org_drop_box_opener)

    @property
    def org_type(self):
        """机构类型"""
        return self._org_type_tree.value

    @property
    def org_name(self):
        """机构名称"""
        return self._org_name_tree.value

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
