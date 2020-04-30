import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.page_operation import BaseTestCase


class TestAddDraft(BaseTestCase):
    file_name = __file__
    name = __name__
    case_log_path = log_path(file_name, name)

    url = Data().ip_for_edu()
    student_data = Data().student_data()

    @log_decorator(case_log_path)
    def test_save_draft_loop(self):
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.add_draft()


if __name__ == "__main__":
    unittest.main()
