import unittest

from base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.page_object.element_loc import StandardTeachElement
from ui_auto.page_object.element_loc import IndexElement
from ui_auto.page_object.standard_teach import StandardTeach
from ui_auto.page_object.login import Login
from ui_auto.page_object.page_operation import ClickButton
from ui_auto.page_object.test_field_work import TestField
from interface.K12edu.common.picture_list_code import wrong_code


class TestErrorCheck(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False) -> None:
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.click = ClickButton(self.driver)
        self.tf = TestField(self.driver)
        self.standard = StandardTeach(self.driver)

        self.url = Data().ip_for_edu()
        self.student_username = Data().student_username_for_edu()
        self.student_name = Data().student_name_for_edu()
        self.password = Data().password_for_edu

    def tearDown(self) -> None:
        self.driver.quit()

    def test_field_error(self):
        """
        试炼场
        :return:
        """
        self.driver.get(self.url)
        self.login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.check_error()

    def test_course_field_error(self):
        """
        课件查看页面精简试炼场
        :return:
        """
        self.driver.get(self.url)
        self.login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click.click_button(IndexElement.standard_course_btn_loc)
        self.click.click_button(StandardTeachElement.first_course_loc)
        code = wrong_code()
        self.standard.course_field_operation(code, 'Error', wrong=True)


if __name__ == "__main__":
    unittest.main()
