import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase


class TestAddDraft(BaseTestCase):
    file_name = __file__
    name = __name__

    url = Data().ip_for_edu()
    student_data = Data().student_data()

    def test_save_draft_loop(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.student_data, student_assert=True)
        self.add_draft()


if __name__ == "__main__":
    unittest.main()
