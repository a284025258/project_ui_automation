import logging

import allure
from selenium.webdriver.common.keys import Keys

from UITest.common.po_base import El
from UITest.controls.DivTable import DivTable
from UITest.controls.DropDownBox import DropDownBox
from UITest.controls.LabelGroup import LabelGroup
from UITest.pages.IndexPage import IndexPage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PeopleManagePage(IndexPage):
    org_select_open = El('部门选择', css='#select .ant-select-selection')
    com_select_open = El('编制类型', css='#compile .ant-select-selection')
    job_select_open = El('工作状态', css='#jobtype .ant-select-selection')
    search_input = El('人员查询输入框', css='[placeholder="查询姓名或身份证号"]')
    search_btn = El('查询按钮', x="//*[text()='查询']/parent::button")
    _table = El("人员表格", css=".fyl-rygl-table")
    add_people_btn = El("人员新增", x='//button[string()="人员新增"]')

    def query_people(self, info):
        """
        查询人员
        :param info:
        {
            "部门":"","编制类型":"",
            "工作状态":"","人员":""
        }
        :return:
        """

        _select_something(self, self.org_select_open, info.get("部门"))
        _select_something(self, self.com_select_open, info.get("编制类型"))
        _select_something(self, self.job_select_open, info.get("工作状态"))
        # todo 身份证校验，目前只有名字校验
        self.search_input.send_keys(info.get("人员", ""))
        self.search_btn.click()
        self.screenshot_in_allure(f"查询人员：查询条件>>>{info}")
        return self

    def click_add_people_btn(self):
        self.add_people_btn.click()
        return NewPeoplePage(self)

    @property
    def table(self):
        return DivTable(self._table,
                        {"x": "./div[1]/div"},
                        {"x": ".//*[@class='fyl-rygl-table-list']"},
                        {"x": "./div"})

    @property
    def info_compliance(self):
        """
        表格中数据合规
        即部门对应，编制类型对应，工作状态对应，人员对应
        :return:
        """
        result = self._department_name_same and self._com_type_same and self._job_type_same and self._search_input_same
        if not result:
            logger.error(f"结果不同表中信息为：\n {self.table.info}")
            self.screenshot_in_allure("结果不同")

        return result

    @property
    def _department_name_same(self):
        """部门名称与表格中相同"""
        if self.org_select_open.text == "全部":
            return True
        else:
            for dep in self.table["部门名称"]:
                if self.org_select_open.text != dep:
                    return False
            else:
                return True

    @property
    def _com_type_same(self):
        """编制类型与表格中相同"""
        if self.com_select_open.text == "全部":
            return True
        else:
            for dep in self.table["编制类型"]:
                if self.com_select_open.text != dep:
                    return False
            else:
                return True

    @property
    def _job_type_same(self):
        """工作状态与表格中相同"""
        if self.job_select_open.text == "全部":
            return True
        else:
            for dep in self.table["工作状态"]:
                if self.job_select_open.text != dep:
                    return False
            else:
                return True

    @property
    def _search_input_same(self):
        """搜索框与表格中相同"""
        val = self.search_input.get_attribute("value")
        if val == "":
            return True
        else:
            for i in self.table["姓名"]:
                if val not in i:
                    return False
            else:
                return True


def _select_something(self, el, val):
    """这个页面选择控件的代理选择的实现"""
    # todo 抽取到控件中去
    if val:
        el.click()
        _s_id = el.get_attribute("aria-controls")
        DropDownBox(self.find_element(mode="V", id=_s_id), el).select(val)


def _label_xpath_drop(name):
    return f'//label[contains(string(),"{name}")]/following-sibling::div//div[@aria-controls]'


def _label_xpath_input(name):
    return f'//label[contains(string(),"{name}")]/following::input'


class NewPeoplePage(IndexPage):
    com_type_box = El("编制类型", x='//*[contains(text(),"编制类型")]/parent::div')
    fullname = El("姓名输入框", x=_label_xpath_input("姓名"))
    id_num = El("身份证号输入框", x=_label_xpath_input("身份证号"))
    gender_box = El("性别选择框", x='//*[contains(text(),"性别")]/parent::div')
    marriage_box = El("婚否选择框", x='//*[contains(text(),"婚否")]/parent::div')
    bth_input_open = El("生日输入框激活器", mode="I", css=".ant-calendar-picker-input")
    ethnic_open = El("民族选择框", x=_label_xpath_drop("民族"))
    email_input = El("邮箱", x=_label_xpath_input("邮箱"))
    office_phone = El("办公电话", x=_label_xpath_input("办公电话"))
    contact_phone = El("联系电话", x=_label_xpath_input("联系电话"))
    uploadimg_input = El("上传照片框", css="#uploadimg")
    # 其他信息
    # 在编、聘用
    department_box = El("正式_借调_临时_部门选择框", x=_label_xpath_drop("部门"))
    position_box = El("职务输入框", x=_label_xpath_input("职务"))
    education_box = El("学历选择框", x=_label_xpath_drop("学历"))
    degree_box = El("学位选择框", x=_label_xpath_drop('学位'))
    job_title_box = El("职称选择框", x=_label_xpath_drop('职称'))
    political_status_box = El("政治面貌选择框", x=_label_xpath_drop('政治面貌'))
    # 临时、借调
    original_work_unit_box = El("原工作单位输入框", x=_label_xpath_input('原工作单位'))
    secondment_validity = El("借调有效期输入框激活器", x=_label_xpath_input("借调有效期"))
    # 保存按钮
    save_btn = El("保存按钮", x='//button[string()="保 存"]')

    def choose_compilation_type(self, c_name):
        """选择编制类型"""
        LabelGroup(self.com_type_box).select_label(c_name)
        return self

    @property
    def compilation_type(self):
        """选择的编制类型"""
        return self.com_type_box.find_element_by_css_selector(".ant-radio-wrapper-checked").text

    def upload_img(self, img_path):
        """上传照片"""
        self.uploadimg_input.send_keys(img_path)

    def input_base_info(self, info_dict):
        """
        填写基本信息
        :param info_dict:
        {
            "姓名": "", "身份证号": "", "性别": "",
            "婚否": "", "出生日期": "", "民族": "",
            "邮箱": "", "办公电话": "", "联系电话": "",
            "上传头像图片地址":""
        }
        :return: self
        """
        with allure.step("填写基本信息"):
            self.fullname.send_keys(info_dict["姓名"])
            self.id_num.send_keys(info_dict["身份证号"])
            # 前端做了自动识别 性别 出生日期不需要手动填写，如果需要改的话传值需符合规范
            LabelGroup(self.gender_box).select_label(info_dict["性别"])
            LabelGroup(self.marriage_box).select_label(info_dict["婚否"])
            self.bth_input_open.click()
            self._input_time(info_dict["出生日期"])
            _select_something(self, self.ethnic_open, info_dict["民族"])
            self.email_input.send_keys(info_dict["邮箱"])
            self.office_phone.send_keys(info_dict["办公电话"])
            self.contact_phone.send_keys(info_dict["联系电话"])
            self.upload_img(info_dict["上传头像图片地址"])
            self.screenshot_in_allure("填写基本信息")
        return self

    def _input_time(self, t):
        """当前页面的输入时间实现"""
        self.find_element(css=".ant-calendar-date-input-wrap input").send_keys(t + Keys.ENTER)

    def input_other_info(self, info_dict):
        """
        输入其他信息
        :param info_dict:
        {
            "部门": "", "学历": "", "职务": "",
            "学位": "", "职称": "", "政治面貌": "",
            # 借调、临时人员独有
            "原工作单位": "", "借调有效期": "",
        }
        :return:
        """
        with allure.step("填写其他信息"):
            _select_something(self, self.department_box, info_dict["部门"])
            _select_something(self, self.education_box, info_dict["学历"])
            self.position_box.send_keys(info_dict["职务"])
            _select_something(self, self.degree_box, info_dict["学位"])
            _select_something(self, self.job_title_box, info_dict["职称"])
            _select_something(self, self.political_status_box, info_dict["政治面貌"])

            if self.compilation_type in ["在编", "聘用"]:
                pass
            elif self.compilation_type in ["借调"]:
                self.original_work_unit_box.send_keys(info_dict["原工作单位"])
                self.secondment_validity.click()
                self._input_time(info_dict["借调有效期"])
            elif self.compilation_type in ["临时"]:
                self.original_work_unit_box.send_keys(info_dict["原工作单位"])

            self.screenshot_in_allure("填写其他信息")
        self.save_btn.click()
        return PeopleManagePage(self)
