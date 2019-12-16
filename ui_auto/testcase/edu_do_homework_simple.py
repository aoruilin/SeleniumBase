import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class DoHomeworkSimple(BaseTestCase):
    file_name = __file__
    name = __name__

    username = Data().student_username_for_edu()
    password = Data().password_for_edu
    student_name = Data().student_name_for_edu()
    url = Data().ip_for_edu()
    
    def test_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(self.username, self.student_name, self.password, student_assert=True)
        self.click_button(*ElementSelector.standard_course_btn_loc)
        self.click_button(*ElementSelector.homework_btn_loc)
        self.student_do_homework_simple(homework_name=None)

    def test_02(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.driver.get(self.url)
        self.login(self.username, self.student_name, self.password, student_assert=True)
        self.click_button(*ElementSelector.checkpoint_course_loc)
        self.click_button(*ElementSelector.index_homework_btn_loc)
        self.student_do_homework_simple(homework_name=None)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
