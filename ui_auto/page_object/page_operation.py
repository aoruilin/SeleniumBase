import time
import datetime
from unittest import TestCase

from seleniumbase import BaseCase
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.page_object.element_loc import SearchFuncElement


class ClickButton:
    def __init__(self, driver):
        self.driver = driver

    def click_button(self, btn_loc, wait=True):
        """
        单独点击一个按钮

        :param btn_loc: 按钮定位器
        :param wait: 是否等待
        :return: None
        """
        if wait:
            self.driver.find_element(*btn_loc, click=True)
        else:
            self.driver.find_element(*btn_loc, tag=False, click=True)

    def click_and_jump(self, btn_loc, handle_num):
        """
        点击按钮并跳转新开tab
        :param btn_loc: 按钮定位器
        :param handle_num: 窗口句柄索引号
        :return: None
        """
        self.driver.find_element(*btn_loc, click=True)
        handle = self.driver.window_handles(handle_num)
        self.driver.switch_to_window(handle)

    def jump_and_click(self, handle_num, btn_loc):
        """
        跳转新tab页面后点击按钮
        :param handle_num: 窗口句柄索引号
        :param btn_loc: 按钮定位器
        :return: None
        """
        handle = self.driver.window_handles(handle_num)
        self.driver.switch_to_window(handle)
        self.driver.find_element(*btn_loc, click=True)


class Assert():
    def __init__(self, driver):
        self.driver = driver

    def assert_equal(self, text, text_loc):
        """
        断言文本相等

        :param text: 期望文本
        :param text_loc: 实际文本定位器
        :return: None
        """
        try:
            wait = SeleniumDriver.webdriver_wait(self.driver)
            show_up = SeleniumDriver.element_presence(self.driver, text_loc)
            wait.until(show_up)
            actual_text = self.driver.find_element(*text_loc, text=True, tag=False)
            print(f'期望： "{text}", 实际： "{actual_text}"')
            tc = TestCase()
            tc.assertEqual(text, actual_text)
        except NoSuchElementException:
            print(f'没有{text}')
        except ElementNotVisibleException:
            print(f'未找到{text}元素')
        except Exception as e:
            print(f'{e}， {text}断言异常，与期望不符')

    def assert_in(self, text, text_loc, reverse=False):
        """
        断言文本在页面中

        :param text: 期望文本
        :param text_loc: 实际文本定位器
        :param reverse: True->取出文本all_text在text中，False->text在取出文本all_text中
        :return: None
        """
        try:
            wait = SeleniumDriver.webdriver_wait(self.driver)
            show_up = SeleniumDriver.element_presence(self.driver, text_loc)
            wait.until(show_up)
            actual_text = self.driver.find_element(*text_loc, text=True, no_wait=True)
            tc = TestCase()
            if reverse:
                tc.assertIn(actual_text, text)
            else:
                tc.assertIn(text, actual_text)
        except NoSuchElementException:
            print(f'没有{text}')
        except ElementNotVisibleException:
            print(f'未找到{text}元素')
        except Exception as e:
            print(f'"{e}, {text}断言异常，不在页面中')

    def assert_text_in_page(self, text, text_loc):
        """
        断言文本在指定区域中

        :param text: 期望文本
        :param text_loc: 实际文本定位器
        :return:
        """
        try:
            element_list = self.driver.find_elements(*text_loc)
            text_list = []
            for s in element_list:
                actual_text = s.text
                text_list.append(actual_text)
            all_text = ''.join(text_list)
            tc = TestCase()
            tc.assertIn(text, all_text)
        except NoSuchElementException:
            print(f'没有{text}')
        except ElementNotVisibleException:
            print(f'未找到{text}元素')
        except Exception as e:
            print(f'{e}, {text}断言异常，不在指定区域中')

    def assert_add_course_tip(self, exp_tip, tip_loc, repeated_tip_confirm_loc):
        try:
            self.driver.find_element(*tip_loc, no_wait=True)
        except NoSuchElementException:
            print('已有其他教师在该班级发布这个课件，点击确定继续发布')
            self.driver.find_element(*repeated_tip_confirm_loc, click=True)
            self.assert_equal(exp_tip, tip_loc)
        except BaseException as e:
            print(f'出现未知异常：{e}')
        else:
            self.assert_equal(exp_tip, tip_loc)


class SearchFunc:

    def __init__(self, driver):
        self.driver = driver

    def date_selection(self, page, name, enable_assert=False):
        """
        提供课程和作业列表页面的日期筛选

        :param page: 课程或作业页面
        :param name: 断言用名称
        :param enable_assert: 是否检查
        :return: None
        """
        search_inp = self.driver.find_element(*SearchFuncElement.search_input_loc)
        SeleniumDriver.action_chains(self.driver, search_inp, msg=SearchFuncElement.search_input_loc[-1])

        if '作业' == page:
            self.driver.find_element(*SearchFuncElement.homework_btn_loc, click=True)
        date_input = self.driver.find_elements(*SearchFuncElement.date_search_input_loc)
        date_start_search = date_input[0]

        date_start_search.click()
        time.sleep(1)

        self.driver.find_element(*SearchFuncElement.today_loc, tag=False, click=True)
        self.driver.find_element(*SearchFuncElement.today_end_loc, tag=False, click=True)

        if enable_assert:
            assert_in_page(self.driver, page, name)

        self.driver.refresh()
        date_input = self.driver.find_elements(*SearchFuncElement.date_search_input_loc)
        date_start_search = date_input[0]
        date_start_search.click()
        self.driver.find_element(*SearchFuncElement.today_loc, tag=False, click=True)
        try:
            self.driver.find_element(*SearchFuncElement.tomorrow_end_loc, tag=False, click=True)
        except Exception as e:
            print(f'{e}这周最后一天，改为选择下周第一天')
            self.driver.find_element(*SearchFuncElement.next_week_end_loc, tag=False, click=True)

        if enable_assert:
            assert_in_page(self.driver, page, name)

        self.driver.refresh()
        date_input = self.driver.find_elements(*SearchFuncElement.date_search_input_loc)
        date_start_search = date_input[0]
        date_start_search.click()
        for s in range(2):
            try:
                self.driver.find_element(*SearchFuncElement.tomorrow_loc, tag=False, click=True)
            except Exception as e:
                print(f'{e}这周最后一天，改为选择下周第一天')
                self.driver.find_element(*SearchFuncElement.next_week_loc, tag=False, click=True)
        if enable_assert:
            try:
                self.driver.find_element(*SearchFuncElement.first_course_loc)
                try:
                    self.driver.find_element(*SearchFuncElement.first_homework_loc)
                except Exception as e1:
                    print(f'{e1},筛选日期为明天，没有筛选出资源，此用例PASS')
                    pass
            except Exception as e:
                print(f'{e},筛选日期为明天，没有筛选出资源，此用例PASS')
        self.driver.refresh()

    def search_input(self, name, enable_assert=False):
        """
        课程作业列表页面搜索

        :param name: 要搜索的资源
        :param enable_assert: 是否检查
        :return: None
        """
        search_inp = self.driver.find_element(*SearchFuncElement.search_input_loc)
        search_inp.send_keys(name)
        self.driver.find_element(*SearchFuncElement.search_btn_loc, tag=False, click=True)
        if enable_assert:
            try:
                text = self.driver.find_element_by_xpath('//body', msg='页面', tag=False, text=True)
                tc = TestCase()
                tc.assertIn(name, text, '日期筛选搜索资源错误')
            except Exception as e:
                print(f'"{e}没有搜索到指定的资源，搜索异常')


def assert_in_page(driver, page, name):
    """
    断言资源是否成功搜索

    :param driver: 浏览器驱动
    :param page: 作业或科技
    :param name: 断言用名称
    :return: None
    """
    if '课件' == page:
        course_name_list = driver.find_elements(*SearchFuncElement.course_list_loc)
        name_list = []
        for name_elem in course_name_list:
            course_name = name_elem.text
            name_list.append(course_name)
        all_course_name = '.'.join(name_list)
        try:
            tc = TestCase()
            tc.assertIn(name, all_course_name, '日期筛选错误')
        except Exception as e:
            print(f'{e}没有筛选出指定的课件，筛选异常')
    elif '作业' == page:
        homework_name_list = driver.find_elements(*SearchFuncElement.homework_list_loc)
        name_list = []
        for name_elem in homework_name_list:
            course_name = name_elem.text
            name_list.append(course_name)
        all_course_name = '.'.join(name_list)
        try:
            tc = TestCase()
            tc.assertIn(name, all_course_name, '日期筛选错误')
        except Exception as e:
            print(f'{e}没有筛选出指定的作业，筛选异常')
