from UITest.common.page_control import BaseControl


class LabelGroup(BaseControl):

    def select_label(self, val):
        if val:
            loc = f".//label[string()='{val}']"
            self.action.click(x=loc)
        return self
