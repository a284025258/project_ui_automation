import allure

from UITest.common.faker_info import f
from UITest.common.po_base import El
from UITest.config import UploadImg
from UITest.controls.DivTable import DivTable
from UITest.controls.DropDownBox import DropDownBox
from UITest.controls.LabelGroup import LabelGroup
from UITest.pages.IndexPage import IndexPage
from common.utils.IDnumber import generate_ID


class PeopleManagePage(IndexPage):
    org_select_open = El('部门选择', css='#select .ant-select-selection')
    com_select_open = El('编制类型', css='#compile .ant-select-selection')
    job_select_open = El('工作状态', css='#jobtype .ant-select-selection')
    search_input = El('人员查询输入框', css='[placeholder="查询姓名或身份证号"]')
    search_btn = El('查询按钮', x="//*[text()='查询']/parent::button")
    _table = El("人员表格", css=".fyl-rygl-table")

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

    @property
    def table(self):
        return DivTable(self._table,
                        {"x": "./div[1]/div"},
                        {"x": ".//*[@class='fyl-rygl-table-list']"},
                        {"x": "./div"})

    @property
    def info_compliance(self):
        tag = True
        if not self.org_select_open.text == "全部":
            tag = self.org_select_open.text in  self.table.info["部门名称"]
        elif not self.com_select_open.text == "全部":
            pass


def _select_something(self, el, val):
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
    id_num = El("身份证号输入框", css=_label_xpath_input("身份证号"))
    gender_box = El("性别选择框", x='//*[contains(text(),"性别")]/parent::div')
    marriage_box = El("婚否选择框", x='//*[contains(text(),"婚否")]/parent::div')
    bth_input_open = El("生日输入框激活器", mode="I", css=".ant-calendar-picker-input")
    bth_input = El("生日输入框", mode="I", css="div.ant-calendar-input-wrap input")
    ethnic_open = El("民族选择框", x=_label_xpath_drop("民族"))
    email_input = El("邮箱", x=_label_xpath_input("邮箱"))
    office_phone = El("办公电话", x=_label_xpath_input("办公电话"))
    contact_phone = El("联系电话", x=_label_xpath_input("联系电话"))
    uploadimg_input = El("上传照片框", css="#uploadimg")
    # 其他信息
    # 在编、聘用
    department_box = El("部门选择框", x=_label_xpath_drop("部门"))
    job_title_box = El("职务输入框", x=_label_xpath_input("职务"))
    education_box = El("学历选择框", x=_label_xpath_drop("学历"))
    degree_box = El("学位选择框", x=_label_xpath_drop('学位'))
    职称_box = El("职称选择框", x=_label_xpath_drop('职称'))
    政治面貌_box = El("政治面貌选择框", x=_label_xpath_drop('政治面貌'))
    # 借调
    原工作单位_box = El("原工作单位输入框", x=_label_xpath_input('原工作单位'))
    借调部门_box = El("借调部门选择框", x=_label_xpath_drop('借调部门'))

    def choose_compilation_type(self, c_name):
        """选择编制类型"""
        LabelGroup(self.com_type_box).select_label(c_name)

    @property
    def compilation_type(self):
        """选择的编制类型"""
        return self.com_type_box.find_element_by_css_selector(".ant-radio-wrapper-checked").text

    def upload_img(self):
        """上传照片"""
        self.uploadimg_input.send_keys(UploadImg)

    def input_base_info(self, info_dict):
        """
        填写基本信息
        @param info_dict:
        {
            "姓名": "", "身份证号": "", "性别": "",
            "婚否 ": "", "出生日期": "", "民族": "",
            "邮箱": "", "办公电话": "", "联系电话": "",
        }
        @return: self
        """
        with allure.step("输入基本信息"):
            self.fullname.send_keys(info_dict.get("姓名") or f.name())
            self.id_num.send_keys(info_dict.get("身份证号") or generate_ID())
            # 前端做了自动识别 性别 出生日期不需要手动填写，如果需要改的话传值需符合规范
            LabelGroup(self.gender_box).select_label(info_dict.get("性别") or "")
            LabelGroup(self.marriage_box).select_label(info_dict.get("婚否") or "")
            # todo 生日输入逻辑
            info_dict.get("出生日期", "")
            _select_something(self, self.ethnic_open, info_dict.get("民族") or "汉族")
            self.email_input.send_keys(info_dict.get("邮箱") or f.email())
            self.office_phone.send_keys(info_dict.get("办公电话") or f.phone_number())
            self.contact_phone.send_keys(info_dict.get("联系电话") or f.phone_number())
        return self

    def input_other_info(self, info_dict):
        if self.compilation_type in ["在编", "聘用"]:
            pass
