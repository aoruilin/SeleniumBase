import unittest
import pytest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


@pytest.mark.run(order=7)
class TestAIExperience(BaseTestCase):
    file_name = __file__
    name = __name__
    case_log_path = log_path(file_name, name)

    teacher_data = Data().teacher_data()

    @log_decorator(case_log_path)
    def test_01(self):
        self.step_log_path = self.case_log_path
        self.login(**self.teacher_data)
        self.click_button(*ElementSelector.ai_experience_loc)
        self.ai_experience()


if __name__ == "__main__":
    unittest.main()
