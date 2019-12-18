import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase


class TestAddDraft(BaseTestCase):
    file_name = __file__
    name = __name__

    url = Data().ip_for_edu()
    username_student = Data().student_username_for_edu()
    password = Data().password_for_edu
    student_name = Data().student_name_for_edu()

    def test_save_draft_loop(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.add_draft()


if __name__ == "__main__":
    unittest.main()
