"""
通过一些方法选择元素列表中的元素
"""


class Selection:
    def __init__(self, els):
        if not els:
            raise TypeError("els' length must getter than 0")
        self.els = els

    @property
    def text_list(self):
        return [el.text for el in self.els]


class SelectByStr(Selection):

    def __call__(self, by):
        if isinstance(by, str):
            if by in self.text_list:
                return self.els[self.text_list.index(by)]
            raise ValueError("not support type {}".format(type(by)))


class SelectByIndex(Selection):
    def __call__(self, by):
        if isinstance(by, int):
            return self.els[by]
        raise ValueError("not support type {}".format(type(by)))


def select_el(els, by):
    if isinstance(by, str):
        SelectByStr(els)(by)
    elif isinstance(by, int):
        SelectByIndex(els)(by)
    raise ValueError("not support type {}".format(type(by)))