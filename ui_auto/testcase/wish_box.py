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
        self.login(**self.student_data, student_assert=True)
        self.wish_box()

    def test_demo(self):
        # self._default_driver = 'chrome'
        self.open('http://192.168.0.160:8096')
        input_elems = self.elements_list('//input[@class="el-input__inner"]')
        for input_elem in input_elems:
            input_elem.click()

        self.get_new_driver()
        self.open('https://www.baidu.com')
        self.switch_to_default_driver()



if __name__ == "__main__":
    unittest.main()
