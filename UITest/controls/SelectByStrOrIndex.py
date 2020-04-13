from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class SelectByStrOrIndex:

    def __init__(self, el, inner_locator, _text_filter=None):
        self._el = el
        self._locator = inner_locator
        self._filter = _text_filter

    @property
    def el_list(self):
        _el_list = self._el.find_elements(*self._locator)
        if self._locator is not None:
            _el_list = [_el for _el in _el_list if _el.text != self._filter]
        return _el_list

    def select_by(self, by) -> WebElement:
        if isinstance(by, int):
            return self._select_by_index(by)
        elif isinstance(by, str):
            return self._select_by_str(by)
        else:
            raise TypeError("只支持str和int作为输入")

    def _select_by_index(self, by):

        try:
            _el = self.el_list[by]
        except IndexError:
            raise NoSuchElementException("不存在第{}个选项".format(by))
        else:
            return _el

    def _select_by_str(self, by):

        try:
            index = self.el_list.index(by)
            _el = self.el_list[index]
        except ValueError:
            raise NoSuchElementException("不存在{}选项".format(by))
        else:
            return _el
