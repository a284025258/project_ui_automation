from UITest.common.page_actions import click
from UITest.controls.DropDownBox import DropDownBox


class TreeDropDownBox(DropDownBox):
    """
    树形下拉框
    """



    def select(self, org_name):
        """通过名称选择机构"""
        if not self.el.is_displayed():
            self.opener.click()
        val = f'a[title*="{org_name}"]'
        click(self.el, css=val)
        return self

    def open(self, org_name):
        """展开机构树的下拉框"""
        if not self.el.is_displayed():
            self.opener.click()
        val = f'//a[contains(@title,"{org_name}") and @class]/preceding-sibling::span'
        click(self.el, x=val)
        return self
