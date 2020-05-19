from selenium.webdriver.remote.webelement import WebElement

from UITest.common.page_control import BaseControl


class DropDownBox(BaseControl):
    """下拉框"""

    def __init__(self, el, opener: WebElement):
        """
        @param el: 下拉框体
        @param opener: 激活框
        """
        super().__init__(el)
        self.opener = opener

    @property
    def value(self):
        """
        返回下拉框的值
        @return: text > value > placeholder
        """
        ga = self.opener.get_attribute
        return self.opener.text or ga("value") or ga("placeholder")

    def open_check(self):
        """可见性检查"""
        if not self._el.is_displayed():
            self.action.click(el=self.opener)

    def select(self, val):
        """通过名称选择机构"""
        self.open_check()
        val = f'.//*[text()="{val}"]'
        self.action.click(x=val)
