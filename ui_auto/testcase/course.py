import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestCourse(BaseTestCase):
    file_name, name = __file__, __name__
    case_log_path = log_path(file_name, name)
    d = Data()
    manager_data = d.manager_data()
    teacher_data = d.teacher_data()
    student_data = d.student_data()

    @log_decorator(case_log_path)
    def test_01_teacher_preview_course(self):
        self.step_log_path = self.case_log_path
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_course_loc)
        self.preview_course()

    @log_decorator(case_log_path)
    def test_02_traverse_check_course(self):
        self.step_log_path = self.case_log_path
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_course_loc)
        course_name = self.add_course_simple(self.teaching_package_list[0])
        self.click_and_jump(1, *ElementSelector.course_list_card_mode_first_course_loc)
        self.check_course_simple(course_name, teacher=True, check_all=True)
        self.switch_window(0)
        self.del_course()


if __name__ == '__main__':
    unittest.main()
