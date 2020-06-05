"""
统一资源管理->物理场所管理
"""
import logging
from time import sleep

import allure

from UITest.common.po_base import El
from UITest.controls.Table import Table
from UITest.pages.IndexPage import IndexPage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LocationManagePage(IndexPage):
    """场所管理主界面"""
    __page_name = "物理场所管理"
    site_building_management_button = El("场所建筑管理按钮", lt='场所建筑管理')
    add_site_button = El("新增场所按钮", lt='新增场所')

    def click_site_building_management_button(self):
        """点击场所建筑管理按钮"""
        self.site_building_management_button.click()
        return SiteBuildingmManagement(self)

    def click_add_site_button(self):
        """新增场所按钮"""
        self.add_site_button.click()
        return SiteManagement(self)


class SiteBuildingmManagement(IndexPage):
    """场所建筑管理"""

    save_btn = El("保存按钮", x='//button[string()="保 存"]')
    com_btn = El("确定按钮", css='#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a')
    back_btn = El("返回按钮", lt='返 回')

    _table = El("建筑表", css="table")

    @property
    def table(self):
        sleep(1)
        return Table(self._table)

    def __get_input(self, label_name):
        return self.find_element(x=f"(//label[contains(string(),'{label_name}')]/following-sibling::div/*)[1]")

    def add_build(self, build_info):
        """
        添加建筑
        :type build_info: list or dict
        :param build_info:
        {"建筑名称":"","楼层总数":""}
        or
        [{"建筑名称":"","楼层总数":""}, {"建筑名称":"","楼层总数":""}]
        :return:
        """

        def _add_build(_build_info):
            """
            添加一个建筑
            :param _build_info: {"建筑名称":"","楼层总数":""}
            :return:
            """
            for k, v in _build_info.items():
                el = self.__get_input(k)
                el.clear()
                el.send_keys(v)
            self.save_btn.click()
            self.com_btn.click()

        if isinstance(build_info, list):
            for info in build_info:
                _add_build(info)
        elif isinstance(build_info, dict):
            _add_build(build_info)
        else:
            raise TypeError(f"add_build only use dict or list, not type:{type(build_info)}:{build_info}")
        return self

    def back(self):
        self.back_btn.click()
        return LocationManagePage(self)


class SiteManagement(IndexPage):
    """场所管理页面"""
    room_information_input_box = El("房间信息输入框", css='#Name')
    test_room_capacity_input_box = El("考场容量输入框", css='#RoomCap')
    duty_phone_input_box = El("值班电话输入框", css='#ContactTel')
    save_btn = El("保存按钮", x='//button[text()="保 存"]')
    back_btn = El("返回按钮", lt='返 回')
    fast_add_btn = El("快速新增", x="//*[text()='快速新增']")
    # 提示框
    msg = El("弹出框信息", css=".layui-layer-content")
    confirm_btn = El("确定按钮", mode="I", lt='确定')
    cancel_btn = El("取消按钮", css='.layui-layer-close')

    def add_site(self, site_info, fast=False):
        """
        添加场所
        :param fast: 快速添加
        :param site_info:
        {
        "场所类型":"","场所名称":"","楼层":"","房间信息":"",
        "考场容量":"","值班电话":""
        "默认座次":""
        }
        场所类型:
        请选择场所类型, 标准化考场, 试卷保管室, 考务办公室,
        视频监考室, 语音播放室, 试卷流转通道, 普通考场,
        试卷保密室, 考务指挥中心, 其他,
        :return:
        """
        with allure.step("快速添加场所" if fast else "添加场所"):
            # 必填
            self._drop_dwon_box_select_by("PtCode", site_info["场所类型"])
            self._drop_dwon_box_select_by("BuildingId", site_info["场所名称"])
            self._drop_dwon_box_select_by("BuildingFloors", site_info["楼层"])
            self.room_information_input_box.send_keys(site_info["房间信息"])
            # 普通考场-考场容量
            if site_info["场所类型"] == "普通考场":
                self.test_room_capacity_input_box.send_keys(str(site_info.get("考场容量", 30)))
            # 值班电话
            if site_info["场所类型"] in ["试卷保管室", "考务办公室", "视频监考室", "语音播放室", "试卷保密室", "考务指挥中心", "其他"]:
                tel = str(site_info.get("值班电话", ""))
                self.duty_phone_input_box.send_keys(tel)
            # 标准化考场-默认座次
            if site_info["场所类型"] == "标准化考场":
                self._drop_dwon_box_select_by('DefaultseattingWay', site_info.get("默认座次", 8877))

            if fast:
                self.fast_add_btn.click()
                logger.info(f"弹出框信息为:{self.msg.text}")
                self.confirm_btn.click()
                return self
            else:
                self.save_btn.click()
                logger.info(f"弹出框信息为:{self.msg.text}")
                self.confirm_btn.click()

                return self

    def _drop_dwon_box_select_by(self, drop_dwon_box_name, by_val):
        """
        此界面下拉框选择框实现
        :param drop_dwon_box_name: 下拉框的data-id属性对应的值
        :param by_val: li标签的值
        :return:
        """
        _el = self.find_element(mode="V", x=f"//button[@data-id='{drop_dwon_box_name}']/parent::div")
        _el.click()
        _el.find_element_by_xpath(f".//li[string()='{by_val}']").click()
