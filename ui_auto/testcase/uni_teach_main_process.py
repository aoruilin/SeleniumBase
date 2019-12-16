'''
Created on 2019年3月22日
Finished on 2019年5月8日

@author: 敖瑞麟
'''
import unittest

from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.base.config import Config
from base.data import Data
from ui_auto.page_object.element_loc import IndexElement, CheckCourseElement, DoHomeWorkElement
from ui_auto.page_object.login import Login
from ui_auto.page_object.standard_teach import StandardTeach, StandardTeachElement
from ui_auto.page_object.page_operation import ClickButton


# from ui_auto.page_object.course.student_check_course import uni_teach_student_check_course
# from ui_auto.page_object.homework.add_homework import add_homework_for_uni_teach
# from ui_auto.page_object.homework.student_do_homework import student_do_homework_traditional


# from base.read_config import get_ip_info


class TestMainProcess(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver_1 = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.driver_2 = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.teacher_login = Login(self.driver_1)
        self.student_login = Login(self.driver_2)
        self.teacher_standard = StandardTeach(self.driver_1)
        self.student_standard = StandardTeach(self.driver_2)
        self.teacher_click = ClickButton(self.driver_1)
        self.student_click = ClickButton(self.driver_2)

    def tearDown(self):
        self.driver_1.quit()
        self.driver_2.quit()

    def test_MainProcess(self):
        state = Config.state
        base_url = Data.ip_for_uni_teach(state)
        self.driver_1.get(base_url)
        username_teacher = Data.teacher_username_for_uni_teach(state)
        username_student = Data.student_username_for_uni_teach(state)
        password = Data.password_for_uniTeach
        teacher_name = Data.uni_teach_teacher_name
        student_name = Data.uni_teach_student_name
        homework_name = Data.homework_name
        self.teacher_login.login_for_uni_teach(username_teacher, teacher_name, password, teacher_assert=False)
        self.teacher_click.click_button(IndexElement.uni_teach_start_course_btn_loc)
        course_name = self.teacher_standard.add_course_simple(StandardTeach.teaching_package_list[0],
                                                              enable_assert=True)
        self.teacher_click.click_button(StandardTeachElement.homework_btn_loc)
        self.teacher_click.click_button(StandardTeachElement.add_homework_btn_loc)
        self.teacher_standard.add_homework_simple(homework_name, StandardTeach.answer_list[0],
                                                  enable_assert=True)
        self.driver_2.get(base_url)
        self.student_login.login_for_uni_teach(username_student, student_name, password, student_assert=False)
        self.student_standard.uni_teach_student_check_course(course_name, enable_assert=True)
        self.student_click.click_button(CheckCourseElement.crumbs_loc)
        self.student_click.click_button(DoHomeWorkElement.homework_btn_loc)
        self.student_standard.student_do_homework_simple(homework_name, enable_assert=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
