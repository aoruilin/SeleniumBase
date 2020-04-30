import unittest
import pytest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path, log_path
from ui_auto.base.log_decorator import log_decorator
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


@pytest.mark.run(order=4)
class TestFieldCase(BaseTestCase):
    file_name = __file__
    name = __name__
    case_log_path = log_path(file_name, name)

    d = Data()
    teacher_data = d.teacher_data()
    student_data = d.student_data()

    @log_decorator(case_log_path)
    def test_01(self):
        """turtle"""
        self.step_log_path = self.case_log_path

        self.login(**self.student_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.do_test_field('turtle')

    @log_decorator(case_log_path)
    def test_02(self):
        """pygame"""
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.do_test_field('pygame')

    @log_decorator(case_log_path)
    def test_03(self):
        """多文件"""
        self.step_log_path = self.case_log_path
        filename = Data().test_field_file_name
        output = Data().test_field_output
        self.login(**self.teacher_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.multiple_files_test_field(filename, '多文件测试', output)

    @log_decorator(case_log_path)
    def test_04(self):
        """打开草稿"""
        self.step_log_path = self.case_log_path
        output = Data().test_field_output
        self.login(**self.teacher_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.open_file(output)

    @log_decorator(case_log_path)
    def test_05(self):
        """3D打印"""
        self.step_log_path = self.case_log_path
        self.login(**self.teacher_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.three_dimensional()

    @log_decorator(case_log_path)
    def test_06(self):
        """
        试炼场发布作品
        :return:
        """
        work_name = Data().work_name
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.submit_work(work_name)

    @log_decorator(case_log_path)
    def test_07(self):
        """素材库"""
        self.step_log_path = self.case_log_path
        self.login(**self.student_data)
        self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
        self.upload_material()
        # self.edit_material_name(Data().material_name)
        # self.delete_material()

    # def test_08(self):
    #     """机器人"""
    #     self.login(**self.teacher_data, teacher_assert=True)
    #     self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
    #     self.robot()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
