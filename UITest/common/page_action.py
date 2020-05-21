from time import sleep
from typing import List

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from UITest.common.locator import get_locator

DefaultTimeOut = 5
step_time = 0.2


# iframe url
# c.execute_script('return arguments[0].contentWindow.location.href',iframe_el)

class PageAction:
    """
    此类用于封装页面主要方法
    """

    def __init__(self, carrier, time_out=0):
        """
        :type carrier: WebElement,WebDriver
        :param carrier:
        """
        self.carrier = carrier
        self.wait = WebDriverWait(carrier, time_out or DefaultTimeOut)
        self._actions = ActionChains(carrier.parent) if isinstance(carrier, WebElement) else ActionChains(carrier)
        self.is_el = isinstance(carrier, WebElement)
        self.executor = self.carrier.parent.execute_script if self.is_el else self.carrier.execute_script

    @property
    def actions(self):
        self._actions.reset_actions()
        return self._actions

    def click(self, *, el=None, force=False, **locator):
        """
        点击元素的实现
        click when el is enable
        :param el: 传入的WebElement对象
        :param force: 是否使用js强制点击,
        :param locator: 使用locator点击
        :return:
        :Usage
            form selenium.webdriver import Chrome

            driver=Chrome()
            # use locator
            PageActive(driver).click(css="#clickMe")
            PageActive(driver).click(id="clickMe")
            # use element
            el=driver.find_element_by_id("clickMe")
            PageActive(Chrome()).click(el=el)
        """
        # 判断使用el还是locator参数
        _el = self._get_el(el, **locator)

        if force:
            # 使用js点击元素
            click_js = "arguments[0].click()"
            self.executor(click_js, _el)
        else:
            self.wait.until(lambda _: _el if _el.is_enabled() and _el.is_displayed() else False)
            _el.click()

    def find_element(self, *, mode="L", **locator) -> WebElement:
        """
        查找元素
        :param locator: 定位器
        :param mode: 元素模式
            - L : element in DOM
            - V : element is visibility
            - I : element is interactive
        :exception TimeOutException
        :return: marked WebElement
        """
        if step_time:
            sleep(step_time)
        methods = {
            "L": EC.presence_of_element_located,
            "V": EC.visibility_of_element_located,
            "I": EC.element_to_be_clickable,
        }
        method = methods[mode]
        _locator = get_locator(locator)
        el = self.wait.until(method(_locator))
        if EC.staleness_of(el)(None):
            el = self.find_element(mode=mode, **locator)
        self.mark(el)
        return el

    def find_elements(self, *, mode="L", **locator) -> List[WebElement]:
        """
        查询元素,超时后会返回None
        :param locator: 定位器
        :param mode: 元素模式
            - L : elements in DOM
            - V : elements is visibility
            - I : elements is interactive
        :exception TimeOutException
        :return: marked WebElement
        """
        if step_time:
            sleep(step_time)
        # 自建类返回可交互的元素
        interactive_of_any_elements_located = type("interactive_of_any_elements_located", (object,), {
            "__init__":
                lambda self_, locator_: setattr(self_, "locator", locator_),
            "__call__":
                lambda self_, driver:
                [el_ for el_ in driver.find_elements(*self_.locator) if el_.is_enable() and el_.is_displayed()]
        })

        methods = {
            "L": EC.presence_of_all_elements_located,
            "V": EC.visibility_of_any_elements_located,
            "I": interactive_of_any_elements_located
        }
        method = methods[mode]
        locator = get_locator(locator)
        els = self.wait.until(method(locator))
        self.mark(*els)
        return els

    def mark(self, *els):
        """
        标记元素
        :param els: 被标记的元素
        """
        mark_js = 'arguments[0].style.border="2px solid red"'
        for el in els:
            try:
                self.executor(mark_js, el)
            except WebDriverException:
                continue

    def hover(self, *, el=None, **locator):
        """
        悬停
        :param el: 被悬停的元素,元素需要可见
        """
        _el = self._get_el(el, mode="V", **locator)
        self.actions.move_to_element(_el).perform()

    def scroll_by(self, x=0, y=0, *, el=None):
        """
        滚动屏幕或者滚动元素
        :param x: x轴移动的距离
        :param y: y轴移动的距离
        :param el: 滑动元素，如果没有的话，整个窗口滑动
        :return:
        """
        if el is None:
            scroll_js = f"window.scrollBy({x},{y})"
        else:
            scroll_js = f"arguments[0].scrollBy({x},{y})"
        self.executor(scroll_js, el)

    def _get_el(self, el, mode="L", **locator):
        """
        参数解析
        :param el:
        :param mode:
        :param locator:
        :return: WebElement
        """
        if isinstance(el, WebElement):
            _el = el
        elif len(locator) == 1:
            _el = self.find_element(mode=mode, **locator)
        else:
            raise ValueError("bad usage")
        return _el

    class SetPageActionTime:
        def __init__(self, pa, time):
            if not isinstance(pa, PageAction) or isinstance(time, int):
                raise ValueError
            self.pa = pa
            self.time = time
            self._time = self.pa.wait._timeout

        def __enter__(self):
            self.pa.wait._timeout = self.time
            return self.pa

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.pa.wait._timeout = self._time
