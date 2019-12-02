import unittest
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.login import Login
from ui_auto.page_object.test_field_work import TestField
from base.data import Data


class TestAddDraft(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.tf = TestField(self.driver)

        self.url = Data().ip_for_edu()
        self.username_student = Data().student_username_for_edu()
        self.password = Data().password_for_edu
        self.student_name = Data().student_name_for_edu()

    def tearDown(self):
        self.driver.quit()

    def test_save_draft_loop(self):
        self.driver.get(self.url)
        self.login.user_login(self.username_student, self.student_name, self.password, student_assert=True)
        self.tf.add_draft()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
