import unittest

from base.data import Data
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.login import Login
from ui_auto.page_object.element_loc import IndexElement
from ui_auto.page_object.page_operation import ClickButton
from ui_auto.page_object.standard_teach import StandardTeach, StandardTeachElement
from ui_auto.page_object.subject_teach import SubjectTeach, SubjectTeachElement


class DoHomeworkSimple(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.standard = StandardTeach(self.driver)
        self.subject = SubjectTeach(self.driver)
        self.click = ClickButton(self.driver)
        self.username = Data().student_username_for_edu()
        self.password = Data().password_for_edu
        self.name = Data().student_name_for_edu()
        self.url = Data().ip_for_edu()

    def tearDown(self):
        self.driver.quit()

    def test_01(self):
        self.driver.get(self.url)
        self.login.user_login(self.username, self.name, self.password, student_assert=True)
        self.click.click_button(IndexElement.standard_course_btn_loc)
        self.click.click_button(StandardTeachElement.homework_btn_loc)
        self.standard.student_do_homework_simple(homework_name=None, enable_assert=False)

    def test_02(self):
        self.driver.get(self.url)
        self.login.user_login(self.username, self.name, self.password, student_assert=True)
        self.click.click_button(IndexElement.checkpoint_course_loc)
        self.click.click_button(SubjectTeachElement.index_homework_btn_loc)
        self.subject.student_do_homework_simple(homework_name=None, enable_assert=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
