from selenium.webdriver.remote.webelement import WebElement

from UITest.common.page_action import PageAction


class BaseControl:

    def __init__(self, el):
        self._el: WebElement = el
        self.action = PageAction(el, 2)
