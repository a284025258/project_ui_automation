from UITest.common.po_base import El
from UITest.controls.DropDownBox import DropDownBox
from UITest.controls.LabelGroup import LabelGroup
from UITest.pages.IndexPage import IndexPage


class PeopleManagePage(IndexPage):
    org_select_open = El('部门选择', css='#select .ant-select-selection')
    com_select_open = El('编制类型', css='#compile .ant-select-selection')
    job_select_open = El('工作状态', css='#jobtype .ant-select-selection')
    search_input = El('人员查询输入框', css='[placeholder="查询姓名或身份证号"]')
    search_btn = El('查询按钮', x="//*[text()='查询']/parent::button")

    def query_people(self, o_name="", c_type="", j_type="", p_name_or_id=""):
        """
        查询人员
        @param o_name:
        @param c_type:
        @param j_type:
        @param p_name_or_id:
        @return:
        """
        _select_something(self, self.org_select_open, o_name)
        _select_something(self, self.com_select_open, c_type)
        _select_something(self, self.job_select_open, j_type)
        self.search_input.send_keys(p_name_or_id)
        self.search_btn.click()


def _select_something(self, el, val):
    if val:
        el.click()
        _s_id = el.get_attribute("aria-controls")
        DropDownBox(self.find_element(id=_s_id), el).select(val)


def _label_xpath_drop(name):
    return f'//label[contains(text(),"{name}")]/following-sibling::div//div[@aria-controls]'


def _label_xpath_input(name):
    return f'//label[contains(text(),"{name}")]/following::input'


class NewPeoplePage(IndexPage):
    com_type_box = El("编制类型", x='//*[contains(text(),"编制类型")]/parent::div')
    fullname = El("姓名输入框", x=_label_xpath_input("姓名"))
    id_num = El("身份证号输入框", css=_label_xpath_input("身份证号"))
    gender_box = El("性别选择框", x='//*[contains(text(),"性别")]/parent::div')
    marriage_box = El("婚否选择框", x='//*[contains(text(),"婚否")]/parent::div')

    bth_input_open = El("生日输入框激活器", mode="I", css=".ant-calendar-picker-input")
    bth_input = El("生日输入框", mode="I", css="div.ant-calendar-input-wrap input")

    ethnic_open = El("民族选择框", x=_label_xpath_drop("民族"))
    email_input = El("邮箱", x=_label_xpath_input("邮箱"))
    office_phone = El("办公电话", x=_label_xpath_input("办公电话"))
    contact_phone = El("联系电话", x=_label_xpath_input("联系电话"))

    def choose_compilation_type(self, c_name):
        LabelGroup(self.com_type_box).select_label(c_name)

    def input_base_info(self,info_dict):
        """

        @param info_dict:
            {
            name="",
            id_num="",
            gender="",
            marriage="",
            bth_day="",
            ethnic="",
            email="",
            office_phone="",
            contact_phone="",
        }
        @return:
        """
        pass

    def input_other_info(self,):
        pass