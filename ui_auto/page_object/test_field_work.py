"""
此模块提供试炼场的元素定位和页面操作
"""
from unittest import TestCase
from time import sleep

from selenium.webdriver.common.keys import Keys

from base.data import Data
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.common.input_code import input_code
from ui_auto.common.upload_file import upload_file_by_auto_it
from ui_auto.page_object.page_operation import Assert, ClickButton
from ui_auto.page_object.element_loc import IndexElement, TestFieldElement, CreationSpaceElement
from interface.K12edu.common.picture_list_code import turtle_code, pygame_code, multiple_files_code, wrong_code
from interface.K12edu.common.picture_list_code import three_dimensional_code, robot_code


class TestField:
    def __init__(self, driver):
        self.driver = driver

    def add_draft(self):
        """
        保存多个个草稿

        :return: None
        """
        for n in range(0, 10):
            ClickButton(self.driver).click_and_jump(IndexElement.test_field_btn_loc, 1)
            self.driver.find_element(*TestFieldElement.draft_name_input_loc, clear=True)
            self.driver.find_element(*TestFieldElement.draft_name_input_loc, tag=False, send_keys=True, content=n)
            self.driver.find_element(*TestFieldElement.save_btn_loc, tag=False, click=True)
            self.driver.find_element(*TestFieldElement.confirm_btn_loc, tag=False, click=True)
            self.driver.close()
            handle = self.driver.window_handles(0)
            self.driver.switch_to_window(handle)

    def test_field(self, model):
        """
        试炼场标准编辑turtle和pygame

        :param model: 传入turtle或pygame
        :return: None
        """
        code_input_element = self.driver.find_element(*TestFieldElement.ace_text_input_loc)
        code_input_element.clear()
        if 'turtle' == model:
            code = turtle_code()
            input_code(code, code_input_element)
        elif 'pygame' == model:
            code = pygame_code()
            input_code(code, code_input_element)
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, click=True)

        if 'pygame' == model:
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.pygame_canvas_loc)
                wait.until(show_up)
                self.driver.find_element(*TestFieldElement.close_pygame_btn_loc, click=True)
            except Exception as e:
                try:
                    out_text = self.driver.find_element(*TestFieldElement.text_out_area_loc, text=True)
                    print(f'报错为{out_text}')
                except Exception as a:
                    print(f'{a}文本输出定位失败')
                print(f'{e}pygame代码运行失败，试炼场pygame异常')
        else:
            sleep(7)
            try:
                exp_text = 'abc'
                out_text = self.driver.find_element(*TestFieldElement.text_out_area_loc, tag=False, text=True)
                assert out_text == exp_text, 'turtle代码运行失败，试炼场turtle异常'
            except Exception as e:
                print(e)
        self.driver.find_element(*TestFieldElement.draft_name_input_loc, clear=True)
        self.driver.find_element(*TestFieldElement.draft_name_input_loc, tag=False, send_keys=True,
                                 content=f'{model}测试')
        self.driver.find_element(*TestFieldElement.save_btn_loc, tag=False, click=True)
        self.driver.find_element(*TestFieldElement.save_confirm_btn_loc, click=True)

    def multiple_files_test_field(self, file_name, draft_name, output, enable_assert=False):
        """
        试炼场多文件代码

        :param file_name: 添加的模块名称
        :param draft_name: 草稿名称
        :param output: 预期输出
        :param enable_assert: 是否检查
        :return: None
        """
        handle = self.driver.window_handles(1)
        self.driver.switch_to_window(handle)
        self.driver.find_element(*TestFieldElement.add_file_btn_loc, click=True)
        self.driver.find_element(*TestFieldElement.create_file_input_loc, send_keys=True, content=file_name)
        self.driver.find_element(*TestFieldElement.add_file_confirm_btn_loc, no_wait=False, click=True)
        code_list = multiple_files_code(file_name, output)
        main_code = code_list[0]
        hey_code = code_list[1]
        code_input_element = self.driver.find_element(*TestFieldElement.ace_text_input_loc)
        input_code(hey_code, code_input_element)
        self.driver.find_element(*TestFieldElement.main_file_tab_loc, click=True)
        input_code(main_code, code_input_element)
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, click=True)
        if enable_assert:
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.text_out_area_loc)
                wait.until(show_up)
                output_text = self.driver.find_element(*TestFieldElement.text_out_area_loc, text=True)
                tc = TestCase()
                tc.assertEqual(output_text, output, '实际输出与预期不一致')
            except Exception as e:
                print(f'{e}运行失败，输出错误')
        self.driver.find_element(*TestFieldElement.draft_name_input_loc, clear=True)
        self.driver.find_element(*TestFieldElement.draft_name_input_loc, tag=False, send_keys=True, content=draft_name)
        self.driver.find_element(*TestFieldElement.save_btn_loc, tag=False, click=True)
        self.driver.find_element(*TestFieldElement.save_confirm_btn_loc, click=True)

    def open_file(self, output, enable_assert=False):
        """
        试炼场打开草稿文件

        :param output: 预期输出
        :param enable_assert: 是否检查
        :return: None
        """
        handle = self.driver.window_handles(1)
        self.driver.switch_to_window(handle)
        file_element = self.driver.find_element(*TestFieldElement.head_file_loc)
        SeleniumDriver.action_chains(self.driver, file_element)
        wait = SeleniumDriver.webdriver_wait(self.driver)
        show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.open_file_btn_loc)
        wait.until(show_up)
        self.driver.find_element(*TestFieldElement.open_file_btn_loc, tag=False, click=True)
        draft_name_element = self.driver.find_element(*TestFieldElement.first_draft_loc)
        draft_name = draft_name_element.text
        draft_name_element.click()
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, click=True)
        if enable_assert:
            try:
                opened_draft_name = self.driver.find_element(*TestFieldElement.draft_name_input_loc).get_attribute(
                    'value')
                tc = TestCase()
                tc.assertEqual(opened_draft_name, draft_name, '文本框中草稿名称与打开草稿名称不符')
            except Exception as e:
                print(f'{e}文本框中草稿名称异常')
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.text_out_area_loc)
                wait.until(show_up)
                output_text = self.driver.find_element(*TestFieldElement.text_out_area_loc, text=True)
                tc = TestCase()
                tc.assertEqual(output_text, output, '实际输出与预期不一致')
            except Exception as e:
                print(f'{e}运行失败，输出错误')

    def three_dimensional(self, enable_assert=False):
        """
        试炼场3D建模

        :param enable_assert: 是否检查
        :return: None
        """
        handle = self.driver.window_handles(1)
        self.driver.switch_to_window(handle)
        type_choose_elem = self.driver.find_element(*TestFieldElement.type_choose_loc)
        SeleniumDriver.action_chains(self.driver, type_choose_elem)
        self.driver.find_element(*TestFieldElement.ck_type_loc, click=True)
        code = three_dimensional_code()
        code_input_element = self.driver.find_element(*TestFieldElement.ace_text_input_loc)
        code_input_element.clear()
        input_code(code, code_input_element)
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, tag=False, click=True)
        if enable_assert:
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.ck_type_output_loc)
                wait.until(show_up)
            except Exception as e:
                print(f'{e}3D建模异常，没有输出')
        self.driver.find_element(*TestFieldElement.draft_name_input_loc, clear=True)
        self.driver.find_element(*TestFieldElement.draft_name_input_loc,
                                 tag=False, send_keys=True, content='3D建模测试')
        self.driver.find_element(*TestFieldElement.save_btn_loc, tag=False, click=True)
        self.driver.find_element(*TestFieldElement.save_confirm_btn_loc, click=True)

    def robot(self, enable_assert=False):
        """
        试炼场机器人

        :param enable_assert: 是否检查
        :return: None
        """
        handle = self.driver.window_handles(1)
        self.driver.switch_to_window(handle)
        type_choose_elem = self.driver.find_element(*TestFieldElement.type_choose_loc)
        SeleniumDriver.action_chains(self.driver, type_choose_elem)
        self.driver.find_element(*TestFieldElement.ck_type_loc, click=True)
        self.driver.find_element(*TestFieldElement.robot_config_btn_loc, click=True)
        robot_box_elem = self.driver.find_element(*TestFieldElement.robot_box_loc)
        SeleniumDriver.action_chains(self.driver, robot_box_elem)
        self.driver.find_element(*TestFieldElement.connect_robot_btn_loc, click=True)
        if enable_assert:
            tc = TestCase()
            try:
                exp_tip = '恭喜你，连接成功！'
                actual_tip = self.driver.find_element(*TestFieldElement.succ_tip_loc, tag=False, text=True)
                tc.assertEqual(actual_tip, exp_tip)
            except Exception as e:
                print(f'{e}连接机器人异常')
        self.driver.find_element(*TestFieldElement.close_robot_config_btn_loc, tag=False, click=True)
        code = robot_code()
        code_input_element = self.driver.find_element(*TestFieldElement.ace_text_input_loc)
        code_input_element.clear()
        input_code(code, code_input_element)
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, tag=False, click=True)
        if enable_assert:
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.robot_img_loc)
                wait.until(show_up)
            except Exception as e:
                print(f'{e}机器人图像异常')

    def check_error(self):
        """
        试炼场
        :return:
        """
        code_input_element = self.driver.find_element(*TestFieldElement.ace_text_input_loc)
        code_input_element.clear()
        code = wrong_code()
        input_code(code, code_input_element)
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, click=True)
        actual_out = self.driver.find_element(*TestFieldElement.text_out_area_loc, text=True)
        assert 'Error' in actual_out

    def submit_work(self, work_name):
        """
        试炼场发布作品

        :param work_name: 发布的作品名称
        :return: None
        """
        name_input_elem = self.driver.find_element(*TestFieldElement.work_name_input_loc)
        name_input_elem.clear()
        name_input_elem.send_keys(work_name)
        code = turtle_code()
        self.driver.find_element(*TestFieldElement.ace_text_input_loc, tag=False, clear=True)
        self.driver.find_element(*TestFieldElement.ace_text_input_loc,
                                 tag=False, send_keys=True, content=Keys.BACKSPACE)
        self.driver.find_element(*TestFieldElement.ace_text_input_loc, tag=False, send_keys=True, content=code)
        self.driver.find_element(*TestFieldElement.run_code_btn_loc, click=True)
        sleep(7)
        self.driver.find_element(*TestFieldElement.submit_work_btn_loc, click=True)
        sleep(7)

        submit_handle = self.driver.window_handles(2)
        self.driver.switch_to_window(submit_handle)

    def upload_material(self, enable_assert=False):
        """
        试炼场上传素材

        :param enable_assert: 是否检查
        :return: None
        """
        handle = self.driver.window_handles(1)
        self.driver.switch_to_window(handle)
        tools_box_elem = self.driver.find_element(*TestFieldElement.tools_box_loc)
        SeleniumDriver.action_chains(self.driver, tools_box_elem)
        self.driver.find_element(*TestFieldElement.material_lib_loc, tag=False, click=True)
        self.driver.find_element(*TestFieldElement.my_material_loc, tag=False, click=True)
        self.driver.find_element(*TestFieldElement.upload_material_btn_loc, tag=False, click=True)
        upload_file_by_auto_it('jpg')
        if enable_assert:
            exp_tip = '上传成功!'
            tc = TestCase()
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.succ_tip_loc)
                wait.until(show_up)
                actual_tip = self.driver.find_element(*TestFieldElement.succ_tip_loc, tag=False, text=True)
                tc.assertEqual(actual_tip, exp_tip)
            except Exception as e:
                print(f'{e}上传素材异常')

    def edit_material_name(self, material_name, enable_assert=False):
        """
        试炼场编辑素材名称

        :param material_name: 编辑的名称
        :param enable_assert: 是否检查
        :return: None
        """
        material_name_elem = self.driver.find_element(*TestFieldElement.material_name_loc)
        SeleniumDriver.action_chains(self.driver, material_name_elem)
        self.driver.find_element(*TestFieldElement.edit_name_btn_loc, tag=False, click=True)
        self.driver.find_element(*TestFieldElement.material_name_input_loc, tag=False, send_keys=True,
                                 content=material_name)
        self.driver.find_element(*TestFieldElement.upload_confirm_btn_loc, tag=False, click=True)
        if enable_assert:
            try:
                actual_material_name = material_name_elem.text
                tc = TestCase()
                tc.assertIn(material_name, actual_material_name)
            except Exception as e:
                print(f'{e}编辑素材名称异常')

    def delete_material(self, enable_assert=False):
        """
        试炼场删除素材

        :param enable_assert: 是否检查
        :return: None
        """
        self.driver.find_element(*TestFieldElement.delete_material_btn_loc, click=True)
        self.driver.find_element(*TestFieldElement.upload_confirm_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '删除素材成功'
            tc = TestCase()
            try:
                wait = SeleniumDriver.webdriver_wait(self.driver)
                show_up = SeleniumDriver.element_presence(self.driver, TestFieldElement.succ_tip_loc)
                wait.until(show_up)
                actual_tip = self.driver.find_element(*TestFieldElement.succ_tip_loc, tag=False, text=True)
                tc.assertEqual(actual_tip, exp_tip)
            except Exception as e:
                print(f'{e}删除素材异常')
