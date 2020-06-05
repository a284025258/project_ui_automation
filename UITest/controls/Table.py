import logging
from time import sleep

from selenium.webdriver.common.by import By

from UITest.common.page_control import BaseControl

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Table(BaseControl):
    """获取表格类数据"""

    def get_row(self, info):
        """通过一个数据获取行数据"""
        sleep(0.5)
        logger.info(f"尝试获取行信息>>>{info}")
        for data in self.data:
            if info in data:
                logger.info(f"获取行信息>>>{data}")
                return data
        else:
            logger.error(f"获取行信息失败>>>None")
            return None

    @property
    def titles(self):
        """标题"""
        return [th.text for th in self._ths]

    @property
    def info(self):
        """
        返回表信息
        :return: {"title1":["info1","info2"],"title2":["info3","info4"]}
        """
        return dict(zip(self.titles, self.T_data))

    @property
    def data(self):
        """
        返回表信息
        :return: [["info1","info2"],
                ["info3","info4"]]
        """
        ret = []
        for row in self._trs:
            tds = row.find_elements(By.TAG_NAME, 'td')
            ret.append([td.text for td in tds])
        return ret

    @property
    def row(self):
        """行"""
        return len(self._trs)

    @property
    def col(self):
        """列"""
        return len(self._ths)

    @property
    def _trs(self):
        return self.action.find_elements(css="tr")[1:]

    @property
    def _ths(self):
        """Table headers webelement list"""

        tr = self.action.find_element(css='tr')
        ths = tr.find_elements_by_css_selector("th")
        if not ths:
            # 畸形表格适配
            ths = tr.find_elements_by_css_selector("td")
        return ths

    @property
    def T_data(self):
        return list(zip(*self.data))

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[item]
        elif isinstance(item, str):
            return self.info[item]
        else:
            raise TypeError("{0} indices must be integers or str not {1}"
                            .format(type(self), type(item)))
