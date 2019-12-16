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

    url = Data().ip_for_edu()
    username_manager = Data().manager_username_for_edu()
    username_teacher = Data().teacher_username_for_edu()
    username_student = Data().student_username_for_edu()
    password = Data().password_for_edu
    manager_name = Data().edu_manager_name()
    teacher_name = Data().teacher_name_for_edu()
    student_name = Data().student_name_for_edu()
    homework_name = Data().homework_name
    admin_class_name = Data().admin_class_name_for_edu()
    pro_class_name = Data().pro_class_name_for_edu()

    def test_MainProcess_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        # self.teacher_login.user_login(self.username_manager, self.manager_name, self.password, teacher_assert=True)
        # self.teacher_click.click_button(*ElementSelector.teach_management_btn_loc)
        # self.teacher_manage.add_account_class(self.username_teacher, self.teacher_name,
        #                                       self.username_student, self.student_name,
        #                                       self.admin_class_name, self.pro_class_name,
        #                                       enable_assert=True)
        # self.teacher_login.user_logout()
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(*ElementSelector.standard_course_btn_loc)
        course_name = self.add_course_simple(self.teaching_package_list[0])
        self.click_button(*ElementSelector.homework_btn_loc)
        self.click_button(*ElementSelector.add_homework_btn_loc, loading=True)
        self.add_homework_simple(self.homework_name, self.answer_list[0])

        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.student_check_index_course(course_name)
        self.click_button(*ElementSelector.first_course_loc)
        self.student_check_course_simple(course_name)
        self.click_button(*ElementSelector.crumbs_loc)
        self.click_button(*ElementSelector.homework_btn_loc, loading=True)
        self.student_do_homework_simple(self.homework_name)

    def test_MainProcess_02(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(*ElementSelector.checkpoint_course_loc)
        self.click_button(*ElementSelector.start_discover_btn_loc)
        self.click_china_map()
        self.click_map_path()
        self.click_and_jump(1, *ElementSelector.watch_course_btn_loc, loading=True)
        self.click_button(*ElementSelector.kj_add_checkpoint_course_loc)
        checkpoint_course_name = self.subject_add_course_simple(self.teaching_package_list[0],
                                                                discover=True)
        self.click_and_jump(1, *ElementSelector.watch_homework_btn_loc)
        self.click_button(*ElementSelector.add_checkpoint_homework_loc, loading=True)
        self.subject_add_homework_simple(self.homework_name, self.subject_answer_list[0])
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(*ElementSelector.checkpoint_course_loc)
        self.click_button(*ElementSelector.start_discover_btn_loc)
        self.click_china_map()
        self.click_map_path()
        self.click_and_jump(1, *ElementSelector.watch_course_btn_loc, loading=True)
        self.subject_student_check_course_simple(checkpoint_course_name,
                                                 discover=True)
        self.click_and_jump(1, *ElementSelector.watch_homework_btn_loc)
        self.subject_student_do_homework_simple(self.homework_name)


if __name__ == "__main__":
    unittest.main()
