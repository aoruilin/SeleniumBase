import unittest

from base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.page_object.element_loc import IndexElement, TeachManagementElement
from ui_auto.page_object.login import Login
from ui_auto.page_object.page_operation import ClickButton
from ui_auto.page_object.teach_management import TeachManagement


class AddResourcesCase(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=True) -> None:
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.click = ClickButton(self.driver)
        self.ar = TeachManagement(self.driver)

        self.url = Data().ip_for_edu()
        self.username_teacher = Data().teacher_username_for_edu()
        self.teacher_name = Data().teacher_name_for_edu()
        self.password = Data().password_for_edu

    def tearDown(self) -> None:
        self.driver.quit()

    def test_add_resources(self):
        self.driver.get(self.url)
        self.login.user_login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click.click_button(IndexElement.teach_management_btn_loc)
        self.click.click_button(TeachManagementElement.resource_manage_tab_loc)
        self.click.click_button(TeachManagementElement.resource_type_sel_loc)
        self.click.click_button(TeachManagementElement.school_resource_btn_loc, wait=False)
        self.ar.add_resources(enable_assert=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
