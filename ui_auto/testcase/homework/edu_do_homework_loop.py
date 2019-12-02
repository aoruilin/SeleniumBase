import unittest

from base.data import Data
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import IndexElement, DoHomeWorkElement
from ui_auto.page_object.login import Login
from ui_auto.page_object.standard_teach import StandardTeach, StandardTeachElement
from ui_auto.page_object.subject_teach import SubjectTeach, SubjectTeachElement
from ui_auto.page_object.page_operation import ClickButton, SearchFunc, SearchFuncElement


class DoHomework(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.click = ClickButton(self.driver)
        self.standard = StandardTeach(self.driver)
        self.subject = SubjectTeach(self.driver)
        self.search = SearchFunc(self.driver)

        self.url = Data().ip_for_edu()
        self.username_student = Data().student_username_for_edu()
        self.password = Data().password_for_edu
        self.student_name = Data().student_name_for_edu()

    def tearDown(self):
        self.driver.quit()

    def test_do_homework_loop_01(self):
        self.driver.get(self.url)
        self.login.user_login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click.click_button(IndexElement.standard_course_btn_loc)
        self.click.click_button(StandardTeachElement.homework_btn_loc)
        self.standard.student_do_homework_loop(enable_assert=True)
        self.search.date_selection('作业', Data().homework_name, enable_assert=True)
        self.search.search_input(Data().homework_name, enable_assert=True)

    def test_do_homework_loop_02(self):
        self.driver.get(self.url)
        self.login.user_login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click.click_button(IndexElement.checkpoint_course_loc)
        self.click.click_button(SubjectTeachElement.index_homework_btn_loc)
        self.subject.student_do_homework_loop(enable_assert=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
