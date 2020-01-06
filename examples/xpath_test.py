""" NOTE: Using CSS Selectors is better than using XPath!
    XPath Selectors break very easily with website changes. """

import time
from seleniumbase import BaseCase


class MyTestClass(BaseCase):

    def test_xpath(self):
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.by import By
        self.maximize_window()
        self.open("https://www.baidu.com/")
        time.sleep(2)
        # e = self.driver.find_element(By.CSS_SELECTOR, '#su')
        # self.driver.w3c = False
        # ActionChains(self.driver).move_to_element(e).perform()
        self.hover_on_element('#su')
        self.hover_and_click('#su', '#su')
        time.sleep(3)
# from examples.boilerplates.base_test_case import BaseTestCase
#
#
# class MyTests(BaseTestCase):
#
#     def test_example(self):
#         self.login()
#         self.example_method()
