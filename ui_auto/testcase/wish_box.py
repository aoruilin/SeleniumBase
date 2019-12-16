import unittest

from ui_auto.base.data import Data
from ui_auto.page_object.page_operation import BaseTestCase


class TestWishBox(BaseTestCase):

    username_student = Data().student_username_for_edu()
    password = Data().password_for_edu
    student_name = Data().student_name_for_edu()

    def test_wish_box(self):
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.wish_box()


if __name__ == "__main__":
    unittest.main()
