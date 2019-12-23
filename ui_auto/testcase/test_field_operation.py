import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestFieldCase(BaseTestCase):
    # file_name = __file__
    # name = __name__
    step_log_path = get_log_path(__file__, __name__)

    url = Data().ip_for_edu()
    teacher_username = Data().teacher_username_for_edu()
    teacher_name = Data().teacher_name_for_edu()
    student_username = Data().student_username_for_edu()
    student_name = Data().student_name_for_edu()
    password = Data().password_for_edu

    def test_01(self):
        """turtle"""
        self.login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.do_test_field('turtle')

    def test_02(self):
        """pygame"""
        self.login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.do_test_field('pygame')

    def test_03(self):
        """多文件"""
        filename = Data().test_field_file_name
        output = Data().test_field_output
        self.login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.multiple_files_test_field(filename, '多文件测试', output)

    def test_04(self):
        """打开草稿"""
        output = Data().test_field_output
        self.login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.open_file(output)

    def test_05(self):
        """3D打印"""
        self.login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.three_dimensional()

    def test_06(self):
        """素材库"""
        # self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.upload_material()
        self.edit_material_name(Data().material_name)
        self.delete_material()

    def test_07(self):
        """机器人"""
        self.login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.robot()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
