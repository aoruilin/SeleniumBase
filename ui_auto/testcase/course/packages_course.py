import unittest

from ui_auto.base.data import Data
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestPackageCourse(BaseTestCase):

    url = Data().ip_for_edu()
    username_teacher = Data().teacher_username_for_edu()
    username_student = Data().student_username_for_edu()
    password = Data().password_for_edu
    teacher_name = Data().teacher_name_for_edu()
    student_name = Data().student_name_for_edu()

    def test_package_course_01(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.add_course_loop()
        self.add_course_wrong()
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.date_selection('课件', '自动上传课件')
        self.search_input('自动上传课件')
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.student_check_course_loop()
        self.date_selection('课件', '自动上传课件', student=True)
        self.search_input('自动上传课件')

    def test_package_course_02(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_course_btn_loc, loading=True)
        self.subject_add_course_loop()
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_course_btn_loc, loading=True)
        self.subject_student_check_course_loop()


if __name__ == "__main__":
    unittest.main()
