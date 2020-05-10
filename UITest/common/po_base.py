import time
from typing import List, Dict, Optional

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

_Locators = {
    By.ID: ["id"],
    By.XPATH: ["xpath", "x"],
    By.LINK_TEXT: ["link_text", "lt"],
    By.PARTIAL_LINK_TEXT: ["partial_link_text", "plt"],
    By.NAME: ["name"],
    By.TAG_NAME: ["tag_name", "tag"],
    By.CLASS_NAME: ["class_name", "class"],
    By.CSS_SELECTOR: ["css_selector", "css"],
}


def get_locators(_) -> Dict[str, str]:
    result = {}
    for key, values in _.items():
        for value in values:
            result[value] = key
    return result


Locators = get_locators(_Locators)


def _get_locator(_var):
    return Locators[_var[0]], _var[1]


class Page:
    def __init__(self, driver_or_page, time_out=5):
        if isinstance(driver_or_page, Page):
            driver = driver_or_page.driver
        else:
            driver = driver_or_page
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, time_out)
        self._action_chains = ActionChains(self.driver)

    @property
    def action_chains(self):
        self._action_chains.reset_actions()
        return self._action_chains

    def find_element(self, by, value):
        """找到元素后会自动标记"""
        return self._find_element((by, value))

    def find_elements(self, by, value):
        """强化版查询元素，附加等待与元素标记"""
        return self._find_elements((by, value))

    def _find_element(self, locator, *, visible=False) -> WebElement:
        """
        查询元素,超时后会返回None
        @param locator: 定位器
        @param visible: 元素可见
        @return: WebElement
        """
        method = EC.visibility_of_element_located if visible else EC.presence_of_element_located
        el = self.wait.until(method(locator))
        self._mark(el)
        return el

    def _find_elements(self, locator, *, visible=False) -> List[WebElement]:
        """
        查询一组元素
        @param locator: 定位器
        @param visible: 元素可见
        :return: List[WebElement]
        """

        els: List[WebElement] = self.wait.until(EC.presence_of_all_elements_located(locator))
        if visible:
            els = [el.is_displayed() for el in els]
        for el in els:
            self._mark(el)
        return els

    def _mark(self, el):
        """
        标记元素
        @param el: 被标记的元素
        """
        mark_js = 'arguments[0].style.border="2px solid red"'
        try:
            self.driver.execute_script(mark_js, el)
        except Exception:
            pass

    def hover(self, hover_el):
        """
        悬停
        @param hover_el: 被悬停的元素,元素需要可见
        """
        self.action_chains.move_to_element(hover_el).perform()

    def switch_to_frame(self, locator=None, switch_out=True):
        """
        切换frame
        @param locator: 为空则默认切换到第一个frame
        @param switch_out: 切换前先切换到最上级，默认开启
        """
        if switch_out:
            self.driver.switch_to.default_content()
        if locator is None:
            locator = 1
        return self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

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
        alert = self.wait.until(EC.alert_is_present())
        if keys_to_send is not None:
            alert.send_keys(keys_to_send)
            alert.accept()
        else:
            alert.accept() if accept else alert.dismiss()

    def scroll(self, x=0, y=0, *, el=None):
        """
        滚动屏幕
        @param x:
        @param y:
        @param el:
        @return:
        """
        if el is None:
            scroll_js = f"window.scrollBy({x},{y})"
            self.driver.execute_script(scroll_js)
        else:
            scroll_js = f"arguments[0].scrollBy({x},{y})"
            self.driver.execute_script(scroll_js, el)

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

    def __init__(self, describe, time_out=0, visible=False, **locator):
        if len(locator) != 1:
            raise ValueError("There must be one and only one locator in your init")
        self.describe = describe
        self._time_out = time_out
        self.locator = _get_locator(locator.popitem())
        self._visible = visible

    @property
    def method(self):
        return EC.visibility_of_element_located if self._visible else EC.presence_of_element_located

    def find_el(self, instance, owner) -> WebElement:
        if self._time_out:
            el = WebDriverWait(instance.driver, self._time_out).until(self.method(self.locator))
        else:
            el = instance.find_element(*self.locator)
        return el

    def __get__(self, instance, owner):
        if not isinstance(instance, Page):
            raise ValueError("need use in a Page-like Object")
        return self.find_el(instance, owner)


class Els(El):

    def find_el(self, instance, owner) -> List[WebElement]:
        if self._time_out:
            els = WebDriverWait(instance.driver, self._time_out).until(self.method(self.locator))
        else:
            els = instance.find_elements(*self.locator)
        return els

    @property
    def method(self):
        return EC.visibility_of_all_elements_located if self._visible else EC.presence_of_all_elements_located


if __name__ == '__main__':
    def xixi(*, haha=""):
        print(haha)


    xixi(haha="lskahjflskj")
