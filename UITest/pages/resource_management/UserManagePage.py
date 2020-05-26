import logging

import allure

from UITest.common.po_base import El
from UITest.controls.DivTable import DivTable
from UITest.controls.DropDownBox import DropDownBox
from UITest.pages.IndexPage import IndexPage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserManagePage(IndexPage):
    department_drop = El("部门下拉框", x='(//div[@aria-controls])[1]')
    preparation_type_drop = El("编制类型下拉框", x='(//div[@aria-controls])[2]')
    query_button = El("查询按钮", x='//button[string()="查询"]')
    user_add_button = El("新增用户按钮", x='//button[string()="新增用户"]')
    _table = El("表格", css='.yh-userlist-wrap')

    @property
    def table(self):
        return DivTable(self._table, {"x": './div[@class="yh-userlist-header"]//span'},
                        {"css": ".yh-userlist-info.yh-border-bottom"},
                        {"x": "./span"})

    def query_user(self, info):
        """
        查询用户
        :param info:
        {"部门":"","编制类型":""}
        :return:
        """
        with allure.step(f"查询用户:查询条件>>>{info}"):
            _select_something(self, self.department_drop, info.get("部门"))
            _select_something(self, self.preparation_type_drop, info.get("编制类型"))
            self.query_button.click()
        return self

    def click_user_add_btn(self):
        """点击新增人员按钮"""
        self.user_add_button.click()
        return self.UserAddPage(self)

    @property
    def info_complite(self):
        """结果与搜索条件相同"""
        result = self._department_complite and self._preparation_type_complite
        if not result:
            logger.error(f"结果不同表中信息为：\n {self.table.info}")
            self.screenshot_in_allure("结果不同")
        return result

    @property
    def _department_complite(self):
        """部门信息相同"""
        t = self.department_drop.text
        if t == "全部":
            return True
        for info in self.table.info["部门名称"]:
            if t != info:
                return False
        else:
            return True

    @property
    def _preparation_type_complite(self):
        """编制类型相同"""
        t = self.preparation_type_drop.text
        if t == "全部":
            return True
        for info in self.table.info["编制类型"]:
            if t != info:
                return False
        else:
            return True

    class UserAddPage(IndexPage):
        """用户添加框弹出"""
        _table = El("表格", css='.ws-table-box')
        save_btn = El("保存按钮", x='//button[string()="保存"]')
        cancel_btn = El("取消按钮", x='//button[string()="取消"]')

        @property
        def table(self):
            return DivTable(self._table, {"css": "p>span"}, {"css": ".gwj-table-box-tableItem"}, {"x": "./div"})

        def select_row_by_name(self, name):
            """通过名称选择表格中对应行的label框"""
            if name == "全部":
                self.click(el=self._table.find_element_by_xpath('.//*[text()="姓名"]/parent::p//input'))
            else:
                self.click(el=self._table.find_element_by_xpath(f'.//*[text()="{name}"]/parent::div//input'))
            return self

        def select_check_box_by_index(self, index):
            """通过index选择label框，index为0时选择全部"""
            els = self._table.find_elements_by_css_selector(".ant-checkbox-input")
            self.click(el=els[index])
            return self

        def select_role_by_name(self, name, role_name):
            """通过用户名字选择角色类型"""
            tr = None
            for tr in getattr(self.table, "_trs"):
                if name in tr.get_attribute("innerText"):
                    break
            else:
                logger.error(f"没有找到>>>{name}>>>对应的人员")
            if tr:
                _select_something(self, tr.find_element_by_xpath("(.//div[@aria-controls])[1]"), role_name)


def _select_something(self, el, val):
    """这个页面选择控件的代理选择的实现"""
    # todo 抽取到控件中去
    if val:
        el.click()
        _s_id = el.get_attribute("aria-controls")
        DropDownBox(self.find_element(mode="V", id=_s_id), el).select(val)
