from poium import PageElement
from selenium.webdriver.common.by import By

from UITest.util.SelectByStrOrIndex import SelectByStrOrIndex


class IndexPageMaxIn:
    top_menu = PageElement(describe="顶部菜单栏", css="#root > section > header > ul")
    org_info = PageElement(describe="机构信息", css="header > div.xt-uinfo > span:nth-child(1) > font > font")
    user_info = PageElement(describe="右上角用户信息", css="span.ant-dropdown-trigger > font")
    user_info_drop_down = PageElement(describe="下拉菜单", css="body > div:nth-child(9) > div > div")
    user_info_box = PageElement(describe="用户信息框", css=".ant-modal-content")
    aside_menu = PageElement(describe="侧边栏菜单栏", css="#root > section > section > aside > div")
    index_iframe = PageElement(describe="iframe定位器", css="iframe.xt-mainIframe")

    def _switch_in(self):
        try:
            self.driver.switch_to.frame(self.index_iframe)
        except BaseException:
            pass

    def choice_user_drop_down_menu(self, by):
        """
        通过菜单名或者index来选择右上角的菜单
        :param menu_name:
        :return:
        """
        self.hover(self.user_info)
        _el = SelectByStrOrIndex(self.user_info_drop_down, (By.CSS_SELECTOR, "ul > li")).select_by(by)
        _el.click()

    def select_top_menu(self, by):
        """
        通过输入的顶部菜单名称或者index来选择菜单
        :param by:
        :return:
        """
        self.driver.switch_to.default_content()
        _el = SelectByStrOrIndex(self.top_menu, (By.CSS_SELECTOR, "li"), "···").select_by(by)
        _el.click()

    def select_aside_menu(self, menu_name_list):
        """
        通过传入的名称列表选择对应菜单，如：
        ["物理场所管理","考场"]，则会选择<物理场所管理>再选择<考场>
        :param menu_name_list:
        :return:
        """
        self.driver.switch_to.default_content()
        menu = self.aside_menu
        for name in menu_name_list:
            _el = SelectByStrOrIndex(menu, (By.CSS_SELECTOR, "ul > li")).select_by(name)
            _el.click()
            sleep(0.5)
            menu = _el
        self._switch_in()

    @property
    def user_verbose_info(self):
        """
        返回用户详细信息
        #个人信息\n用户账号\n45\n用户姓名\n完美\n所属机构\n广西省考试院\n身份证号\n110101199003078312\n用户角色\n系统管理员\n手机号码\n保存
        :return:
        """
        # self.user_info_box.text.split("\n")[1:-1]

        return [""] if self.user_info_box is None else self.user_info_box.text.split("\n")[1:-1]
