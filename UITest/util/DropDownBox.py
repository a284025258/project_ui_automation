from selenium.webdriver.remote.webelement import WebElement


class DropDownBox:
    """
    封装用于下拉框的API
    """

    def __init__(self, el: WebElement, desc="",switch_selector=None, is_open=False):
        """

        :param el: 页面元素
        :param desc: 描述
        :param switch_selector: 相对页面元素的选择器，需要反选父类可能需要用Xpath，不填则为元素本身
        :param is_open: 初始化时下拉框状态
        """
        self.describe = desc
        self.switch_selector = switch_selector
        self._el = el
        self._open = is_open

    @property
    def switch(self):
        if self.switch_selector:
            return self._el
        else:
            return self._el.find_element(self.switch_selector)

    def open_box(self):
        if not self._open:
            self.switch.click()

    def close_box(self):
        if self._open:
            self.switch.click()
