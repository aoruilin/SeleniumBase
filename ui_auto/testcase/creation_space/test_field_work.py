import unittest
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from base.data import Data
from ui_auto.page_object.element_loc import IndexElement, CreationSpaceElement
from ui_auto.page_object.login import Login
from ui_auto.page_object.test_field_work import TestField
from ui_auto.page_object.my_creation import AddWork
from ui_auto.page_object.page_operation import ClickButton


class WorksHall(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False) -> None:
        self.driver_1 = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.driver_2 = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.student_login = Login(self.driver_1)
        self.teacher_login = Login(self.driver_2)
        self.student_click = ClickButton(self.driver_1)
        self.teacher_click = ClickButton(self.driver_2)
        self.student_tf = TestField(self.driver_1)
        self.student_ad = AddWork(self.driver_1)
        self.teacher_ad = AddWork(self.driver_2)

        self.url = Data().ip_for_edu()
        self.student_username = Data().student_username_for_edu()
        self.teacher_username = Data().teacher_username_for_edu()
        self.student_name = Data().student_name_for_edu()
        self.teacher_name = Data().teacher_name_for_edu()
        self.password = Data().password_for_edu
        self.direct_release_work_name = Data().direct_release_work_name
        self.detailed_review_work_name = Data().detailed_review_work_name
        self.reject_work_name = Data().reject_work_name
        self.class_name = Data().pro_class_name_for_edu()

    def test_01(self):
        self.driver_1.get(self.url)
        self.student_login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.student_click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.student_tf.submit_work(self.direct_release_work_name)
        self.student_ad.add_work(self.direct_release_work_name, self.class_name, test_field=True, enable_assert=True)
        self.driver_2.get(self.url)
        self.teacher_login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.teacher_click.click_button(IndexElement.creative_space_loc)
        self.teacher_click.click_button(CreationSpaceElement.student_work_tab_loc)
        self.teacher_ad.audit_work(self.direct_release_work_name, enable_assert=True)

    def test_02(self):
        self.driver_1.get(self.url)
        self.student_login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.student_click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.student_tf.submit_work(self.detailed_review_work_name)
        self.student_ad.add_work(self.detailed_review_work_name, self.class_name, test_field=True, enable_assert=True)
        self.driver_2.get(self.url)
        self.teacher_login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.teacher_click.click_button(IndexElement.creative_space_loc)
        self.teacher_click.click_button(CreationSpaceElement.student_work_tab_loc)
        self.teacher_ad.audit_work(self.detailed_review_work_name, enable_assert=True)

    def test_03(self):
        self.driver_1.get(self.url)
        self.student_login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.student_click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.student_tf.submit_work(self.reject_work_name)
        self.student_ad.add_work(self.reject_work_name, self.class_name, test_field=True, enable_assert=True)
        self.driver_2.get(self.url)
        self.teacher_login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.teacher_click.click_button(IndexElement.creative_space_loc)
        self.teacher_click.click_button(CreationSpaceElement.student_work_tab_loc)
        self.teacher_ad.audit_work(self.reject_work_name, enable_assert=True)

    def tearDown(self) -> None:
        self.driver_1.quit()
        self.driver_2.quit()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
