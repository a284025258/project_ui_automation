from selenium.common.exceptions import UnexpectedTagNameException
from selenium.webdriver.common.by import By


class Table:
    """获取表格类数据"""

    def __init__(self, webelement):
        if webelement.tag_name.lower() != "table":
            raise UnexpectedTagNameException(
                "Select only works on <table> elements, not on <%s>" %
                webelement.tag_name)
        self._el = webelement

    @property
    def row(self):
        return len(self._tr)

    @property
    def col(self):
        return len(self._th)

    @property
    def _tr(self):
        return self._el.find_elements(By.TAG_NAME, 'tr')[1:]

    @property
    def _th(self):
        """Table headers webelement list"""
        ths = self._el.find_elements(By.CSS_SELECTOR, 'th')
        return ths

    @property
    def titles(self):
        return [th.text for th in self._th]

    @property
    def data(self):
        """Table data"""
        ret = []
        for row in self._tr:
            tds = row.find_elements(By.TAG_NAME, 'td')
            ret.append(tds)
        return ret

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        elif isinstance(item, str):
            index = self.titles.index(item)
            return [i[index] for i in self.data]
        else:
            raise TypeError("{0} indices must be integers or str not {1}"
                            .format(type(self), type(item)))
