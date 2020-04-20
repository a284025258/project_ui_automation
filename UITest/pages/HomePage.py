import allure
from poium import PageElement

from UITest.pages.BasePage import BasePage
from UITest.pages.IndexPage import IndexPage


class HomePage(BasePage):
    examination_management_system = PageElement(describe='考务综合管理平台', xpath="//font[text()='考务综合管理平台']")
    logout_button = PageElement(describe='登出按钮', xpath="//font[text()='安全退出']")
    sys_search_input_box = PageElement(describe='系统搜索框输入框', xpath="//input[@placeholder='系统名称']")
    sys_search_button = PageElement(describe="系统搜索框搜索按钮", css="svg.icon.yh-search-svg > use")

    def search_sys(self, sys_name):
        self.logger.info("搜索名为》{}《的系统".format(sys_name))
        self.sys_search_input_box.clear()
        self.sys_search_input_box.send_keys(sys_name)
        self.sys_search_button.click()
        return self

    def into_EMS(self):
        with allure.step("切换到EMS"):
            self.examination_management_system.click()
            self.logger.info("切换window handle")
            self.switch_to_window(self.new_window_handle)
            return IndexPage(self.driver)

