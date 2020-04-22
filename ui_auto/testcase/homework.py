import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestHomework(BaseTestCase):
    file_name = __file__
    name = __name__
    case_log_path = log_path(file_name, name)

    d = Data()
    teacher_data = d.teacher_data()
    student_data = d.student_data()
    username = Data().teacher_username_for_edu()
    password = Data().password_for_edu
    username_student = Data().student_username_for_edu()
    student_name = Data().student_name_for_edu()
    teacher_name = Data().teacher_name_for_edu()

    @log_decorator(case_log_path)
    def test_01_homework_loop(self):
        self.step_log_path = self.case_log_path
        # 教师操作
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.add_homework_loop()
        # self.date_selection('作业', Data().homework_name)   # 日期筛选全部砍掉了，先保留代码免得后面又加回来
        # 学生操作
        self.get_new_driver()
        self.login(**self.student_data)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.student_do_homework_loop()
        # self.date_selection('作业', Data().homework_name, student=True)

    @log_decorator(case_log_path)
    def test_02_add_homework_wrong(self):
        self.step_log_path = self.case_log_path
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.add_homework_wrong()

    @log_decorator(case_log_path)
    def test_03_homework_search(self):
        self.step_log_path = self.case_log_path
        # 教师操作
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.search_input('自动')
        # 学生操作
        self.get_new_driver()
        self.login(**self.student_data)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.search_input('自动')


if __name__ == "__main__":
    unittest.main()
