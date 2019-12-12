from ui_auto.page_object.page_operation import BaseTestCase


class UserLoginWrong(BaseTestCase):

    def test_wrong_login(self):

        self.user_login_wrong()
