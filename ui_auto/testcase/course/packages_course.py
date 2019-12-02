import unittest

from base.data import Data
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.login import Login
from ui_auto.page_object.element_loc import IndexElement
from ui_auto.page_object.standard_teach import StandardTeach, StandardTeachElement
from ui_auto.page_object.subject_teach import SubjectTeach, SubjectTeachElement
from ui_auto.page_object.page_operation import ClickButton, SearchFunc, SearchFuncElement


class TestPackageCourse(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver_1 = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.driver_2 = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.teacher_login = Login(self.driver_1)
        self.student_login = Login(self.driver_2)
        self.teacher_standard = StandardTeach(self.driver_1)
        self.student_standard = StandardTeach(self.driver_2)
        self.teacher_subject = SubjectTeach(self.driver_1)
        self.student_subject = SubjectTeach(self.driver_2)
        self.teacher_search = SearchFunc(self.driver_1)
        self.student_search = SearchFunc(self.driver_2)
        self.teacher_click = ClickButton(self.driver_1)
        self.student_click = ClickButton(self.driver_2)

        self.url = Data().ip_for_edu()
        self.username_teacher = Data().teacher_username_for_edu()
        self.username_student = Data().student_username_for_edu()
        self.password = Data().password_for_edu
        self.teacher_name = Data().teacher_name_for_edu()
        self.student_name = Data().student_name_for_edu()

    def test_package_course_01(self):
        self.driver_1.get(self.url)
        self.teacher_login.user_login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.teacher_click.click_button(IndexElement.standard_course_btn_loc)
        self.teacher_standard.add_course_loop()
        self.teacher_standard.add_course_wrong(enable_assert=True)
        self.teacher_click.click_button(IndexElement.standard_course_btn_loc)
        self.teacher_search.date_selection('课件', '自动上传课件', enable_assert=True)
        self.teacher_search.search_input('自动上传课件', enable_assert=True)
        self.driver_2.get(self.url)
        self.student_login.user_login(self.username_student, self.student_name, self.password, student_assert=True)
        self.student_click.click_button(IndexElement.standard_course_btn_loc)
        self.student_standard.student_check_course_loop()
        self.student_search.date_selection('课件', '自动上传课件', enable_assert=True)
        self.student_search.search_input('自动上传课件', enable_assert=True)

    def test_package_course_02(self):
        self.driver_1.get(self.url)
        self.teacher_login.user_login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.teacher_click.click_button(IndexElement.checkpoint_course_loc)
        self.teacher_click.click_button(SubjectTeachElement.index_course_btn_loc)
        self.teacher_subject.add_course_loop_checkpoint()
        self.driver_2.get(self.url)
        self.student_login.user_login(self.username_student, self.student_name, self.password, student_assert=True)
        self.student_click.click_button(IndexElement.checkpoint_course_loc)
        self.student_click.click_button(SubjectTeachElement.index_course_btn_loc)
        self.student_subject.student_check_course_loop()

    def tearDown(self):
        self.driver_1.quit()
        self.driver_2.quit()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
