import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class TestAIExperience(BaseTestCase):
    file_name = __file__
    name = __name__

    teacher_data = Data().teacher_data()

    def test_01(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.teacher_data, teacher_assert=True)
        self.click_and_jump(1, *ElementSelector.ai_experience_loc)
        self.ai_experience()


if __name__ == "__main__":
    unittest.main()
