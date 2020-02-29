import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class DoHomework(BaseTestCase):
    file_name = __file__
    name = __name__

    student_data = Data().teacher_data()

    def test_do_homework_loop_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data, student_assert=True)
        self.click_button(*ElementSelector.standard_course_btn_loc)
        self.click_button(*ElementSelector.homework_btn_loc)
        self.student_do_homework_loop()
        self.date_selection('作业', Data().homework_name, student=True)
        self.search_input(Data().homework_name)

    def test_do_homework_loop_02(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data, student_assert=True)
        self.click_button(*ElementSelector.checkpoint_course_loc)
        self.click_button(*ElementSelector.index_homework_btn_loc, loading=True)
        self.subject_student_do_homework_loop()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
