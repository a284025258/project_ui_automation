from UITest.common.page_control import WapperControl


class DropDownBox(WapperControl):
    """下拉框"""



    def select(self, val):
        """通过名称选择机构"""
        self.open_check()
        val = f'.//*[text()="{val}"]'
        self.action.click(x=val)
