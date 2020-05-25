from UITest.common.locator import get_locator
from UITest.controls.Table import Table


class DivTable(Table):
    """获取表格类数据"""

    def __init__(self, el, title_loc: dict, row_loc: dict, cell_loc: dict):
        """

        :param el: 表格最上级元素
        :param title_loc: 能够定位到title的定位器符合locator_dict
        :param row_loc: 定位到数据行
        :param cell_loc: 由数据行定义去查询格子的定义
        备注推荐全部使用xpath定位，或者css子级定位器定位。避免出现奇怪的定位错误
        """
        super().__init__(el)
        self.title_loc = title_loc
        self.row_loc = row_loc
        self.cell_loc = get_locator(cell_loc)

    @property
    def data(self):
        ret = []
        for row in self._trs:
            tds = row.find_elements(*self.cell_loc)
            ret.append([td.text for td in tds])
        return ret

    @property
    def _trs(self):
        return self.action.find_elements(**self.row_loc)

    @property
    def _ths(self):
        return self.action.find_elements(**self.title_loc)
