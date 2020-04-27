from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from UITest.controls.BaseControl import BaseControl


class DropDownBox(BaseControl):
    """
    单选下拉框控件,内部无多选
    """

    def __init__(self, el, inner_el_loc=None):
        super().__init__(el)
        if el.tag_name.lower() == "select":
            self.el = Select(el)
        if inner_el_loc is None:
            self.inner_el_loc = self.guess_inner()
        self.inner_el_loc = inner_el_loc
        self.inner_els = self.el.find_elements(*self.inner_el_loc)

    def guess_inner(self):
        if self.el.tag_name == "ul":
            return By.CSS_SELECTOR, "li"
        elif self.el.tag_name == "select":
            return By.CSS_SELECTOR, "option"

    @property
    def text_list(self):
        return [el.get_attribute('innerText') for el in self.inner_els]
