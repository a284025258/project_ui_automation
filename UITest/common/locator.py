from selenium.webdriver.common.by import By

_Locators = {
    By.ID: ["id"],
    By.XPATH: ["xpath", "x", "text"],
    By.LINK_TEXT: ["link_text", "lt"],
    By.PARTIAL_LINK_TEXT: ["partial_link_text", "plt"],
    By.NAME: ["name"],
    By.TAG_NAME: ["tag_name", "tag"],
    By.CLASS_NAME: ["class_name", "class"],
    By.CSS_SELECTOR: ["css_selector", "css"],
}


def __get_locators(_):
    result = {}
    for key, values in _.items():
        for value in values:
            result[value] = key
    return result


Locators = __get_locators(_Locators)


def get_locator(locator: dict):
    """
    获取locator
    :param locator:
    :return:

    Usage:
    get_locator(("css", "div a")) == (By.CSS_SELECTOR,"div a")
    get_locator(("x", "//a")) == (By.XPATH,"//a")
    get_locator(("text", "value")) == (By.XPATH,"//*[text()='value']")

    """
    if not isinstance(locator, dict) or len(locator) != 1:
        raise ValueError("bad usage")
    by, val = locator.copy().popitem()
    if by == "text_c":
        val = f"//*[contains(text(),'{val}')]"
    elif by == "text":
        val = f"//*[text()='{val}']"
    return Locators[by], val


if __name__ == '__main__':
    print(Locators.items())
    print(get_locator({"text": "locator"}))
    print(get_locator({"css": "locator"}))
    assert get_locator({"x": "//a"}) == (By.XPATH, "//a")
    assert get_locator({"text": "value"}) == (By.XPATH, "//*[text()='value']")
