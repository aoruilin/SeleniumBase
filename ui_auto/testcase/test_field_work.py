import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class WorksHall(BaseTestCase):
    file_name = __file__
    name = __name__
    
    url = Data().ip_for_edu()
    student_username = Data().student_username_for_edu()
    teacher_username = Data().teacher_username_for_edu()
    student_name = Data().student_name_for_edu()
    teacher_name = Data().teacher_name_for_edu()
    password = Data().password_for_edu
    work_name = Data().work_name

    def test_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.submit_work(self.work_name)
        self.add_work(self.work_name, test_field=True)


if __name__ == "__main__":
    unittest.main()
