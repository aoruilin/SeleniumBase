"""
Created on 2019年3月22日
Last Update on 2019年5月8日

@author: 敖瑞麟
"""
import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestMainProcess(BaseTestCase):
    file_name = __file__
    name = __name__
    # step_log_path = get_log_path(file_name, name)
    d = Data()
    manager_data = d.manager_data()
    teacher_data = d.teacher_data()
    student_data = d.student_data()

    homework_name = d.homework_name
    admin_class_name = d.admin_class_name_for_edu()
    pro_class_name = d.pro_class_name_for_edu()

    def test_MainProcess_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        # self.teacher_login.user_login(self.username_manager, self.manager_name, self.password)
        # self.teacher_click.click_button(*ElementSelector.teach_management_btn_loc)
        # self.teacher_manage.add_account_class(self.username_teacher, self.teacher_name,
        #                                       self.username_student, self.student_name,
        #                                       self.admin_class_name, self.pro_class_name,
        #                                       enable_assert=True)
        # self.teacher_login.user_logout()
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.bar_course_loc)
        course_name = self.add_course_simple(self.teaching_package_list[0])
        self.teacher_check_index_course(course_name)
        self.click_button(*ElementSelector.bar_homework_loc)
        self.click_button(*ElementSelector.homework_list_add_homework_btn_loc, loading=True)
        self.add_homework_simple(self.homework_name, self.answer_list[0], '显示难度')
        self.teacher_check_index_homework(self.homework_name)

        self.get_new_driver()
        self.login(**self.student_data)
        self.student_check_index_homework(self.homework_name)
        self.student_check_index_course(course_name)
        self.click_button(*ElementSelector.course_list_card_mode_first_course_loc)
        self.check_course_simple(course_name)
        self.click_button(*ElementSelector.bar_homework_loc, loading=True)
        completion, correct = self.student_do_homework_simple(self.homework_name)
        # 教师检查作业详情
        self.switch_to_default_driver()
        self.teacher_check_homework_simple(self.homework_name, self.student_data['username'],
                                           self.student_data['name'], completion, correct)


if __name__ == "__main__":
    unittest.main()
