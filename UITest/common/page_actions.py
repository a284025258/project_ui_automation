from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from UITest.common.locator import get_locator


def click(driver, force=False, **locator):
    """
    点击元素
    @type driver: WebDriver,WebElement
    @param driver: WebDriver
    @param force: 使用js点击
    @param locator: 定位符: x="//a" or css="a" or id="click_me" etc.
    @return:
    """
    if len(locator) != 1:
        raise ValueError("There must be one and only one locator in your init")

    locator = get_locator(locator.popitem())

    if not force:
        el = _find_element(driver, locator, mode="click")
        el.click()
    else:
        el = _find_element(driver, locator)
        if isinstance(driver, WebDriver):
            driver.execute_script("arguments[0].click()", el)
        elif isinstance(driver, WebElement):
            # driver is WebElement
            driver.parent.execute_script("arguments[0].click()", el)


def _find_element(driver, locator, mode=""):
    """
    查询元素,超时后会返回None
    @param locator: 定位器
    @param mode: 元素模式
    @return: WebElement
    """
    wait = _get_wait(driver)

    method = EC.presence_of_element_located
    if mode == "click":
        method = EC.element_to_be_clickable
    elif mode == "visible":
        method = EC.visibility_of_element_located
    el = wait.until(method(locator))

    _mark(driver, el)
    return el


def _get_wait(driver, timeout=5):
    return WebDriverWait(driver, timeout)


def _mark(driver, el):
    """
    标记元素
    @param el: 被标记的元素
    """
    mark_js = 'arguments[0].style.border="2px solid red"'
    try:
        driver.execute_script(mark_js, el)
    except Exception:
        pass
