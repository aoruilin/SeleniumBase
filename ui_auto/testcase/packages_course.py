import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestPackageCourse(BaseTestCase):
    file_name = __file__
    name = __name__

    d = Data()
    teacher_data = d.teacher_data()
    student_data = d.student_data()

    def test_package_course_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.teacher_data, teacher_assert=True)
        self.click_button(*ElementSelector.standard_course_btn_loc)
        self.add_course_loop()
        self.add_course_wrong()
        self.click_button(*ElementSelector.standard_course_btn_loc)
        self.date_selection('课件', '自动上传课件')
        self.search_input('自动上传课件')
        self.get_new_driver()
        self.login(**self.student_data, student_assert=True)
        self.click_button(*ElementSelector.standard_course_btn_loc)
        self.student_check_course_loop()
        self.date_selection('课件', '自动上传课件', student=True)
        self.search_input('自动上传课件')

    def test_package_course_02(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.teacher_data, teacher_assert=True)
        self.click_button(*ElementSelector.checkpoint_course_loc)
        self.click_button(*ElementSelector.index_course_btn_loc, loading=True)
        self.subject_add_course_loop()
        self.get_new_driver()
        self.login(**self.student_data, student_assert=True)
        self.click_button(*ElementSelector.checkpoint_course_loc)
        self.click_button(*ElementSelector.index_course_btn_loc, loading=True)
        self.subject_student_check_course_loop()


if __name__ == "__main__":
    unittest.main()
