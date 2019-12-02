""" NOTE: Using CSS Selectors is better than using XPath!
    XPath Selectors break very easily with website changes. """

# from seleniumbase import BaseCase
#
#
# class MyTestClass(BaseCase):
#
#     def test_xpath(self):
#         self.maximize_window()
#         self.open("http://192.168.0.160:8096")
#         self.assert_element('//img')
#         self.assert_element('/html/body/div[2]/div[2]/img')
#         self.click("//ul/li[6]/a")
#         self.assert_text("xkcd.com", "//h2")
from examples.boilerplates.base_test_case import BaseTestCase


class MyTests(BaseTestCase):

    def test_example(self):
        self.login()
        self.example_method()
