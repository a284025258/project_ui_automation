from UITest.common.page_control import BaseControl


class DropDownBox(BaseControl):
    """下拉框"""

    def __init__(self, el, opener):
        """
        @param el: 下拉框体
        @param opener: 激活框
        """
        super().__init__(el)
        self.opener = opener

    def select(self, val):
        pass
