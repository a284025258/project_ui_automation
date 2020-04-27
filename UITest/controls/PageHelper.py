from UITest.controls.BaseControl import BaseControl


class PageHelper(BaseControl):
    """
    页码控件
    """

    @property
    def els(self):
        return self.el.find_element_by_css_selector("li")

    @property
    def next_page(self):
        """
        上一页
        @return:
        """
        return self.els[1]

    @property
    def last_page(self):
        """
        下一页
        @return:
        """
        return self.els[-1]

    def current_page(self):
        """
        当前页码
        @return:
        """
        _el = self.el.find_element_by_css_selector(".ant-pagination-item-active")
        return _el.text

    @property
    def page_msg(self):
        """

        @return: 显示的内容：如当前显示1-20条，共39条
        """
        return self.els[0].text

    def switch_to_page(self, page_num):
        # todo 切换页码，待数据足够再写
        pass
