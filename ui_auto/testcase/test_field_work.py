import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class WorksHall(BaseTestCase):
    file_name = __file__
    name = __name__
    
    d = Data()
    student_data = d.student_data()
    work_name = Data().work_name

    def test_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data, student_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.submit_work(self.work_name)
        self.add_work(self.work_name, test_field=True)


if __name__ == "__main__":
    unittest.main()
