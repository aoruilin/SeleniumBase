import unittest
import pytest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


@pytest.mark.run(order=5)
class TestMyCreation(BaseTestCase):
    file_name = __file__
    name = __name__
    case_log_path = log_path(file_name, name)

    d = Data()
    student_data = d.student_data()
    work_name = d.work_name

    @log_decorator(case_log_path)
    def test_01(self):
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.click_button(*ElementSelector.bar_creative_space_loc)
        self.click_button(*ElementSelector.works_hall_my_works_tab_loc, loading=True)
        self.click_button(*ElementSelector.my_creation_draft_btn_loc, loading=True)
        self.click_button(*ElementSelector.my_creation_publish_draft_btn_loc, loading=True)
        self.add_work(self.work_name)


if __name__ == '__main__':
    unittest.main()
