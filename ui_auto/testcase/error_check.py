import unittest

from ui_auto.base.data import Data
from ui_auto.common.picture_list_code import wrong_code
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestErrorCheck(BaseTestCase):
    
    url = Data().ip_for_edu()
    student_username = Data().student_username_for_edu()
    student_name = Data().student_name_for_edu()
    password = Data().password_for_edu

    def test_field_error(self):
        """
        试炼场
        :return:
        """
        self.login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.check_error()

    def test_course_field_error(self):
        """
        课件查看页面精简试炼场
        :return:
        """
        self.login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.click_button(ElementSelector.first_course_loc)
        code = wrong_code()
        self.course_field_operation(code, 'Error', wrong=True)


if __name__ == "__main__":
    unittest.main()
