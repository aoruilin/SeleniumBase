import pytest

from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.page_operation import BaseTestCase


@pytest.mark.run(order=6)
class UserLoginWrong(BaseTestCase):
    file_name = __file__
    name = __name__
    case_log_path = log_path(file_name, name)

    @log_decorator(case_log_path)
    def test_wrong_login(self):
        self.step_log_path = self.case_log_path
        self.user_login_wrong()
