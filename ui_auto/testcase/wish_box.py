import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase


class TestWishBox(BaseTestCase):
    file_name = __file__
    name = __name__

    student_data = Data().student_data()

    def test_wish_box(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data)
        self.wish_box()

    def test_demo(self):
        import time
        from ..page_object.element_loc import ElementSelector
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        time.sleep(1)
        self.driver.close()
        self.switch_window(0)
        time.sleep(1)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()
