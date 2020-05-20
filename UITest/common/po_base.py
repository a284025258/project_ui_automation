"""
@author Ymangz

"""
from time import sleep
from typing import List

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from UITest.common.page_action import PageAction
from UITest.config import Start_Url


class Page:

    def __init__(self, driver_or_page):
        if isinstance(driver_or_page, Page):
            driver = driver_or_page.driver
        else:
            driver = driver_or_page
        self.action = PageAction(driver)
        self.driver: WebDriver = driver

    def click(self, el=None, *, force=False, **locator):
        return self.action.click(el=el, force=force, **locator)

    @property
    def pm(self):
        """
        页面管理
        @return: pm对象
        """
        from UITest.common.page_manage import pm
        return pm

    def _clear_cache(self):
        """chrome清除缓存，返回登陆界面"""
        self.driver.get("chrome://settings/privacy")
        # 打开清除缓存界面
        # shadow-root 解决   https://developer.mozilla.org/zh-CN/docs/Web/API/Element/shadowRoot
        sleep(0.5)
        self.driver.execute_script(
            """document.querySelector('settings-ui').shadowRoot.querySelector('#main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector("#basicPage settings-section[section='privacy'] settings-privacy-page").shadowRoot.querySelector('#pages div #clearBrowsingData').click()""")
        sleep(0.5)
        self.driver.execute_script(
            """document.querySelector('settings-ui').shadowRoot.querySelector('#main').shadowRoot.querySelector('settings-basic-page').shadowRoot.querySelector("#basicPage settings-section[section='privacy'] settings-privacy-page").shadowRoot.querySelector('settings-clear-browsing-data-dialog').shadowRoot.querySelector('#clearBrowsingDataConfirm').click()""")
        self.driver.get(Start_Url)

    def find_element(self, *, mode="L", **locator):
        """找到元素后会自动标记"""
        return self.action.find_element(mode=mode, **locator)

    def find_elements(self, *, mode="L", **locator):
        """强化版查询元素，附加等待与元素标记"""
        return self.action.find_elements(mode=mode, **locator)

    def hover(self, hover_el=None, **locator):
        """
        悬停
        @param hover_el: 被悬停的元素,元素需要可见
        """
        return self.action.hover(el=hover_el, **locator)

    def switch_to_frame(self, locator=None, switch_out=True):
        """
        切换frame
        @param locator: 为空则默认切换到第一个frame
        @param switch_out: 切换前先切换到最上级，默认开启
        """
        if switch_out:
            self.driver.switch_to.default_content()
        if locator is None:
            locator = 0
        return self.action.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def switch_to_new_window(self, auto_close=False):
        """
        切换到新窗口
        @param auto_close: 为真则关闭当前页面后切换
        """
        if auto_close:
            self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_alter(self, accept=True, keys_to_send=None):
        """
        切换到弹框
        @param accept: 若为真则接受，若为假则取消
        @param keys_to_send: 若存在则输入后确认
        """
        alert = self.action.wait.until(EC.alert_is_present())
        if keys_to_send is not None:
            alert.send_keys(keys_to_send)
            alert.accept()
        else:
            alert.accept() if accept else alert.dismiss()

    def screenshot_in_allure(self, step_name="运行快照"):
        """
        添加屏幕截图
        @param step_name: 步骤名
        """
        try:
            allure.attach(self.driver.get_screenshot_as_png(), step_name, allure.attachment_type.PNG)
        except Exception:
            pass


class El:

    def __init__(self, describe, *, instance=None, time_out=0, mode="L", **locator):
        self.instance = instance
        self.describe = describe
        self._time_out = time_out
        self.mode = mode
        self.locator = locator

    @property
    def el(self):
        if not isinstance(self.instance, Page):
            raise ValueError("BadUsage: need init with a Page-like Object")
        return self.__get__(self.instance, type(self.instance))

    def __get__(self, instance, owner) -> WebElement:
        if not isinstance(instance, Page):
            raise ValueError("need use in a Page-like Object\nEl(instance=driver)")

        if self._time_out:
            with instance.action.SetPageActionTime(instance.action, self._time_out) as action:
                el = action.find_element(mode=self.mode, **self.locator)
            return el

        el = instance.action.find_element(mode=self.mode, **self.locator)
        return el


class Els(El):

    def __get__(self, instance, owner) -> List[WebElement]:
        if not isinstance(instance, Page):
            raise ValueError("need use in a Page-like Object")
        if self._time_out:
            with instance.action.SetPageActionTime(instance.action, self._time_out) as action:
                els = action.find_elements(mode=self.mode, **self.locator)
            return els
        els = instance.action.find_elements(mode=self.mode, **self.locator)
        return els


if __name__ == '__main__':
    pass
