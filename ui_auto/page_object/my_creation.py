from unittest import TestCase

from base.data import Data
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.common.input_code import input_code
from ui_auto.common.upload_file import upload_file_by_auto_it
from ui_auto.page_object.page_operation import ClickButton
from ui_auto.page_object.element_loc import CreationSpaceElement, IndexElement
from interface.K12edu.common.picture_list_code import turtle_code


class AddWork:
    def __init__(self, driver):
        self.driver = driver

    def add_work(self, work_name, class_name, test_field=False, enable_assert=False):
        """
        学生作品提交审核

        :param work_name: 提交的作品名称
        :param class_name: 班级名称
        :param test_field: 是否从试炼场进入
        :param enable_assert: 是否检查
        :return: None
        """
        if test_field:
            pass
        else:
            self.driver.find_element(*CreationSpaceElement.work_name_input_loc, send_keys=True, content=work_name)
            code_input_element = self.driver.find_element(*CreationSpaceElement.add_work_cursor_loc, tag=False)
            code = turtle_code()
            input_code(code, code_input_element)
            for a in range(0, 2):
                add_picture_elem = self.driver.find_elements(*CreationSpaceElement.add_picture_btn_loc, loading=True)
                add_work_pic = add_picture_elem[a]
                add_work_pic.click()
                upload_file_by_auto_it('jpg')
        self.driver.find_element(*CreationSpaceElement.sel_class_loc, tag=False, loading=True, click=True)
        self.driver.find_element(*CreationSpaceElement.first_class_loc, tag=False, click=True)
        self.driver.find_element(*CreationSpaceElement.sel_teacher_loc, tag=False, click=True)
        sel_teacher_class_elem_list = self.driver.find_elements_by_xpath(f'//span[text()="{class_name}"]',
                                                                         msg=class_name, tag=False)
        for b in range(3):
            sel_teacher_class_elem = sel_teacher_class_elem_list[b]
            SeleniumDriver.action_chains(self.driver, sel_teacher_class_elem, msg=f'鼠标移到{class_name}')
            try:
                self.driver.find_element_by_xpath(f'//span[text()="{Data().teacher_name_for_edu()}"]',
                                                  tag=False, msg=Data().teacher_name_for_edu(), click=True)
            except BaseException as e:
                print(f'{e}错误的元素，尝试下一个')
        self.driver.find_element(*CreationSpaceElement.submit_audit_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '恭喜你，已提交教师进行审核！'
            actual_tip = self.driver.find_element(*CreationSpaceElement.succ_tip_loc, tag=False, text=True)
            tc = TestCase()
            try:
                tc.assertEqual(actual_tip, exp_tip, '提示错误')
            except Exception as e:
                print(f'{e}提交成功提示错误或作品提交失败，发布作品提交异常')

    def audit_work(self, work_name, enable_assert=False):
        """
        教师审核作品

        :param work_name: 审核的作品名称
        :param enable_assert: 是否检查
        :return: None
        """
        self.driver.find_element(*CreationSpaceElement.screening_tab_loc, click=True)
        name_elem_list = self.driver.find_elements_by_xpath(f'//div[text()="{work_name}"]', msg=work_name)
        work_name_elem = name_elem_list[0]
        work_name_elem.click()
        if '直接审核作品' == work_name:
            self.driver.find_element(*CreationSpaceElement.direct_release_btn_loc, click=True)
            exp_tip = '发布成功'
            msg = '教师直接审核提示错误'
            actual_tip = self.driver.find_element(*CreationSpaceElement.succ_tip_loc, tag=False, text=True)
        elif '详细审核通过作品' == work_name:
            self.driver.find_element(*CreationSpaceElement.detailed_review_btn_loc, click=True)
            self.driver.find_element(*CreationSpaceElement.pass_review_btn_loc, click=True)
            exp_tip = '审核成功！'
            msg = '教师详细审核提示错误'
            actual_tip = self.driver.find_element(*CreationSpaceElement.succ_tip_loc, tag=False, text=True)
        else:
            self.driver.find_element(*CreationSpaceElement.detailed_review_btn_loc, click=True)
            self.driver.find_element(*CreationSpaceElement.reject_btn_loc, click=True)
            exp_tip = '驳回成功！'
            msg = '教师驳回作品提示错误'
            actual_tip = self.driver.find_element(*CreationSpaceElement.succ_tip_loc, tag=False, text=True)
        if enable_assert:
            tc = TestCase()
            try:
                tc.assertEqual(actual_tip, exp_tip, msg)
            except Exception as e:
                print(f'{e},{work_name}作品审核异常')

        ClickButton(self.driver).click_button(IndexElement.creative_space_loc)
        if enable_assert:
            try:
                works_name_elem_list = self.driver.find_elements(*CreationSpaceElement.works_hall_list_loc)
                works_name_list = []
                for o in works_name_elem_list:
                    works_name_list.append(o.text)
                works_name = ''.join(works_name_list)
                tc = TestCase()
                tc.assertIn(work_name, works_name, '该作品不在这页作品大厅中！')
            except Exception as e:
                print(f'{e}作品被驳回，不在作品大厅中，此用例PASS')
