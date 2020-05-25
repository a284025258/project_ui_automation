from UITest.common.po_base import El, Els

from UITest.pages.exam_situation_manage.AllNoticePage import AllNoticePage


class MyNoticePage(AllNoticePage):
    del_btn = El("删除按钮", xpath="//span[text()='删除']")
    del_selector = Els("删除选择项", css="input.ant-checkbox-input")
    accept_btn = El("确认删除", css=".ant-btn")

    def select_to_del(self, *index):
        """

        :param index: 0:当前页全选，1-21为个数
        :return:
        """
        if 0 in index:
            self.del_selector[0].click()
        else:
            for i in index:
                self.del_selector[i].click()

    def do_del(self):
        if self.del_btn.is_enabled():
            self.del_btn.click()
        self.accept_btn.click()
        return self
