from UITest.controls.DropDownBox import DropDownBox


class TreeDropDownBox(DropDownBox):
    """
    树形下拉框
    """

    def select(self, org_name):
        """通过名称选择机构"""
        self.open_check()
        val = f'a[title*="{org_name}"]'
        self.action.click(css=val)
        return self

    def open(self, org_name):
        """展开机构树的下拉框"""
        self.open_check()
        val = f'.//a[contains(@title,"{org_name}") and @class]/preceding-sibling::span'
        self.action.click(x=val)
        return self

    def select_by_list(self,a_list):
        """
        通过列表选择,默认列表传入时最后一个为选择对象，前面的都作为展开
        :param a_list:
        :return:
        """
        if a_list:
            tag = True
            for index, org_type in enumerate(a_list, 1):
                if index == len(a_list):
                    tag = False
                self.open(org_type) if tag else self.select(org_type)
            return True
        return False
