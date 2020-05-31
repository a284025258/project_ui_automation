import logging

import allure

from UITest.common.po_base import El
from UITest.controls.DropDownBox import DropDownBox
from UITest.controls.Table import Table
from UITest.pages.IndexPage import IndexPage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DeviceInfoManagePage(IndexPage):
    __page_name = "设备信息管理"

    def switch_tab(self, tab_name):
        tabs = {
            "设备信息管理": DeviceInfoManageTab,
            "设备管理日志": DeviceManageLogTab
        }
        self.click(x=f"//*[@id='ul_device']//a[text()='{tab_name}']")


class DeviceInfoManageTab(DeviceInfoManagePage):
    """设备信息管理tab页"""
    _table = El("设备表格", css="table")
    device_category_selection_box_opener = El("设备类别选择框触发", css='//*[@data-id="DtCode"]')
    device_category_selection_box = El("设备类别选择框", css='//*[@data-id="DtCode"]/following-sibling::div/ul')

    association_status_opener = El("关联状态触发", css='//*[@data-id="RelationStatus"]')
    association_status_selection_box = El("关联状态选择框", css='//*[@data-id="RelationStatus"]/following-sibling::div/ul')
    query_btn = El("查询按钮", css="#btnQuery")

    search_input = El("搜索框", css="#deviceSearch")
    search_btn = El("搜索按钮", css="#btnSearch")

    @property
    def info_compliance(self):
        """
        信息合规
        :return: bool
        """
        dev_type = self._device_category_selection.value
        status = self._association_status_selection.value
        table_status = set(self.table["关联状态"])
        table_types = set(self.table["设备类别"])
        logger.info(f"选择的设备类别:{dev_type}")
        logger.info(f"选择的关联状态:{status}")
        logger.info(f"表格中的设备类别set:{table_status}")
        logger.info(f"表格中的设备类别set:{table_types}")
        # 192.168.170.160
        if dev_type == "全部" and status == "全部":
            return True
        elif dev_type == "全部":
            return status in table_status
        elif status == "全部":
            return dev_type in table_types
        else:
            return status in table_status and dev_type in table_types

    def search_dev(self, dev_name):
        """
        搜索设备代码/设备名称
        :type dev_name: str
        :param dev_name:
        :return: self
        """
        if dev_name:
            with allure.step(f"搜索设备代码/设备名称:{dev_name}"):
                self.search_input.send_keys(dev_name)
                self.search_btn.click()
        return self

    def query_dev(self, dev_info):
        """
        :type dev_info: dict
        :param dev_info:
        {
        "设备类别":"",
        "关联状态":"",
        }
        :return: self
        """
        dev_type = dev_info.get("设备类别", "")
        association_status = dev_info.get("关联状态", "")
        with allure.step(f"查询设备>>>设备类别:{dev_type},关联状态:{association_status}"):
            if dev_type:
                self._device_category_selection.select(dev_type)
            if association_status:
                self._association_status_selection.select(association_status)
            if dev_type or association_status:
                self.query_btn.click()
        return self

    @property
    def _device_category_selection(self):
        """设备类别"""
        return DropDownBox(self.device_category_selection_box, self.device_category_selection_box_opener)

    @property
    def _association_status_selection(self):
        """关联状态"""
        return DropDownBox(self.association_status_selection_box, self.association_status_opener)

    @property
    def table(self):
        """设备表格"""
        return Table(self._table)

    class AddDevicePage(IndexPage):
        """"""


class DeviceManageLogTab(DeviceInfoManagePage):
    """"""
