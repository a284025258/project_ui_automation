from selenium.webdriver.common.by import By

from UITest.pages.BasePage import BasePage


class OrgManagePage(BasePage):

    def switch_tab(self,tab_name):
        self.find_element(By.XPATH,f"//*[text()='{tab_name}']").click()





