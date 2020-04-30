import unittest
import pytest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.common.picture_list_code import wrong_code
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


@pytest.mark.run(order=9)
class TestErrorCheck(BaseTestCase):
    file_name, name = __file__, __name__
    case_log_path = log_path(file_name, name)

    student_data = Data().student_data()

    @log_decorator(case_log_path)
    def test_field_error(self):
        """
        试炼场
        :return:
        """
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.check_error()

    @log_decorator(case_log_path)
    def test_course_field_error(self):
        """
        课件查看页面精简试炼场
        :return:
        """
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.click_button(*ElementSelector.bar_course_loc)
        self.click_and_jump(1, *ElementSelector.course_list_card_mode_first_course_loc,
                            loading=True)
        self.click_button(*ElementSelector.course_detail_start_study_course_loc,
                          loading=True)
        code = wrong_code()
        self.course_field_operation(code, 'Error', wrong=True)


if __name__ == "__main__":
    unittest.main()
