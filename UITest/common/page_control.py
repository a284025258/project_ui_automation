from selenium.webdriver.remote.webelement import WebElement

from UITest.common.page_action import PageAction


class BaseControl:

    def __init__(self, el):
        self._el: WebElement = el
        self.action = PageAction(el, 2)


class WapperControl(BaseControl):

    def __init__(self, el, opener):
        super().__init__(el)
        self.opener: WebElement = opener

    def open_check(self):
        """可见性检查"""
        if not self._el.is_displayed():
            self.action.click(el=self.opener)

    @property
    def value(self):
        """
        返回下拉框的值
        :return: text > value > placeholder
        """
        ga = self.opener.get_attribute
        text = self.opener.text or ga("value") or ga("placeholder")
        return text.strip()
