import unittest

from base.data import Data
from ui_auto.base.config import Config
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import IndexElement
from ui_auto.page_object.login import Login
from ui_auto.page_object.page_operation import ClickButton
from ui_auto.page_object.standard_teach import StandardTeach, StandardTeachElement


class UniTeachDoHomework(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.click = ClickButton(self.driver)
        self.standard = StandardTeach(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_01(self):
        state = Config.state
        url = Data.ip_for_uni_teach(state)
        self.driver.get(url)
        username = Data.student_username_for_uni_teach(state)
        password = Data.password_for_uniTeach
        student_name = Data.uni_teach_student_name(state)
        self.login.login_for_uni_teach(username, student_name, password, student_assert=True)
        self.click.click_button(IndexElement.uni_teach_start_course_btn_loc)
        self.click.click_button(StandardTeachElement.homework_btn_loc)
        self.standard.student_do_homework_for_teach(enable_assert=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
