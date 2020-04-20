from poium import PageElement, PageElements

from UITest.utils.selection import select_el


class IndexPageMaxIn:
    """
    对主页主要位置的封装，包括顶部菜单，用户信息，左侧菜单，个人信息框，修改密码框
    ---------------------------------------------
    |   ----------------------------------------|                                         |
    |   |                                       |
    |   |                                       |
    |   |           <非封装区域>                  |
    |   |                                       |
    |   |                                       |
    |   |                                       |
    ---------------------------------------------
    """
    # 顶部
    title = PageElement(describe="标题框", css="div.xt-title")
    top_menu = PageElements(describe="顶部菜单栏", css="header .ant-menu-item.ant-menu-item-only-child")
    user_info_box = PageElement(describe="用户信息框体", css=".xt-uinfo-name")
    org_info = PageElement(describe="机构信息", xpath="/font[1]", context=user_info_box)
    user_info = PageElement(describe="用户信息", xpath="/font[2]", context=user_info_box)
    user_info_drop_down = PageElements(describe="下拉菜单", css=".ant-dropdown.ant-dropdown-placement-bottomCenter li")
    # 侧边
    aside_menu = PageElements(describe="侧边栏菜单栏", css="aside li")
    # 主页面定位
    index_iframe = PageElement(describe="iframe定位器", css="iframe.xt-mainIframe")
    # 修改密码框
    change_password_box = PageElement(describe="密码修改框", css=".ant-modal-content")
    old_password_box = PageElement(describe="旧密码", id_="resetpwd_form_oldPwd")
    new_password_box = PageElement(describe="新密码", id_="resetpwd_form_newPwd")
    confirm_password_box = PageElement(describe="确认新密码", id_="resetpwd_form_confirmPwd")

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
        el = select_el(self.user_info_drop_down, by)
        el.click()

    def select_top_menu(self, by):
        """
        通过输入的顶部菜单名称或者index来选择菜单
        :param by:
        :return:
        """
        self.driver.switch_to.default_content()
        el = select_el(self.top_menu, by)
        el.click()

    def select_aside_menu(self, by):
        """
        通过传入的名称列表选择对应侧边菜单
        :param by:
        :return:
        """
        self.driver.switch_to.default_content()
        menu = select_el(self.aside_menu, by)
        menu.click()
        self._switch_in()

    def change_password(self, old, new):
        self.old_password_box.clear()
