from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase


class UserLoginWrong(BaseTestCase):
    file_name = __file__
    name = __name__

    def test_wrong_login(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.user_login_wrong()
