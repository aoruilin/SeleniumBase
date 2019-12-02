import unittest

from base.data import Data
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import IndexElement
from ui_auto.page_object.login import Login
from ui_auto.page_object.page_operation import ClickButton
from ui_auto.page_object.test_field_work import TestField


class TestFieldCase(unittest.TestCase):
    log_path = get_log_path(__file__, __name__)

    def setUp(self, browser=None, except_tag=False):
        self.driver = SeleniumDriver(log_path=self.log_path, browser=browser, except_tag=except_tag)
        self.login = Login(self.driver)
        self.click = ClickButton(self.driver)
        self.tf = TestField(self.driver)

        self.url = Data().ip_for_edu()
        self.teacher_username = Data().teacher_username_for_edu()
        self.teacher_name = Data().teacher_name_for_edu()
        self.student_username = Data().student_username_for_edu()
        self.student_name = Data().student_name_for_edu()
        self.password = Data().password_for_edu

    def tearDown(self):
        self.driver.quit()

    def test_01(self):
        """turtle"""
        self.driver.get(self.url)
        self.login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.test_field('turtle')

    def test_02(self):
        """pygame"""
        self.driver.get(self.url)
        self.login.user_login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.test_field('pygame')

    def test_03(self):
        """多文件"""
        self.driver.get(self.url)
        filename = Data().test_field_file_name
        output = Data().test_field_output
        self.login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.multiple_files_test_field(filename, '多文件测试', output, enable_assert=True)

    def test_04(self):
        """打开草稿"""
        self.driver.get(self.url)
        output = Data().test_field_output
        self.login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.open_file(output, enable_assert=True)

    def test_05(self):
        """3D打印"""
        self.driver.get(self.url)
        self.login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.three_dimensional(enable_assert=True)

    def test_06(self):
        """素材库"""
        self.driver.get(self.url)
        self.login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.upload_material(enable_assert=True)
        self.tf.edit_material_name(Data().material_name, enable_assert=True)
        self.tf.delete_material(enable_assert=True)

    def test_07(self):
        """机器人"""
        self.driver.get(self.url)
        self.login.user_login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click.click_and_jump(IndexElement.test_field_btn_loc, 1)
        self.tf.robot(enable_assert=True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
