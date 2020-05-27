"""
统一资源管理->物理场所管理
"""
from UITest.common.po_base import El
from UITest.pages.IndexPage import IndexPage


class LocationManagePage(IndexPage):
    """场所管理主界面"""
    __page_name = "物理场所管理"
    site_building_management_button = El("场所建筑管理按钮", lt='场所建筑管理')
    add_site_button = El("新增场所按钮", lt='新增场所')

    def click_site_building_management_button(self):
        self.site_building_management_button.click()
        return SiteBuildingmManagement(self)

    def click_add_site_button(self):
        self.add_site_button.click()
        return SiteManagement(self)


class SiteBuildingmManagement(IndexPage):
    """场所建筑管理"""
    建筑名称输入框 = El("建筑名称输入框", css='#BuildingName')
    楼层总数输入框 = El("楼层总数输入框", css='#BuildingFloors')
    保存按钮 = El("保存按钮", x='//button[string()="保 存"]')
    确定按钮 = El("确定按钮", css='#layui-layer1 > div.layui-layer-btn.layui-layer-btn- > a')
    返回按钮 = El("返回按钮", lt='返 回')

    def 新增建筑(self, name, floor=1):
        self.建筑名称输入框.send_keys(name)
        self.楼层总数输入框.clear()
        self.楼层总数输入框.send_keys(str(floor))
        self.保存按钮.click()
        self.确定按钮.click()
        return self

    def 返回场所列表(self):
        self.返回按钮.click()
        return LocationManagePage(self)


class SiteManagement(IndexPage):
    """场所管理页面"""
    room_information_input_box = El("房间信息输入框", css='#Name')
    test_room_capacity_input_box = El("考场容量输入框", css='#RoomCap')
    duty_phone_input_box = El("值班电话输入框", css='#ContactTel')
    save_btn = El("保存按钮", x='//button[text()="保 存"]')
    back_btn = El("返回按钮", lt='返 回')
    # 提示框
    confirm_btn = El("确定按钮", lt='确定')
    cancel_btn = El("取消按钮", css='.layui-layer-close')

    def input_site_info(self, site_info):
        """
        添加场所
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
        return self

    def click_save_btn(self):
        # todo 做到这里了，
        self.save_btn.click()
        self.confirm_btn.click()

    def _drop_dwon_box_select_by(self, drop_dwon_box_name, by_val):
        """
        此界面下拉框选择框实现
        :param drop_dwon_box_name: 下拉框的data-id属性对应的值
        :param by_val: li标签的值
        :return:
        """
        _el = self.find_element(mode="V", x=f"//button[@data-id='{drop_dwon_box_name}']/parent::div")
        _el.click()
        _el.find_element_by_xpath(f".//li[text()='{by_val}']").click()
