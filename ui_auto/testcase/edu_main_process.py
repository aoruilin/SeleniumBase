"""
Created on 2019年3月22日
Last Update on 2020年3月5日

@author: 敖瑞麟
"""
import unittest
import pytest  # 请忽略不在必要条件文件的警告~

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


@pytest.mark.run(order=1)
class TestMainProcess(BaseTestCase):
    file_name, name = __file__, __name__
    case_log_path = log_path(file_name, name)
    d = Data()
    manager_data = d.manager_data()
    teacher_data = d.teacher_data()
    student_data = d.student_data()

    homework_name = d.homework_name
    admin_class_name = d.admin_class_name_for_edu()
    pro_class_name = d.pro_class_name_for_edu()

    @log_decorator(case_log_path)
    def test_01_main_process_course(self):
        self.step_log_path = self.case_log_path
        # 教师操作
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_course_loc)
        course_name = self.add_course_simple(self.teaching_package_list[0])
        self.click_and_jump(1, *ElementSelector.course_list_card_mode_first_course_loc)
        self.check_course_simple(course_name, teacher=True)
        self.teacher_check_index_course(course_name)
        # 学生操作
        self.get_new_driver()
        self.login(**self.student_data)
        self.student_check_index_course(course_name)
        self.click_and_jump(1, *ElementSelector.course_list_card_mode_first_course_name_loc)
        self.check_course_simple(course_name)

    @log_decorator(case_log_path)
    def test_02_main_process_homework(self):
        self.step_log_path = self.case_log_path
        # 教师发布作业
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.click_button(*ElementSelector.homework_list_add_homework_btn_loc, loading=True)
        add_homework_param = {
            'homework_name': self.homework_name,
            'answer_config': self.answer_list[0],
            'difficulty': 1
        }
        self.add_homework_simple(**add_homework_param)
        self.teacher_check_index_homework(self.homework_name)
        # 学生做作业
        self.get_new_driver()
        self.login(**self.student_data)
        self.student_check_index_homework(self.homework_name)
        self.click_button(*ElementSelector.bar_homework_loc, loading=True)
        completion, correct = self.student_do_homework_simple(self.homework_name)
        # 教师检查作业详情
        self.switch_to_default_driver()
        self.teacher_check_index_homework(self.homework_name)
        self.teacher_check_homework_simple(self.homework_name, completion, correct)

    @log_decorator(case_log_path)
    def test_03_delete_course(self):
        self.step_log_path = self.case_log_path
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_course_loc)
        self.del_course()


if __name__ == "__main__":
    unittest.main()
