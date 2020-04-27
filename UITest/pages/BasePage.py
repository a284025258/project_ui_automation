import logging
from time import sleep

import allure
from poium import Page
from selenium.webdriver import ActionChains

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BasePage(Page):
    """
    页面元素类根类
    """

    def close(self):
        logger.info("正在关闭浏览器的一个页面")
        self.driver.close()

    def hover(self, el, time_to_hover=1):
        """
        悬停
        :param time_to_hover:
        :param el: 一个元素
        """
        logger.info("尝试悬停在>>>{}元素上".format(el.describe))
        ActionChains(self.driver).move_to_element(el).perform()
        sleep(time_to_hover)

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def quit(self):
        logger.info("正在关闭浏览器")
        return self.driver.quit()

    def screenshots(self, step_name="运行快照"):
        """
        添加屏幕截图
        @param step_name: 步骤名
        @return:
        """
        try:
            allure.attach(self.driver.get_screenshot_as_png(), step_name, allure.attachment_type.PNG)
        except Exception as exc:
            logger.error("添加截图失败")
            logger.error(exc)
        else:
            logger.info("截图成功添加")

    def find_element_by_text(self, text):
        return self.driver.find_element_by_xpath(f"//*[text()='{text}']")
