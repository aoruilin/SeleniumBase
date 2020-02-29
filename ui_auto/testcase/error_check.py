import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.common.picture_list_code import wrong_code
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestErrorCheck(BaseTestCase):
    file_name = __file__
    name = __name__
    
    student_data = Data().student_data()

    def test_field_error(self):
        """
        试炼场
        :return:
        """
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data, student_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.check_error()

    def test_course_field_error(self):
        """
        课件查看页面精简试炼场
        :return:
        """
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data, student_assert=True)
        self.click_button(*ElementSelector.standard_course_btn_loc)
        self.click_button(*ElementSelector.first_course_loc)
        code = wrong_code()
        self.course_field_operation(code, 'Error', wrong=True)


if __name__ == "__main__":
    unittest.main()
