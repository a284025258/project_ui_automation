import logging

from poium import PageElement

from UITest.pages.BasePage import BasePage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class HomePage(BasePage):
    examination_management_system = PageElement(describe='考务综合管理平台', xpath="//font[text()='考务综合管理平台']")
    logout_button = PageElement(describe='登出按钮', xpath="//font[text()='安全退出']")
    sys_search_input_box = PageElement(describe='系统搜索框输入框', xpath="//input[@placeholder='系统名称']")
    sys_search_button = PageElement(describe="系统搜索框搜索按钮", css="svg.icon.yh-search-svg > use")

    def search_sys(self, sys_name):
        logger.info("搜索名为>>>{}的系统".format(sys_name))
        self.sys_search_input_box.clear()
        self.sys_search_input_box.send_keys(sys_name)
        self.sys_search_button.click()
        return self

    def click_system(self, sys_name):
        css = f'span[title="{sys_name}"]'
        el = self.driver.find_element_by_css_selector(css)
        el.click()
