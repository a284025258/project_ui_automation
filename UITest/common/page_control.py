from selenium.webdriver.remote.webelement import WebElement


class BaseControl:

    def __init__(self, el):
        self.el: WebElement = el
