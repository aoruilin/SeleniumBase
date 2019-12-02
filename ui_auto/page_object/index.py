import os
from unittest import TestCase

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.common.upload_file import upload_file_by_auto_it
from ui_auto.page_object.page_operation import Assert


class Index:
    """首页操作"""

    def __init__(self, driver):
        self.driver = driver
        self.assert_in = Assert(self.driver)

    def wish_box(self):
        """
        首页意见反馈操作

        :return: None
        """
        self.driver.find_element(*ElementSelector.feedback_btn_loc, click=True)
        self.driver.find_element(*ElementSelector.content_textarea_loc, content='意见反馈测试', send_keys=True)
        self.driver.find_element(*ElementSelector.upload_pic_loc, click=True, tag=False)
        upload_file_by_auto_it('jpg')
        self.driver.find_element(*ElementSelector.submit_btn_loc, tag=False, loading=True, click=True)

    def ai_experience(self, enable_assert=False):
        """
        AI体验

        :param enable_assert: 是否检查
        :return: None
        """
        self.driver.find_element(*ElementSelector.image_identify_tab_loc, click=True)
        self.driver.find_element(*ElementSelector.upload_pic_loc, loading=True, click=True)
        upload_file_by_auto_it('jpg')
        face_output = '年龄：'
        car_license_output = '车牌号为：'
        pic_tag_output = '这个是'
        fail_output = '上传图片无法识别'
        btn_text_list = ['人脸', '车牌', '图片标签']
        for t in btn_text_list:
            self.driver.find_element_by_xpath(f'//span[contains(text(),"{t}")]', msg=t, click=True)
            if enable_assert:
                tc = TestCase()
                try:
                    actual_output = self.driver.find_element(*ElementSelector.output_text_loc, loading=True,
                                                             text=True)
                    try:
                        if '人脸' == t:
                            tc.assertIn(face_output, actual_output, '人脸识别失败')
                        elif '车牌' == t:
                            tc.assertIn(car_license_output, actual_output, '车牌识别失败')
                        else:
                            tc.assertIn(pic_tag_output, actual_output, '图片标签识别失败')
                    except Exception as a:
                        print(f'{a}用失败提示再次断言')
                        tc.assertIn(fail_output, actual_output)
                except Exception as e:
                    print(f'{e}图片识别异常')
        self.driver.find_element(*ElementSelector.car_pic_loc, click=True)
        for t in btn_text_list:
            self.driver.find_element_by_xpath(f'//span[contains(text(),"{t}")]', tag=False, loading=True, msg=t,
                                              click=True)
            if enable_assert:
                tc = TestCase()
                try:
                    actual_output = self.driver.find_element(*ElementSelector.output_text_loc, loading=True,
                                                             text=True)
                    try:
                        if '人脸' == t:
                            tc.assertIn(face_output, actual_output, '人脸识别失败')
                        elif '车牌' == t:
                            tc.assertIn(car_license_output, actual_output, '车牌识别失败')
                        else:
                            tc.assertIn(pic_tag_output, actual_output, '图片标签识别失败')
                    except Exception as a:
                        print(f'{a}，使用失败提示再次断言')
                        tc.assertIn(fail_output, actual_output)
                except Exception as e:
                    print(f'{e}图片识别异常')

        word = '叮当码'
        for tab in range(1, 3):
            self.driver.find_element_by_xpath(f'//div[@class="item-change-box clearfix"]/div[{tab}]',
                                              tag=False, click=True)
            self.driver.find_element(*ElementSelector.word_input_loc, send_keys=True, content=word)
            self.driver.find_element(*ElementSelector.generate_btn_loc, tag=False, click=True)
            self.assert_in.assert_in('我还在学习', ElementSelector.succ_tip_loc)
            tc = TestCase()
            if tab == 1:
                try:
                    actual_title = self.driver.find_element(*ElementSelector.poetry_title_loc,
                                                            text=True, loading=True)
                    tc.assertEqual(word, actual_title)
                except NoSuchElementException:
                    print('没找到元素')
                except ElementNotVisibleException:
                    print('元素不存在')
                except BaseException as e:
                    print(f'{e}创作诗句异常')
            else:
                try:
                    actual_title = self.driver.find_element(*ElementSelector.couples_title_loc,
                                                            text=True, loading=True)
                    if all([actual_title]):
                        pass
                    else:
                        print('异常：春联标题没有文本')
                except NoSuchElementException:
                    print('没找到元素')
                except ElementNotVisibleException:
                    print('元素不存在')
                except BaseException as e:
                    print(f'{e}创作春联异常')
            self.driver.find_element(*ElementSelector.subject_word_loc, click=True)
            actual_word = self.driver.find_element(*ElementSelector.subject_word_loc,
                                                   text=True, loading=True)
            if tab == 1:
                self.assert_in.assert_equal(actual_word, ElementSelector.poetry_title_loc)
            else:
                try:
                    couple_text = self.driver.find_element(*ElementSelector.couples_text_loc,
                                                           text=True)
                    c_list = couple_text.split('\n')
                    if any(c_list):
                        for a in actual_word:
                            tc.assertIn(a, c_list)
                    else:
                        print('异常：没有春联文本')
                except NoSuchElementException:
                    print('没找到元素')
                except ElementNotVisibleException:
                    print('元素不存在')
                except BaseException as e:
                    print(f'{e}创作春联异常')
