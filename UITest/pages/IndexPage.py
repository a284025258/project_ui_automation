import logging

from poium import PageElement, PageElements

from UITest.pages.BasePage import BasePage
from UITest.pages.LoginPage import LoginPage
from UITest.pages.MaxIn.IndexPageMaxIn import UserInfoBox, PassWordChangeBox
from UITest.utils.selection import select_el

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class IndexPage(BasePage):
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

    def _switch_in(self):
        try:
            self.driver.switch_to.frame(self.index_iframe)
        except Exception as exc:
            logger.error(exc)
            pass

    def choice_user_drop_down_menu(self, by):
        """
        通过菜单名或者index来选择右上角的下拉菜单
        :param by:
        :return:
        """
        self.hover(self.user_info)
        el = select_el(self.user_info_drop_down, by)
        el.click()
        if by in ["个人信息", 0]:
            return UserInfoBox(self)
        elif by in ["修改密码", 1]:
            return PassWordChangeBox(self)
        elif by in ["安全退出", 2]:
            return LoginPage(self)

    def select_top_menu(self, by):
        """
        通过输入的顶部菜单名称或者index来选择菜单
        @param by:
        @return:
        """
        self.driver.switch_to.default_content()
        el = select_el(self.top_menu, by)
        el.click()
        return self

    def select_aside_menu(self, by):
        """
        通过传入的名称列表选择对应侧边菜单
        @param by:
        @return:
        """
        self.driver.switch_to.default_content()
        menu = select_el(self.aside_menu, by)
        menu.click()
        self._switch_in()
