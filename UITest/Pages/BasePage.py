import logging
import os
import time
from time import sleep

import allure
from poium import Page
from selenium.webdriver import ActionChains

from config import IMG_DIR


class BasePage(Page):
    """
    页面元素类根类
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    def close(self):
        self.logger.info("正在关闭浏览器的一个页面")
        self.driver.close()

    def hover(self, el, time_to_hover=1):
        """
        悬停
        :param time_to_hover:
        :param el: 一个元素
        """
        self.logger.info("尝试悬停在》{}《元素上".format(el.describe))
        ActionChains(self.driver).move_to_element(el).perform()
        sleep(time_to_hover)

    def drag_and_drop(self, source, target):
        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def quit(self):
        self.logger.info("正在关闭浏览器")
        return self.driver.quit()

    def screenshots(self, filename=time.strftime("%Y_%M_%d_%H_%M_%S")):
        """
        获得屏幕截图
        :param filename: 文件名
        :return:
        """
        with allure.step("截图"):
            if not filename.endswith('.png'):
                filename += '.png'
            file_path = os.path.join(IMG_DIR, filename)
            if self.driver.get_screenshot_as_file(file_path):
                with open(file_path, mode='rb') as f:
                    allure.attach(f.read(), "执行过程截图", allure.attachment_type.PNG)
                    self.logger.info("截图:{}成功添加".format(file_path))
