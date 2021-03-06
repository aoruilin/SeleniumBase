import time
import datetime
from calendar import weekday
from random import choice

from selenium.common.exceptions import WebDriverException, ElementNotVisibleException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

from seleniumbase import BaseCase

from interface.K12edu.common.parameter_for_others import ParameterForOthers
from ui_auto.base.data import Data, PointIdIndex
from ui_auto.base.logs import log
from ui_auto.common.mysql import get_code, get_choice
from ui_auto.common.upload_file import upload_file_by_auto_it
from ui_auto.common.picture_list_code import turtle_code, \
    pygame_code, multiple_files_code, three_dimensional_code, robot_code, wrong_code
from ui_auto.common.input_code import input_code
from ui_auto.page_object.element_loc import ElementSelector


class BaseTestCase(BaseCase):

    def setUp(self, masterqa_mode=False):
        super(BaseTestCase, self).setUp()
        self.step_log_path = None
        self.url_for_edu = Data().ip_for_edu()
        self.url_for_uni = Data().ip_for_uni_teach()
        self.parameter = ParameterForOthers(identity='student')

    def tearDown(self):
        # Add custom tearDown code for your tests BEFORE the super().tearDown()
        super(BaseTestCase, self).tearDown()

    def open_the(self, url):
        log(self.step_log_path, f'打开网址：{url}')

        return self.open(url=url)

    def back(self):
        """
        浏览器后退
        :return:
        """
        log(self.step_log_path, '后退到上一页')

        return self.go_back()

    def click_button(self, btn_loc, msg=None, wait=False, loading=False):
        """
        单独点击一个按钮

        :param btn_loc: 按钮定位器
        :param msg: 日志信息
        :param wait: 是否等待
        :param loading: 是否等待遮罩层
        :return: None
        """
        if loading:
            log(self.step_log_path, '等待遮罩层隐藏')
            if self.__wait_for_loading():
                if wait:
                    log(self.step_log_path, f'慢速点击{msg}')
                    self.slow_click(btn_loc)
                else:
                    log(self.step_log_path, f'点击{msg}')
                    self.click(btn_loc)
        else:
            if wait:
                log(self.step_log_path, f'慢速点击{msg}')
                self.slow_click(btn_loc)
            else:
                log(self.step_log_path, f'点击{msg}')
                self.click(btn_loc)

    def hover_click(self, hover_loc, btn_loc, msg=None):
        log(self.step_log_path, f'hover并点击{msg}')

        return self.hover_and_click(hover_loc, btn_loc)

    def switch_window(self, window):
        log(self.step_log_path, f'正在切换到第{window + 1}个窗口')

        return self.switch_to_window(window)

    def click_and_jump(self, handle_num, btn_loc, msg=None, wait=False, loading=False):
        """
        点击按钮并跳转新开tab
        :param btn_loc: 按钮定位器
        :param msg: 日志信息
        :param handle_num: 窗口句柄索引号
        :param wait:
        :param loading:
        :return:
        """
        if loading:
            if self.__wait_for_loading():
                log(self.step_log_path, f'等待遮罩层隐藏')
                if wait:
                    log(self.step_log_path,
                        f'慢速点击{msg}并切换第{handle_num + 1}个窗口')
                    self.slow_click(btn_loc)
                    self.switch_window(handle_num)
                else:
                    log(self.step_log_path,
                        f'点击{msg}并切换第{handle_num + 1}个窗口')
                    self.click(btn_loc)
                    self.switch_window(handle_num)
        else:
            if wait:
                log(self.step_log_path,
                    f'慢速点击{msg}并切换第{handle_num + 1}个窗口')
                self.slow_click(btn_loc)
                self.switch_window(handle_num)
            else:
                log(self.step_log_path,
                    f'点击{msg}并切换第{handle_num + 1}个窗口')
                self.click(btn_loc)
                self.switch_window(handle_num)

    def change_text(self, selector, msg=None, text=None):
        log(self.step_log_path, f'清空{msg}现有文本后，输入：{text}')

        return self.update_text(selector, new_value=text)

    def send_text(self, selector, msg=None, text=None):
        log(self.step_log_path, f'在：{msg}，输入：{text}')

        return self.add_text(selector, text=text)

    def take_text(self, selector, msg=None):
        log(self.step_log_path, f'拿到 {msg} 中的文本')

        return self.get_text(selector)

    def wait_text(self, text, selector='html', msg='页面'):
        log(self.step_log_path, f'等待 {msg} 中出现 {text}')

        return self.wait_for_text_visible(text, selector)

    def wait_element_visible(self, selector, msg=None):
        log(self.step_log_path, f'等待元素{msg}在页面可见')

        return self.wait_for_element_visible(selector)

    def take_element(self, selector, msg=None):
        log(self.step_log_path, f'拿到元素 {msg}')

        return self.get_element(selector)

    def take_attribute(self, selector, msg=None, attribute=None):
        log(self.step_log_path, f'获取元素{msg}的属性{attribute}的值')

        return self.get_attribute(selector, attribute)

    def element_visible(self, selector, msg=None):
        log(self.step_log_path, f'等待 {msg} 可见')

        return self.wait_for_element_visible(selector)

    def element_not_visible(self, selector, msg=None):
        log(self.step_log_path, f'等待 {msg} 不可见')

        return self.wait_for_element_not_visible(selector)

    def elements_list(self, selector, msg=None, loading=False):
        """
        复数定位器返回元素列表
        :param selector: 定位器
        :param msg: 日志信息
        :param loading: 是否等待遮罩
        :return:
        """
        if loading:
            if self.__wait_for_loading():
                log(self.step_log_path, f'等待遮罩层隐藏')
                log(self.step_log_path, f'查找所有的{msg}')
                return self.find_elements(selector)
        else:
            return self.find_elements(selector)

    def login(self, username, password, name):
        # self.maximize_window()
        self.set_window_size(1250, 1035)
        self.open_the(self.url_for_edu)
        self.change_text(*ElementSelector.username_input_loc, text=username)
        self.change_text(*ElementSelector.password_input_loc, text=password)
        self.click_button(*ElementSelector.save_login_loc)
        self.click_button(*ElementSelector.login_btn_loc)
        self.wait_for_element(*ElementSelector.index_portrait_loc)
        # 登录有帮助引导，直接忽略
        try:
            # 点击头像
            self.click_button(*ElementSelector.index_portrait_loc,
                              loading=True, wait=True)
        except ElementNotVisibleException:
            log(self.step_log_path, '不是第一次登录，没有新手指引')
            self.click_button(*ElementSelector.index_help_ignore_loc, loading=True)
            self.click_button(*ElementSelector.index_portrait_loc, loading=True)
        finally:
            # 检查头像下拉框用户名字
            self.__assert_equal(name, ElementSelector.index_portrait_name_loc)
            self.click_button(*ElementSelector.index_portrait_loc)

    def login_for_uni_teach(self, username, name, password, teacher_assert=False, student_assert=False):
        self.open_the(self.url_for_uni)
        self.change_text(*ElementSelector.username_input_loc, text=username)
        self.change_text(*ElementSelector.password_input_loc, text=password)
        self.click_button(*ElementSelector.save_login_loc)
        self.click_button(*ElementSelector.uni_teach_login_btn_loc)

        if teacher_assert:
            self.__assert_equal(name, ElementSelector.index_teacher_name_loc)

        if student_assert:
            self.__assert_equal(name, ElementSelector.index_student_name_loc)

    def user_login_wrong(self):
        self.open_the(self.url_for_edu)
        self.change_text(*ElementSelector.username_input_loc, text='152084519491')
        self.change_text(*ElementSelector.password_input_loc, text='123456')
        self.click_button(*ElementSelector.login_btn_loc)

        self.__assert_equal('账号不存在', ElementSelector.wrong_login_tip_loc)
        self.element_not_visible(*ElementSelector.wrong_login_tip_loc)

        self.change_text(*ElementSelector.username_input_loc, text='13900000088')
        self.change_text(*ElementSelector.password_input_loc, text='1234567')
        self.click_button(*ElementSelector.login_btn_loc)

        self.__assert_equal('用户名/密码错误', ElementSelector.wrong_login_tip_loc)

        self.refresh()
        self.send_text(*ElementSelector.username_input_loc, text=Keys.ENTER)
        self.send_text(*ElementSelector.password_input_loc, text=Keys.ENTER)
        self.click_button(*ElementSelector.login_btn_loc)

        self.__assert_equal('请输入6-19位账号', ElementSelector.wrong_username_tip_loc)
        self.__assert_equal('请输入6-16位密码', ElementSelector.wrong_password_tip_loc)

    def user_logout(self):
        self.click_button(*ElementSelector.index_portrait_loc)
        self.click_button(*ElementSelector.index_portrait_logout_loc)

    def __choice_point(self):
        level_two_index = PointIdIndex.level_two_index + 1
        level_three_index = PointIdIndex.level_three_index + 1
        self.click_button(
            f'//div[@class="ant-cascader-menus ant-cascader-menus-placement-bottomLeft "]'
            f'/div/ul[1]/li[{level_two_index}]',
            msg=f'二级列表第 {level_two_index} 个知识点'
        )
        self.click_button(
            f'//div[@class="ant-cascader-menus ant-cascader-menus-placement-bottomLeft "]'
            f'/div/ul[2]/li[{level_three_index}]',
            msg=f'三级列表第 {level_three_index} 个知识点'
        )

    def __choice_problem_for_homework(self):
        self.click_button(*ElementSelector.add_homework_choice_problem_loc)
        self.click_button(*ElementSelector.add_homework_all_choice_problem_loc)
        self.click_button(*ElementSelector.add_homework_operation_problem_loc, wait=True)
        self.click_button(*ElementSelector.add_homework_all_operation_problem_loc, wait=True)
        self.click_button(*ElementSelector.add_homework_problem_confirm_loc)

    teaching_package_list = ['叮当资源', '其他资源']
    answer_list = ['立即公布', '不公布', '截止']
    subject_answer_list = ['显示', '不显示', '截止时间后显示']
    course_btn_list = ['课件', '视频', '讲义']

    def add_course_simple(self, package_name):
        """
        发布课程

        :param package_name: 添加的课程类型
        :return: None
        """
        self.click_button(*ElementSelector.course_list_add_course_loc,
                          loading=True)
        # 此处功能必改，不要写死！（手动狗头~）
        # self.click_button(f'//span[text()="{package_name}"]/parent::label/span[1]',
        #                   loading=True, wait=True, msg=f' {package_name}')  # 授课包选择 待定 后期可能会加上
        if '叮当资源' == package_name:
            self.click_button(*ElementSelector.add_course_choose_course_loc)
            self.__choose_course_operation()
        else:
            self.click_button(f'//span[text()="{package_name}"]/parent::label/span[1]',
                              loading=True, wait=True, msg=f' {package_name}')  # 授课包选择其他课程 待定 后期可能会加上
        # 计划授课选择日期
        self.click_button(*ElementSelector.add_course_course_plan_switch_loc)
        day_of_week = self.__choose_course_plan()
        self.click_button(f'//div[@class="ant-row"]/div[{day_of_week + 1}]/label/span[1]',
                          f'每周{day_of_week + 1}')
        self.click_button(*ElementSelector.add_course_choose_class_loc, loading=True)
        self.click_button(*ElementSelector.add_course_choose_first_class_loc)
        self.click_button(*ElementSelector.add_course_publish_course_loc)
        self.__assert_add_course_tip('发布成功！', ElementSelector.add_course_homework_success_tip_loc)
        course_name = self.take_text(*ElementSelector.course_list_card_mode_first_course_name_loc)

        return course_name  # 返回课程名称

    def add_course_loop(self):
        """
        发布课程遍历2个资源类型添加课程

        :return: 返回添加的2个课件名称
        """
        course_name_list = []

        for name in self.teaching_package_list:
            course_name = self.add_course_simple(name)
            course_name_list.append(course_name)
        return course_name_list  # 返回课件名称列表，包含3个课件名称

    def del_course(self):
        """
        教师删除课程
        :return:
        """
        self.click_button(*ElementSelector.course_list_operation_loc)
        self.click_button(*ElementSelector.course_list_operation_delete_course_loc)
        self.click_button(*ElementSelector.confirm_btn_contains_text)
        if self.__wait_for_loading():
            self.__assert_equal('删除成功！', ElementSelector.tip_loc)

    def add_course_wrong(self):
        """
        发布课程错误操作

        :return: None
        """

        # 不选择知识点
        self.click_button(*ElementSelector.course_list_add_course_loc, loading=True)
        self.click_button(*ElementSelector.add_course_choose_class_loc)
        self.click_button(*ElementSelector.add_course_choose_first_class_loc)
        self.click_button(*ElementSelector.add_course_publish_course_loc)
        self.__assert_equal('请选择您要发布的课件包！', ElementSelector.add_course_publish_course_fail_tip_loc)  # 提示文本待定

        # 不选择班级
        self.refresh()
        self.click_button(*ElementSelector.course_list_add_course_loc, loading=True)
        self.click_button(*ElementSelector.add_course_choose_course_loc, wait=True)
        self.__choose_course_operation()
        self.click_button(*ElementSelector.add_course_delete_first_class_loc, loading=True)  # 不知道是否会默认选当前班级，待定操作
        self.click_button(*ElementSelector.add_course_publish_course_loc)
        self.__assert_equal('请选择您要发往的班级！', ElementSelector.add_course_publish_course_fail_tip_loc)  # 提示文本待定

    def preview_course(self):
        """
        预览课程操作
        :return:
        """
        self.click_button(*ElementSelector.course_list_add_course_loc,
                          loading=True)
        self.click_button(*ElementSelector.add_course_choose_course_loc)
        self.__choose_course_operation()
        # 预览课程页面操作
        self.click_button(*ElementSelector.add_course_preview_course_loc, wait=True)
        self.check_course_simple('', teacher=True, preview=True)

    def __choose_course_operation(self):
        """
        发布课程的选择课程操作
        :return:
        """
        try:
            self.click_button(*ElementSelector.choose_first_series_loc)
        except ElementNotVisibleException:
            log(self.log_path, '课程没拉到数据，刷新页面后重新操作')
            self.refresh()
            self.click_button(*ElementSelector.course_list_add_course_loc,
                              loading=True)  # 不知道刷新后是不是要重新开抽屉，暂定要重新开
            self.click_button(*ElementSelector.add_course_choose_course_loc)
            self.click_button(*ElementSelector.choose_first_series_loc)

    def add_homework_simple(self, homework_name, answer_config, difficulty=None, timing=None):
        """
        标准授课发布作业

        :param answer_config: 答案设置
        :param difficulty: 显示难度
        :param timing: 定时设置
        :param homework_name: 发布作业的名称
        :return: None
        """
        # 答案设置->输入名称->截止时间->显示难度->定时->选择系列->选择班级->选择题目->发布->检查发布是否成功
        # 选系列时，需要有班级先发布了该系列的课程，没有班级发布该系列课程则不能选该系列题目
        # 选班级只能选发布了该系列的班级
        self.click_button(*ElementSelector.add_homework_show_answer_loc, wait=True)
        self.click_button(f'//div[contains(text(),"{answer_config}")]', msg=answer_config)  # 选择显示答案
        self.send_text(*ElementSelector.add_homework_homework_name_input_loc, text=homework_name)  # 输入作业名称
        self.change_text(*ElementSelector.add_homework_time_input_loc, text=self.__input_time())
        self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)  # 输入截止时间
        if 1 == difficulty:  # 显示难度
            self.click_button(*ElementSelector.add_homework_show_diff_loc)
        if 1 == timing:  # 输入定时时间
            self.click_button(*ElementSelector.add_homework_timing_btn_loc)
            self.change_text(*ElementSelector.add_homework_time_input_loc,
                             text=self.__input_time(start=True))
            self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)
        else:
            pass
        self.click_button(*ElementSelector.add_homework_choice_series_loc)
        self.click_button(*ElementSelector.choose_homework_series_loc)  # 选择系列
        self.click_button(*ElementSelector.add_homework_choose_homework_class_loc)
        self.click_button(*ElementSelector.add_homework_choose_first_class_loc)  # 选择班级
        self.__choose_problem_operation()  # 选择题目
        self.click_button(*ElementSelector.add_homework_post_btn_loc)
        self.__assert_equal('发布成功', ElementSelector.add_course_homework_success_tip_loc)
        self.click_button(*ElementSelector.confirm_btn_contains_text)
        self.__assert_equal(homework_name, ElementSelector.homework_list_homework_name)

    def add_homework_loop(self):
        """
        遍历所有发布设置发布作业

        :return: None
        """
        for a in self.answer_list:
            for d in range(2):
                for t in range(2):
                    homework_name = f'答案{a}难度{d}定时{t}'
                    self.click_button(*ElementSelector.homework_list_add_homework_btn_loc,
                                      loading=True, wait=True)
                    self.add_homework_simple(homework_name, a, d, t)

    def add_homework_wrong(self):
        """
        标准授课发布作业错误操作

        :return: None
        """
        # 全部不填
        self.click_button(*ElementSelector.homework_list_add_homework_btn_loc,
                          loading=True, wait=True)
        self.click_button(*ElementSelector.add_homework_timing_btn_loc, wait=True)
        self.click_button(*ElementSelector.add_homework_post_btn_loc)
        mandatory_elem_list = self.elements_list(*ElementSelector.add_homework_mandatory_tip_loc,
                                                 loading=True)
        try:
            self.wait_text('这是必填项！')
            assert 5 == len(mandatory_elem_list)
        except AssertionError:
            log(self.step_log_path, '发布作业必填提示数量异常')
        finally:
            self.refresh()
        # 不选题目
        self.click_button(*ElementSelector.homework_list_add_homework_btn_loc,
                          loading=True, wait=True)
        self.click_button(*ElementSelector.add_homework_choice_series_loc, wait=True)
        self.click_button(*ElementSelector.choose_homework_series_loc)  # 选择系列
        self.change_text(*ElementSelector.add_homework_time_input_loc, text=self.__input_time())
        self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)  # 输入截止时间
        self.send_text(*ElementSelector.add_homework_homework_name_input_loc, text='不选题目')  # 输入作业名称
        self.click_button(*ElementSelector.add_homework_choose_homework_class_loc)
        self.click_button(*ElementSelector.add_homework_choose_first_class_loc)  # 选择班级
        self.click_button(*ElementSelector.add_homework_post_btn_loc)
        self.__assert_equal('未选择题目', ElementSelector.tip_loc)
        self.refresh()
        # 当前时间 < 截止时间 < 定时时间
        self.click_button(*ElementSelector.homework_list_add_homework_btn_loc,
                          loading=True, wait=True)
        self.click_button(*ElementSelector.add_homework_choice_series_loc, wait=True)
        self.click_button(*ElementSelector.choose_homework_series_loc)  # 选择系列
        self.send_text(*ElementSelector.add_homework_homework_name_input_loc, text='截止时间小于定时时间')  # 输入作业名称
        self.change_text(*ElementSelector.add_homework_time_input_loc, text=self.__input_time(later=True))  # 输入截止时间
        self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)
        self.click_button(*ElementSelector.add_homework_timing_btn_loc)  # 输入定时时间
        self.change_text(*ElementSelector.add_homework_time_input_loc,
                         text=self.__input_time(start=True))
        self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)
        self.click_button(*ElementSelector.add_homework_choose_homework_class_loc)
        self.click_button(*ElementSelector.add_homework_choose_first_class_loc)  # 选择班级
        self.__choose_problem_operation()  # 选择题目
        self.click_button(*ElementSelector.add_homework_post_btn_loc)
        self.__assert_equal('截止时间要大于定时发布时间', ElementSelector.tip_loc)
        self.refresh()
        # 输入错误的定时和截止时间
        time_list = ['定时', '截止']
        for t in time_list:
            for n in range(0, 2):
                homework_name = f'输入错误{t}时间'
                self.click_button(*ElementSelector.homework_list_add_homework_btn_loc,
                                  loading=True, wait=True)
                self.click_button(*ElementSelector.add_homework_choice_series_loc, wait=True)
                self.click_button(*ElementSelector.choose_homework_series_loc)  # 选择系列
                self.send_text(*ElementSelector.add_homework_homework_name_input_loc, text=homework_name)  # 输入作业名称
                self.__choose_problem_operation()  # 选择题目
                self.click_button(*ElementSelector.add_homework_choose_homework_class_loc, loading=True)
                self.click_button(*ElementSelector.add_homework_choose_first_class_loc)  # 选择班级
                if '定时' == t:
                    self.change_text(*ElementSelector.add_homework_time_input_loc, text=self.__input_time())
                    self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)  # 输入截止时间

                    self.click_button(*ElementSelector.add_homework_timing_btn_loc)
                    if 1 == n:
                        self.send_text(*ElementSelector.add_homework_time_input_loc,
                                       text=self.__input_time(now=True))
                    else:
                        self.send_text(*ElementSelector.add_homework_time_input_loc,
                                       text=self.__input_time(front=True))
                    self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)
                    self.click_button(*ElementSelector.add_homework_post_btn_loc)
                    self.__assert_equal('定时发布时间要大于当前时间', ElementSelector.tip_loc)
                else:
                    if 1 == n:
                        self.change_text(*ElementSelector.add_homework_time_input_loc,
                                         text=self.__input_time(now=True))
                    else:
                        self.change_text(*ElementSelector.add_homework_time_input_loc,
                                         text=self.__input_time(front=True))
                    self.send_text(*ElementSelector.add_homework_time_input_loc, text=Keys.ENTER)
                    self.click_button(*ElementSelector.add_homework_post_btn_loc)
                    self.__assert_equal('截止时间要大于当前时间',
                                        ElementSelector.tip_loc)
                self.refresh()

    def __choose_problem_operation(self):
        """
        发布作业选择知识点和题目的操作
        :return:
        """
        self.click_button(*ElementSelector.add_homework_choice_point_id_loc)
        self.click_button(*ElementSelector.add_homework_choice_point_id_sel_know_loc)
        self.__choice_point()
        try:
            self.__choice_problem_for_homework()
        except Exception as e:
            log(self.log_path, f'{e},需要再点一次选择知识点的下拉按钮')
            self.click_button(*ElementSelector.add_homework_choice_point_id_sel_know_loc)
            self.__choice_problem_for_homework()

    def teacher_check_index_course(self, course_name):
        """
        教师端检查首页课程名称
        :param course_name: 断言用课程名称
        :return:
        """
        self.click_button(*ElementSelector.bar_index_loc)
        self.__assert_equal(course_name, ElementSelector.index_course_name_loc)

    def teacher_check_index_homework(self, homework_name):
        """
        教师端检查首页作业名称
        :param homework_name: 断言用作业名称
        :return:
        """
        self.click_button(*ElementSelector.bar_index_loc)
        self.__assert_equal(homework_name, ElementSelector.index_homework_name_loc)
        self.__assert_equal('进行中', ElementSelector.index_homework_status_loc)

    def student_check_index_course(self, course_name):
        """
        学生端检查首页课件名称

        :param course_name: 断言用课件名称
        :return: None
        """
        # self.__assert_equal(course_name, ElementSelector.index_course_loc)
        self.click_button(*ElementSelector.bar_course_loc)

    def student_check_index_homework(self, homework_name):
        """
        学生端检查首页作业名称
        :param homework_name: 断言用作业名称
        :return:
        """
        self.__assert_equal(homework_name, ElementSelector.index_homework_name_loc)
        self.__assert_equal('进行中', ElementSelector.index_homework_status_loc)

    def subject_student_check_index_course(self, course_name):
        self.__assert_equal(course_name, ElementSelector.index_course_loc)
        self.click_button(*ElementSelector.checkpoint_course_loc)

    def course_field_operation(self, code, exp_output, wrong=False):
        """
        查看课件精简试炼场操作
        :return:
        """
        self.click_button(*ElementSelector.course_detail_start_course_edit_btn_loc, loading=True)
        code_input_element = self.take_element(*ElementSelector.course_detail_start_course_edit_cursor_loc)
        try:
            input_code(code, code_input_element)
        except ElementNotInteractableException:
            log(self.step_log_path, 'chromedriver不稳定，版本问题，待解决')
        else:
            self.click_button(*ElementSelector.course_detail_start_course_course_run_code_btn_loc)
            if wrong:
                self.wait_text(exp_output, *ElementSelector.course_detail_start_course_text_output_area_loc)
            else:
                self.click_button(*ElementSelector.course_detail_start_course_pic_output_btn_loc, loading=True)
                try:
                    self.element_visible(*ElementSelector.course_detail_start_course_pic_output_area_loc)
                except ElementNotVisibleException:
                    log(self.step_log_path, f'精简试炼场图形输出异常')
                finally:
                    self.click_button(*ElementSelector.course_detail_start_course_text_output_btn_loc)
                    self.wait_element_visible(*ElementSelector.course_detail_start_course_text_output_area_loc)
                    self.__assert_equal(exp_output, ElementSelector.course_detail_start_course_text_output_area_loc)
                    # 横向模式操作再次检查，最后点击收起
                    self.click_button(*ElementSelector.course_detail_start_course_edit_cross_btn_loc)
                    self.click_button(*ElementSelector.course_detail_start_course_course_run_code_btn_loc)
                    self.wait_element_visible(*ElementSelector.course_detail_start_course_text_output_area_loc)
                    self.__assert_equal(exp_output, ElementSelector.course_detail_start_course_text_output_area_loc)
                    self.click_button(*ElementSelector.course_detail_start_course_pic_output_btn_loc, loading=True)
                    try:
                        self.element_visible(*ElementSelector.course_detail_start_course_pic_output_area_loc)
                    except ElementNotVisibleException:
                        log(self.step_log_path, f'精简试炼场图形输出异常')
        finally:
            self.click_button(*ElementSelector.course_detail_start_course_putback_btn_loc)

    def check_course_simple(self, course_name, teacher=False, preview=False, check_all=False):
        """
        查看课程
        :param course_name: 查看的课件名称
        :param teacher: 是否教师查看
        :param preview: 是否预览
        :param check_all: 是否查看全部章节
        :return: None
        """
        # 进入课程第一个知识点默认展开，单独查看
        if teacher and not preview:
            self.__send_course()
        self.__check_course_operation(course_name)
        full_screen_loc = ElementSelector.course_detail_full_screen_course_loc \
            if teacher else ElementSelector.course_detail_start_study_course_loc
        self.click_button(*full_screen_loc)
        self.course_field_operation(turtle_code(), 'abc')
        self.__check_course_operation(course_name, full_screen=True)
        self.click_button(*ElementSelector.course_detail_full_screen_return_course_loc)  # 点击退出全屏
        if teacher and not preview and check_all:
            self.__check_course_traverse(course_name)

    def __check_course_traverse(self, course_name):
        """
        遍历查看课程资源的操作
        :param course_name: 课程名称
        :return:
        """
        # 选择章节，可考虑复数定位元素列表->遍历列表点击每个小节
        chap_elem_list = self.elements_list(*ElementSelector.course_detail_choose_chap_loc, loading=True)  # 章节知识点
        for c in range(2, len(chap_elem_list) + 1):  # 遍历点击章节，第一个默认展开，从第二个开始
            self.click_button(f'//div[@class="courseDetail_course-catalogue__3rF7c"]/div[2]/div[{c}]', f'第{c}章')
            time.sleep(0.2)
        sec_elem_list = self.elements_list(*ElementSelector.course_detail_choose_section_loc)  # 小节知识点
        for s in range(2, len(sec_elem_list)):  # 遍历点击小节，从第二个开始
            self.click_button(
                f'//div[@class="courseDetail_course-catalogue__3rF7c"]/descendant::li[{s}]/div[3]/div/div[1]',
                f'第{s}节', wait=True)
            self.__check_course_operation(course_name)

    def __send_course(self):
        """
        课程详情发送知识点的课程
        :return:
        """
        hover_loc, _ = ElementSelector.course_detail_send_course_name_loc
        self.wait_for_element_visible(hover_loc)
        self.click_button(*ElementSelector.course_detail_send_course_name_loc, loading=True)
        self.click_button(*ElementSelector.course_detail_send_course_loc)
        self.click_button(*ElementSelector.confirm_btn_contains_text)
        if self.__wait_for_loading():
            self.__assert_equal('发送成功', ElementSelector.tip_loc)

    def student_do_practice(self):
        """
        学生做练习题
        :return:
        """
        self.click_button(*ElementSelector.course_detail_practice_loc, loading=True)
        self.click_and_jump(2, *ElementSelector.course_detail_practice_list_problem_loc,
                            loading=True)
        choice_id_list, operation_id_list = self.__get_practice_id()
        choice_num = len(choice_id_list)
        operation_num = len(operation_id_list)
        all_num = choice_num + operation_num
        # 做作业操作
        self.__do_homework_operation(choice_num, choice_id_list, problem_type='选择')
        self.__do_homework_operation(operation_num, operation_id_list, problem_type='操作')

    def __get_practice_id(self):
        """
        获取练习题id
        :return:
        """
        course_id = self.parameter.get_user_course_list()[0]
        class_id = self.parameter.get_class_list(get_all=True)[0]
        point_id_list = [i['id'] for i in self.parameter.get_all_point_resource_id(1)]
        all_practice_id = self.parameter.get_practice_id_list(course_id, class_id, point_id_list[0])
        choice_id_list = list(filter(lambda x: x[1] == 1, all_practice_id))
        operation_id_list = list(filter(lambda x: x[1] == 2, all_practice_id))

        return choice_id_list, operation_id_list

    def student_check_course_loop(self):
        """
        学生端遍历查看列表前3个课件

        :return: None
        """
        for c in range(1, 4):
            course_name_sel = f'//div[@class="course-container-gird"]/ul/li[{c}]/div/div/div[2]/div[1]/div'
            course_name = self.take_text(course_name_sel, msg=f'第{c}个课件')
            self.click_button(course_name_sel)  # 点击课程名称进入课程详情页面
            self.check_course_simple(course_name)
            self.click_button(*ElementSelector.crumbs_loc)

    def __check_course_operation(self, course_name, full_screen=False):
        """
        课程详情选择资源操作
        :param course_name: 课程名称
        :return:
        """
        btn_list = ['课件', '视频', '讲义']
        for btn in btn_list:
            try:
                btn_loc = f'//span[text()="{btn}"]/parent::span/preceding-sibling::span/div/div[2]/span' \
                    if full_screen else f'//div[text()="{btn}"]'
                self.click_button(btn_loc, btn)
                if full_screen:  # 全屏模式继续点击课件名称
                    self.click_button(f'//span[text()="{btn}"]'
                                      f'/ancestor::div[@class="ant-tree-list-holder-inner"]/div[2]/span[3]',
                                      f'{btn}下的资源')
                if '自动上传课件' == course_name:  # 后期可能会加上自定义课件功能
                    self.click_button(
                        f'//p[text()="{btn}"]/parent::div/parent::div/parent::div/div[2]/div[2]',
                        msg=btn
                    )
            except ElementNotVisibleException:
                log(self.step_log_path, '缺少资源')
            except WebDriverException:
                log(self.step_log_path, '按钮被挡住')
                self.click_button(*ElementSelector.back_on_top_loc)
                self.click_button(f'//div[text()="{btn}"]', wait=True)
            self.__ppt_video_operation(btn, full_screen)

    def __ppt_video_operation(self, btn, full_screen=False):
        if '课件' == btn:
            try:
                frame_loc = ElementSelector.course_detail_full_screen_course_iframe_loc \
                    if full_screen else ElementSelector.course_detail_start_course_iframe_loc
                frame_elem = self.take_element(*frame_loc)
                self.switch_to_frame(frame_elem, timeout=10)
                self.switch_to_frame('wacframe', timeout=10)
                time.sleep(1)
                if self.__wait_for_loading():
                    self.element_visible(*ElementSelector.course_detail_ppt_content_loc)  # 等待PPT显示
                    self.element_visible(*ElementSelector.course_detail_ppt_pages_num_loc)
                    page_num_text = self.take_text(*ElementSelector.course_detail_ppt_pages_num_loc)
                    page_text = page_num_text[11:]
                    num_text = page_text[:2]
                    try:
                        page_num = int(num_text)
                    except ValueError:  # 没取到页码数值时等待后重新取
                        time.sleep(1)
                        page_num_text = self.take_text(*ElementSelector.course_detail_ppt_pages_num_loc)
                        page_text = page_num_text[11:]
                        num_text = page_text[:2]
                        page_num = int(num_text)
                    for s in range(page_num):
                        self.slow_click(*ElementSelector.course_detail_ppt_next_btn_loc)
            except ElementNotVisibleException:
                log(self.step_log_path, 'PPT显示异常')
            except Exception as e:
                log(self.step_log_path, f'{e},PPT加载异常')
            finally:
                self.switch_to_default_content()
        if '视频' == btn:
            try:
                video_loc = ElementSelector.course_detail_full_screen_video_loc \
                    if full_screen else ElementSelector.course_detail_video_content_loc
                self.element_visible(*video_loc)
            except ElementNotVisibleException:
                log(self.step_log_path, '视频显示异常')
        if '讲义' == btn:
            try:
                pdf_loc = ElementSelector.course_detail_full_screen_pdf_loc \
                    if full_screen else ElementSelector.course_detail_pdf_loc
                self.element_visible(*pdf_loc)
            except ElementNotVisibleException:
                log(self.step_log_path, '讲义显示异常')

    # def uni_teach_student_check_course(self, course_name):
    #     """
    #     高校版学生查看课件
    #     :param course_name:查看的课件名称
    #     :return: None
    #     """
    #     self.__assert_equal(course_name, ElementSelector.index_course_name_loc)
    #     self.click_button(*ElementSelector.uni_teach_start_course_btn_loc)
    #     self.click_button(*ElementSelector.first_course_loc)  # 点击课程名称进入课程详情页面
    #     self.__assert_equal(course_name, ElementSelector.courseCard_tit_loc)
    #
    #     btn_list = ['课件', '视频', '讲义']
    #     for btn in btn_list:
    #         self.click_button(f'//p[text()="{btn}"]', msg=btn)
    #         self.click_button(f'//p[text()="{btn}"]'
    #                           f'/parent::div/parent::div/parent::div/div[2]/div/div/div',
    #                           msg='课件下的ppt'
    #                           )
    #         self.__check_course_operation(btn)

    def student_do_homework_simple(self, homework_name):
        """
        标准授课做作业
        :param homework_name: 断言用作业名称
        :return: None
        """
        try:
            self.element_visible(*ElementSelector.homework_list_homework_name)
        except Exception as e:
            log(self.step_log_path, f'{e}学生端作业列表返回空列表')
            self.refresh()
        finally:
            self.__assert_equal(homework_name, ElementSelector.homework_list_homework_name)
            self.click_button(*ElementSelector.homework_list_homework_name)
        self.click_and_jump(1, *ElementSelector.homework_list_student_detail_go_answer_loc)
        # 获取题目id
        choice_list, operation_list = self.__get_problem_id_list()
        choice_p_num = len(choice_list)
        operation_p_num = len(operation_list)
        all_num = choice_p_num + operation_p_num
        # 做作业操作
        self.__do_homework_operation(choice_p_num, choice_list, problem_type='选择')
        self.__do_homework_operation(operation_p_num, operation_list, problem_type='操作')

        self.click_button(*ElementSelector.homework_detail_push_homework_btn_loc)
        self.click_button(*ElementSelector.confirm_btn_contains_text)
        # 3.0版本暂时没有紧急挑战，待定
        # try:
        #     self.click_button(*ElementSelector.standard_emergency_challenge_btn_loc)
        # except Exception as e:
        #     log(self.step_log_path, f'{e},没有出现紧急挑战按钮，请检查题目是否全部正确')
        # else:
        #     self.__do_challenge_operation()
        # self.switch_window(0)
        # self.refresh()

        self.wait_text('作业提交成功', *ElementSelector.tip_loc)
        self.wait_text('100', *ElementSelector.homework_list_student_detail_score_loc)  # 检查得分
        self.wait_text('A', *ElementSelector.homework_list_student_detail_level_loc)
        self.__assert_equal(
            f'{all_num}/{all_num}',
            ElementSelector.homework_list_student_detail_correct_loc)  # 作业列表的正确率检查
        self.__assert_equal(
            f'{all_num}/{all_num}',
            ElementSelector.homework_list_student_detail_completion_loc)  # 作业列表的完成率检查
        correct = self.take_text(*ElementSelector.homework_list_student_detail_correct_loc)
        completion = self.take_text(*ElementSelector.homework_list_student_detail_completion_loc)
        return completion, correct  # 返回完成率和正确率文本

    def student_do_homework_loop(self):
        """
        标准授课遍历做作业列表前3个作业
        :return: None
        """

        for a in range(1, 4):  # 依次做作业列表3个作业
            homework_name_sel = \
                f'//div[@class="leftMenu_work-card-wrap2__20Vfb"]/div/div[{a}]/div/div/ul/li[1]/span[1]'
            self.__wait_homework_and_click(homework_name_sel, a)
            self.click_and_jump(1, *ElementSelector.homework_list_student_detail_go_answer_loc)

            choice_list, operation_list = self.__get_problem_id_list()
            choice_p_num = len(choice_list)  # 选择题题目数量
            operation_p_num = len(operation_list)  # 操作题题目数量
            self.__do_homework_operation(choice_p_num, choice_list, problem_type='选择')
            s = operation_p_num - a  # 作答正确的操作题数量
            self.__do_homework_operation(s, operation_list, problem_type='操作')
            self.click_button(
                f'//div[contains(text(),"操作")]/parent::div/ul/li[{operation_p_num}]',
                msg=f'题目列表第{operation_p_num}道题'
            )
            code_input = self.take_element(*ElementSelector.homework_detail_code_view_loc)
            wrong_answer = 'wrong_answer = "wrong answer"'
            if self.__wait_for_loading():
                code_input.send_keys(wrong_answer)
            code_text_show_up = self.element_visible(*ElementSelector.homework_detail_code_text_loc)
            if code_text_show_up:
                self.click_button(*ElementSelector.homework_detail_save_run_btn_loc, loading=True)
                self.wait_text('答案评测有误', *ElementSelector.homework_detail_result_text_loc)
            self.click_button(*ElementSelector.homework_detail_push_homework_btn_loc)
            self.click_button(*ElementSelector.confirm_btn_contains_text)

            do_num = s + choice_p_num  # 做对题目总数
            complete_num = do_num + 1 if code_text_show_up else do_num  # 完成题目总数，如果最后一题没做就按最对题目算
            all_num = choice_p_num + operation_p_num  # 所有题目总数
            self.__wait_homework_and_click(homework_name_sel, a)
            try:
                self.__assert_equal(
                    f'{do_num}/{all_num}',
                    ElementSelector.homework_list_student_detail_correct_loc)  # 作业列表的正确率检查
                self.__assert_equal(
                    f'{complete_num}/{all_num}',
                    ElementSelector.homework_list_student_detail_completion_loc)  # 作业列表的完成率检查
                correct_rate = int(float('%.2f' % (do_num / all_num)) * 100)
                # 作业列表得分检查
                self.__assert_equal(correct_rate, ElementSelector.homework_list_student_detail_score_loc)

                import bisect
                # 二分法查找
                exp_homework_quality = "DCBA"[bisect.bisect_right([60, 70, 85, 100], correct_rate)]

                # 作业列表的等级检查
                self.__assert_equal(exp_homework_quality, ElementSelector.homework_list_student_detail_level_loc)
            except Exception as e:
                log(self.step_log_path, f'{e}作业完成状态和质量异常')
            self.driver.close()
            self.switch_window(0)
            self.refresh()

    def __wait_homework_and_click(self, homework_selector, homework_num):
        """
        等待作业可见并点击
        :param homework_selector: 作业名称定位器
        :param homework_num: 第几个作业
        :return:
        """
        try:
            self.element_visible(homework_selector, msg=f'第{homework_num}个作业')
        except Exception as e:
            log(self.step_log_path, f'{e}作业列表为空，刷新页面')
            self.refresh()
        finally:
            self.click_button(homework_selector, msg=f'第{homework_num}个作业')

    def __get_problem_id_list(self):
        """
        获取作业题目id列表
        :return: choice_problem_list-选择题id列表，operation_problem_list-操作题id列表
        """
        all_problem_id_list = self.parameter.student_get_problem_id_list()
        choice_problem_list = list(filter(lambda x: x[1] == 1, all_problem_id_list))
        operation_problem_list = list(filter(lambda x: x[1] == 2, all_problem_id_list))
        return choice_problem_list, operation_problem_list

    def teacher_check_homework_simple(self, homework_name, completion, correct):
        self.click_button(*ElementSelector.bar_homework_loc)
        self.click_button(*ElementSelector.homework_list_homework_name, loading=True)
        self.__assert_equal(homework_name, ElementSelector.homework_list_homework_name)
        self.element_visible(*ElementSelector.homework_list_student_list_username_loc)
        self.element_visible(*ElementSelector.homework_list_student_list_name_loc)
        self.__assert_equal(completion, ElementSelector.homework_list_student_list_completion_loc)
        self.__assert_equal(correct, ElementSelector.homework_list_student_list_correct_loc)
        self.__assert_equal('100', ElementSelector.homework_list_student_list_score_loc)
        self.__assert_equal('A', ElementSelector.homework_list_student_list_level_loc)

    # def student_do_homework_for_teach(self):
    #     """
    #     高校版做作业操作
    #
    #     :return: None
    #     """
    #     for a in range(1, 7):  # 依次做作业列表6个作业
    #         homework_name_sel = f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div'
    #         self.click_button(homework_name_sel, msg=f'第{a}个作业')
    #         self.click_button(*ElementSelector.view_code_btn_loc)
    #         self.driver.switch_to_window(a)  # 切换新弹出的table
    #
    #         problem_list = self.driver.find_elements_by_xpath('//div[@class="el-row"]/div')
    #         n = len(problem_list)
    #         s = n - a
    #         for i in range(1, s + 1):  # 依次点击题目列表的题，做题数量递减
    #             self.click_button(f'//div[@class="el-row"]/div[{i}]')
    #
    #             # DB中把code拿出来
    #             get_problem_id = self.take_text(*ElementSelector.problem_id_loc)
    #             len_text = len(get_problem_id)
    #             problem_id = get_problem_id[:len_text - 1]
    #             code = get_code(problem_id=problem_id, problem_name=None)
    #             code_input = self.take_element(*ElementSelector.uni_teach_code_view_loc)
    #             input_code(code, code_input)
    #
    #             self.click_button(*ElementSelector.save_run_btn_loc)
    #             try:
    #                 self.wait_text('通过', *ElementSelector.uni_teach_result_text_loc)
    #             except Exception as e:
    #                 log(self.step_log_path, f'{e}题目运行结果异常')
    #         problem_list[n - 1].click()
    #         code_input = self.take_element(*ElementSelector.uni_teach_code_view_loc)
    #         wrong_answer = 'wrong_answer = "wrong"'
    #         code_input.send_keys(wrong_answer)
    #         self.click_button(*ElementSelector.save_run_btn_loc, loading=True)
    #         try:
    #             self.wait_text('不通过', *ElementSelector.unpass_result_text_loc)
    #         except Exception as e:
    #             log(self.step_log_path, f'{e}错误答案运行结果异常')
    #         self.click_button(*ElementSelector.push_homework_btn_loc)
    #         self.click_button(*ElementSelector.confirm_btn_loc)
    #         self.__assert_equal('已完成', f'//div[@class="homework-container-gird"]'
    #                                    f'/ul/li[{a}]/div/div/div/div[2]/div[3]')
    #         self.click_button(homework_name_sel, msg=f'第{a}个作业')  # 点击作业名称
    #
    #         correct_rate = int((s / n) * 100)
    #         if 100 >= correct_rate >= 85:
    #             exp_homework_quality = '优秀'
    #         elif 85 > correct_rate >= 70:
    #             exp_homework_quality = '良好'
    #         elif 70 > correct_rate >= 60:
    #             exp_homework_quality = '及格'
    #         else:
    #             exp_homework_quality = '不及格'
    #
    #         self.__assert_equal(exp_homework_quality, ElementSelector.homework_quality_loc)
    #         self.__assert_equal('已完成', ElementSelector.homework_status_loc)
    #         self.go_back()

    def date_selection(self, page, name, student=False):
        """
        提供课程和作业列表页面的日期筛选

        :param page: 课程或作业页面
        :param name: 断言用名称
        :param student: 是否是学生端
        :return: None
        """
        search_loc = None
        if '作业' == page:
            search_loc = ElementSelector.student_homework_date_search_input_loc \
                if student else ElementSelector.teacher_homework_date_search_input_loc
        if '课件' == page:
            search_loc = ElementSelector.student_course_date_search_input_loc \
                if student else ElementSelector.teacher_course_date_search_input_loc
        self.click_button(*search_loc, loading=True)
        self.click_button(*ElementSelector.today_loc, wait=True)
        self.click_button(*ElementSelector.today_end_loc, wait=True)
        try:
            self.wait_text(name)
        except ElementNotVisibleException:
            log(self.step_log_path, f'没有搜索到{name}')

        self.refresh()
        self.click_button(*search_loc, loading=True)
        self.click_button(*ElementSelector.today_loc, wait=True)
        try:
            self.click_button(*ElementSelector.tomorrow_end_loc, wait=True)
        except Exception as e:
            log(self.step_log_path, f'{e}这周最后一天，改为选择下周第一天')
            self.click_button(*ElementSelector.next_week_end_loc)
        try:
            self.wait_text(name)
        except ElementNotVisibleException:
            log(self.step_log_path, f'没有搜索到{name}')

        self.refresh()
        self.click_button(*search_loc, loading=True)
        for s in range(2):
            try:
                self.click_button(*ElementSelector.tomorrow_loc, wait=True)
            except Exception as e:
                log(self.step_log_path, f'{e}这周最后一天，改为选择下周第一天')
                self.click_button(*ElementSelector.next_week_loc)
        try:
            self.element_visible(*ElementSelector.course_list_card_mode_first_course_loc)
            try:
                self.element_visible(*ElementSelector.homework_list_homework_name)
            except Exception as e1:
                log(self.step_log_path, f'{e1},筛选日期为明天，没有筛选出资源，此用例PASS')
                pass
        except Exception as e:
            log(self.step_log_path, f'{e},筛选日期为明天，没有筛选出资源，此用例PASS')
        self.refresh()

    def search_input(self, name):
        """
        课程作业列表页面搜索

        :param name: 要搜索的资源
        :return: None
        """
        self.send_text(*ElementSelector.homework_list_search_input_loc, text=name)
        self.click_button(*ElementSelector.homework_list_search_btn_loc, wait=True)
        try:
            self.wait_text(name)
        except Exception as e:
            log(self.step_log_path, f'"{e}没有搜索到指定的资源，搜索异常')

    def __assert_add_course_tip(self, exp_tip, tip_loc):
        try:
            self.__assert_equal(exp_tip, tip_loc)
        except ElementNotVisibleException:
            log(self.step_log_path, '课程发布失败')
        except BaseException as e:
            log(self.step_log_path, f'出现未知异常：{e}')
        else:
            self.click_button(*ElementSelector.add_course_publish_course_window_confirm_loc)

    def __do_homework_operation(self, num, problem_id_list, problem_type=''):
        """
        标准授课作答页面做作业操作题
        :param num: 题目数量
        :param problem_type: 题目类型，选择 或 操作
        :param problem_id_list: problem id 列表
        :return:
        """
        if not problem_type:
            raise Exception('problem_type不能为空，请传入“选择”或“操作”')
        for i in range(1, num + 1):  # 依次点击题目列表的题，做题数量递减
            try:
                self.element_visible(
                    f'//div[contains(text(),"{problem_type}")]/parent::div/ul/li[{i}]',
                    msg=f'{problem_type} 题目列表第{i}道题')
            except ElementNotVisibleException:
                log(self.step_log_path, '学生作业作答页面题目列表返回空列表')
                self.refresh()
            finally:
                self.click_button(f'//div[contains(text(),"{problem_type}")]/parent::div/ul/li[{i}]',
                                  loading=True, msg=f'{problem_type} 题目列表第{i}道题')

            problem_id, _ = problem_id_list[i - 1]  # 取出对应索引题目的problem_id
            if '操作' == problem_type:
                code = get_code(problem_id=problem_id, problem_name=None)  # 操作题查询代码
                code_input = self.take_element(*ElementSelector.homework_detail_code_view_loc)
                if self.__wait_for_loading():
                    input_code(code, code_input)

                self.click_button(*ElementSelector.homework_detail_save_run_btn_loc, loading=True)
                try:
                    self.wait_text('恭喜，答案评测通过!', *ElementSelector.homework_detail_result_text_loc)
                except Exception as e:
                    log(self.step_log_path, f'{e}DB答案错误导致{problem_id}题目评测异常')
            elif '选择' == problem_type:
                answer = get_choice(problem_id=problem_id, problem_name=None)  # 选择题查询答案
                self.click_button(f'//p[contains(text(),"{answer}")]/parent::div',
                                  loading=True, msg=f'选择题答案：{answer}')
            else:
                raise Exception('problem_type输入错误，请输入“选择”或“操作”')

    # def __do_challenge_operation(self, subject=False):
    #     """
    #     紧急挑战做题操作
    #     :return: None
    #     """
    #     for i in range(2):
    #         if subject:
    #             if i == 0:
    #                 problem_name = self.take_text(*ElementSelector.enm_problem_name_loc)
    #             else:
    #                 problem_name = self.take_text(*ElementSelector.enm_problem_name_loc_1)
    #         else:  # 标准授课取出题目名称
    #             problem_name_list = self.take_text(*ElementSelector.standard_enm_problem_name_loc)
    #             name_list = problem_name_list.split(' ')
    #             problem_name = name_list[-1]
    #         code = get_code(problem_id=None, problem_name=problem_name, challenge=True)
    #         code_input = self.take_element(*ElementSelector.code_view_loc)
    #         input_code(code, code_input)
    #         run_loc = ElementSelector.checkpoint_save_run_btn_loc \
    #             if subject else ElementSelector.standard_challenge_run_btn_loc  # 保存并评测按钮
    #         result_loc = ElementSelector.challenge_result_tip_loc \
    #             if subject else ElementSelector.standard_challenge_result_tip_loc  # 评测结果
    #         self.click_button(*run_loc, loading=True)
    #         try:
    #             self.__assert_equal('挑战成功', result_loc)
    #         except ElementNotVisibleException:
    #             log(self.step_log_path, f'题目"{problem_name}"答案错了，用挑战失败再断言一次')
    #             self.__assert_equal('挑战失败', result_loc)
    #         except Exception as e:
    #             log(self.step_log_path, f'{e}挑战结果异常')
    #         if i == 1:
    #             if subject:  # 主题授课从第2题开始点击 继续挑战 -> 换一题
    #                 for n in range(2):
    #                     self.click_button(*ElementSelector.keep_challenge_btn_loc)
    #                     self.wait_text(problem_name)
    #                     self.click_button(*ElementSelector.change_problem_btn_loc)
    #                     problem_name = self.take_text(*ElementSelector.enm_problem_name_loc_1)
    #                     code = get_code(problem_id=None, problem_name=problem_name, challenge=True)
    #                     code_input = self.take_element(*ElementSelector.code_view_loc)
    #                     input_code(code, code_input)
    #
    #                     self.click_button(*ElementSelector.checkpoint_save_run_btn_loc, loading=True)
    #                     try:
    #                         self.wait_text('挑战成功', *ElementSelector.challenge_result_tip_loc)
    #                     except ElementNotVisibleException:
    #                         log(self.step_log_path, f'题目"{problem_name}"答案错了，用挑战失败再断言一次')
    #                         self.wait_text('挑战失败', *ElementSelector.challenge_result_tip_loc)
    #                     except Exception as e:
    #                         log(self.step_log_path, f'{e}挑战结果异常')
    #         else:  # 点击保存并评测按钮之后的操作
    #             # 标准授课的“继续挑战”和主题授课的“下一道题”按钮
    #             next_btn_loc = ElementSelector.challenge_next_problem_btn_loc \
    #                 if subject else ElementSelector.standard_keep_challenge_btn_loc
    #             try:
    #                 self.click_button(*next_btn_loc)
    #             except Exception as e:  # 主题授课挑战失败时点击继续跳转后点击换一题
    #                 log(self.step_log_path,
    #                     f'答案错误挑战失败导致{e},尝试点击继续挑战按钮并点击换一题')
    #                 self.click_button(*ElementSelector.keep_challenge_btn_loc)
    #                 self.click_button(*ElementSelector.change_problem_btn_loc)
    #             try:
    #                 self.wait_text(problem_name)
    #             except Exception as e:
    #                 log(self.step_log_path, f'{e}做过的题不在题目列表中，题目列表异常')

    def add_work(self, work_name):
        """
        学生作品发布

        :param work_name: 发布的作品名称
        :return: None
        """
        if self.__wait_for_loading():
            self.change_text(*ElementSelector.works_publish_my_work_name_input_loc, text=work_name)
        self.click_button(*ElementSelector.works_publish_btn_loc)
        if self.__wait_for_loading():
            self.__assert_equal('发布成功，可在作品大厅进行查看', ElementSelector.tip_loc)

    def audit_work(self, work_name):
        """
        教师审核作品

        :param work_name: 审核的作品名称
        :return: None
        """
        self.click_button(*ElementSelector.screening_tab_loc, loading=True)
        self.click_button(f'//div[text()="{work_name}"]', loading=True, msg=work_name)
        if '直接审核作品' == work_name:
            self.click_button(*ElementSelector.direct_release_btn_loc)
            exp_tip = '发布成功'
        elif '详细审核通过作品' == work_name:
            self.click_button(*ElementSelector.detailed_review_btn_loc)
            self.click_button(*ElementSelector.pass_review_btn_loc)
            exp_tip = '审核成功！'
        else:
            self.click_button(*ElementSelector.detailed_review_btn_loc)
            self.click_button(*ElementSelector.reject_btn_loc)
            exp_tip = '驳回成功！'
        self.__assert_equal(exp_tip, ElementSelector.tip_loc)
        self.click_button(*ElementSelector.creative_space_loc)
        try:
            self.wait_text(work_name)
        except Exception as e:
            log(self.step_log_path, f'{e}作品被驳回，不在作品大厅中，此用例PASS')

    def wish_box(self):
        """
        首页意见反馈操作

        :return: None
        """
        self.click_button(*ElementSelector.fill_feedback_btn_loc, loading=True)
        self.send_text(*ElementSelector.content_textarea_loc, text='意见反馈测试')
        self.click(*ElementSelector.feedback_upload_pic_loc)
        upload_file_by_auto_it('jpg')
        if self.__wait_for_loading():
            self.click_button(*ElementSelector.confirm_btn_contains_text)
            self.__assert_equal('反馈成功！', ElementSelector.tip_loc)

    def ai_experience(self):
        """
        AI体验

        :return: None
        """
        self.click_button(*ElementSelector.image_identify_tab_loc, loading=True)
        self.click_button(*ElementSelector.upload_pic_loc, loading=True)
        upload_file_by_auto_it('jpg')

        self.__pic_image_identify_operation()
        self.click_button(*ElementSelector.car_pic_loc)
        self.__pic_image_identify_operation()

        word = '叮当码'
        for tab in range(1, 3):
            self.click_button(f'//div[@class="ant-tabs-nav ant-tabs-nav-animated"]/div[1]/div[{tab}]',
                              msg=f'切换第{tab}个tab')
            input_loc = ElementSelector.poetry_word_input_loc \
                if tab == 1 else ElementSelector.spring_festival_word_input_loc
            generate_btn_loc = ElementSelector.poetry_word_generate_btn_loc \
                if tab == 1 else ElementSelector.spring_festival_generate_btn_loc
            self.change_text(*input_loc, text=word)
            self.click_button(*generate_btn_loc)
            if tab == 1:
                try:
                    if self.__wait_for_loading():
                        self.wait_text(word, *ElementSelector.poetry_title_loc)
                except BaseException as a:
                    log(self.step_log_path, f'{a}用失败提示再次断言')
                    try:
                        self.wait_text('我还在学习', *ElementSelector.tip_loc)
                    except BaseException as e:
                        log(self.step_log_path, f'{e}创作诗句异常')
            else:
                try:
                    self.wait_for_element(*ElementSelector.couples_title_loc)
                    actual_title = self.take_text(*ElementSelector.couples_title_loc)
                    if all([actual_title]):
                        pass
                    else:
                        log(self.step_log_path, '异常：春联标题没有文本')
                except BaseException as e:
                    log(self.step_log_path, f'{e}创作春联异常')
            subject_word_loc = ElementSelector.poetry_subject_word_loc \
                if tab == 1 else ElementSelector.spring_festival_subject_word_loc
            self.slow_click(*subject_word_loc)
            actual_word = None
            if self.__wait_for_loading():
                actual_word = self.take_text(*subject_word_loc)
            if tab == 1:
                self.wait_text(actual_word, *ElementSelector.poetry_title_loc)
            else:
                try:
                    couple_text = self.take_text(*ElementSelector.couples_text_loc)
                    c_list = couple_text.split('\n')
                    if any(c_list):
                        n = 0
                        while n < len(actual_word) - 1:
                            if actual_word[n] not in c_list:
                                n += 1
                            if actual_word[n] in c_list:
                                break
                    else:
                        log(self.step_log_path, '异常：没有春联文本')
                except BaseException as e:
                    log(self.step_log_path, f'{e}创作春联异常')

    def __pic_image_identify_operation(self):
        face_output = '年龄：'
        car_license_output = '车牌号为：'
        pic_tag_output = '这个是'
        fail_output = '上传图片无法识别'
        btn_text_list = ['人脸', '车牌', '图片']
        for t in btn_text_list:
            if self.__wait_for_loading():
                self.click_button(f'//span[contains(text(),"{t}")]/parent::button',
                                  msg=f'{t}识别')
                try:
                    if '人脸' == t:
                        if self.__wait_for_loading():
                            self.wait_text(face_output, *ElementSelector.output_text_loc)
                    elif '车牌' == t:
                        if self.__wait_for_loading():
                            self.wait_text(car_license_output, *ElementSelector.output_text_loc)
                    else:
                        if self.__wait_for_loading():
                            self.wait_text(pic_tag_output, *ElementSelector.output_text_loc)
                except Exception as a:
                    log(self.step_log_path, f'{a}用失败提示再次断言')
                    try:
                        self.wait_text(fail_output, *ElementSelector.output_text_loc)
                    except Exception as e:
                        log(self.step_log_path, f'{e}图片识别异常')

    def add_account_class(self, username_teacher, teacher_name, username_student, student_name, admin_class_name,
                          pro_class_name):
        """
        管理员创建账号班级

        :param username_teacher: 创建的教师账号
        :param teacher_name: 创建的教师名称
        :param username_student: 创建的学生账号
        :param student_name: 创建的学生名称
        :param admin_class_name: 创建的行政班名称
        :param pro_class_name: 创建的课程班名称
        :return: None
        """

        # 创建教师账号
        self.click_button(*ElementSelector.teacher_manage_tab_loc)
        self.click_button(*ElementSelector.add_teacher_btn_loc)
        add_teacher_input_list = self.driver.find_elements_by_xpath(
            ElementSelector.add_input_loc)  # 创建教师表单输入框
        teacher_acc_elem = add_teacher_input_list[0]
        teacher_acc_elem.send_keys(username_teacher)
        teacher_name_elem = add_teacher_input_list[1]
        teacher_name_elem.send_keys(teacher_name)
        teacher_gender_input_list = self.driver.find_elements_by_xpath(
            ElementSelector.gender_input_loc)
        teacher_gender_elem = choice(teacher_gender_input_list)  # 随机选择1个性别
        teacher_gender_elem.click()
        teacher_position_elem = add_teacher_input_list[2]
        teacher_position_elem.send_keys('tester')
        self.click_button(*ElementSelector.confirm_btn_loc)
        self.__assert_equal('添加成功', ElementSelector.success_tip_loc)
        self.click_button(*ElementSelector.return_management_btn_loc)

        # 创建行政班
        self.click_button(*ElementSelector.class_manage_tab_loc)
        self.click_button(*ElementSelector.add_class_btn_loc)
        add_admin_class_input_list = self.driver.find_elements_by_xpath(
            ElementSelector.add_input_loc)  # 创建行政班表单输入框
        admin_class_name_elem = add_admin_class_input_list[0]
        admin_class_name_elem.send_keys(admin_class_name)
        manage_teacher_elem = add_admin_class_input_list[1]
        manage_teacher_elem.click()
        self.click_button(*ElementSelector.sel_teacher_loc)  # 管理老师下拉框选择第1个老师
        self.click_button(*ElementSelector.confirm_btn_loc)
        self.__assert_equal('添加成功', ElementSelector.success_tip_loc)
        self.click_button(*ElementSelector.return_management_btn_loc)

        # 行政班创建学生账号
        self.click_button(*ElementSelector.admin_class_list_first_loc)
        self.click_button(*ElementSelector.add_student_btn_loc)
        add_student_input_list = self.driver.find_elements_by_xpath(
            ElementSelector.add_input_loc)  # 添加学生表单输入框
        student_id_input_elem = add_student_input_list[0]
        student_id_input_elem.send_keys(username_student)
        student_name_input_elem = add_student_input_list[2]
        student_name_input_elem.send_keys(student_name)
        student_gender_input_list = self.driver.find_elements_by_xpath(
            ElementSelector.gender_input_loc)
        student_gender_elem = choice(student_gender_input_list)  # 随机选择1个性别
        student_gender_elem.click()
        self.click_button(*ElementSelector.confirm_btn_loc)
        self.__assert_equal('添加成功', ElementSelector.success_tip_loc)
        self.click_button(*ElementSelector.return_management_btn_loc)

        # 创建课程班
        self.click_button(*ElementSelector.course_manage_tab_loc)
        self.click_button(*ElementSelector.add_pro_class_btn_loc)
        add_pro_class_input_list = self.driver.find_elements_by_xpath(
            ElementSelector.add_input_loc)
        pro_class_name_input_elem = add_pro_class_input_list[0]
        pro_class_name_input_elem.send_keys(pro_class_name)
        index_list = [1, 2, 3, 4]
        index = choice(index_list)  # 随机选择1个班级配图
        class_img_elem = self.driver.find_element_by_xpath(
            f'//div[@class="item-card-center"]/ul/li[{index}]')
        class_img_elem.click()
        pro_class_manage_teacher_elem = add_pro_class_input_list[2]
        pro_class_manage_teacher_elem.click()
        self.click_button(*ElementSelector.sel_teacher_loc)  # 选择课程班管理教师
        self.click_button(*ElementSelector.confirm_btn_loc)
        self.__assert_equal('添加成功', ElementSelector.success_tip_loc)
        self.click_button(*ElementSelector.return_management_btn_loc)

        # 课程班添加学生
        self.click_button(*ElementSelector.pro_class_list_first_loc)
        self.click_button(*ElementSelector.add_student_btn_loc)
        self.click_button(*ElementSelector.sel_admin_class_loc)
        self.click_button(*ElementSelector.sel_all_student_loc)
        self.click_button(*ElementSelector.confirm_sel_btn_loc)
        self.__assert_equal('成功添加！', ElementSelector.add_success_tip_loc)

    def add_resources(self):
        """
        教师添加资源

        :return: None
        """

        resource_name = '自动上传课件'
        options_list = ['校内公开', '仅自己']
        for visibility in options_list:
            self.click_button(*ElementSelector.want_publish_btn_loc,
                              loading=True)
            self.click_button(*ElementSelector.visibility_sel_loc, loading=True)
            self.click_button(f'//span[text()="{visibility}"]', msg=visibility)

            self.send_text(
                *ElementSelector.resource_name_input_loc,
                text=resource_name)

            resource_img_list = self.driver.find_elements_by_xpath(
                ElementSelector.resource_img_loc)
            resource_img_elem = choice(resource_img_list)
            resource_img_elem.click()
            self.send_text(
                *ElementSelector.course_describe_loc,
                text=resource_name)

            format_list = ['ppt', 'video', 'word', 'doc']
            for f in format_list:
                if self.__wait_for_loading():
                    upload_btns = self.driver.find_elements_by_xpath(
                        ElementSelector.upload_file_btns_loc)
                    upload_btn = upload_btns[0]
                    upload_btn.click()
                    upload_file_by_auto_it(f)

            i = 0
            for f in format_list:
                if self.__wait_for_loading():
                    continue_upload_btns = self.driver.find_elements_by_xpath(
                        ElementSelector.continue_to_upload_loc)
                    continue_upload_btn = continue_upload_btns[i]
                    continue_upload_btn.click()
                    upload_file_by_auto_it(f)
                i += 1

            """
            #win32gui文件上传
            upload_btns = self.driver.find_elements(*ElementSelector.upload_file_btns_loc, 
            tag=False, loading=True)
            upload_btn = upload_btns[0]
            upload_btn.click()
            dialog = win32gui.FindWindow('#32770', u'打开')
            combo_box_ex = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
            combo_box = win32gui.FindWindowEx(combo_box_ex, 0, 'ComboBox', None)
            edit = win32gui.FindWindowEx(combo_box, 0, 'Edit', None)
            button = win32gui.FindWindowEx(dialog, 0, 'Button', None)
            win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, 'E:\\测试文件\\ppt\\ppt1.pptx')
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
            time.sleep(1)

            #上帝之眼文件上传
            path = os.path.dirname(os.getcwd())
            j_path = get_default_jvm_path()
            jvm_path = r'C:\Program Files (x86)\Java\jdk1.8.0_151\jre\bin\client\jvm.dll'
            #jvm_path = r"C:\Program Files\Java\jdk1.8.0_191\jre\bin\server\jvm.dll"
            jar_path = '-Djava.class.path=' + path + r'\base\libs\sikulixapi.jar'
            log(self.step_log_path, j_path, jar_path)
            jpype.startJVM(j_path, jar_path)
            Screen = jpype.JClass('org.sikuli.script.Screen')
            screen = Screen()
            input_path = path + r'base\images\input.png'
            screen.click(input_path)
            ppt1 = path + '\\base\\files\\ppt1.pptx'
            screen.type(input_path, ppt1)
            open_path = path + r'\base\images\open.png'
            screen.click(open_path)
            time.sleep(2)
            jpype.shutdownJVM()
            """

            self.click_button(*ElementSelector.publish_btn_loc, loading=True)
            self.wait_text('添加成功')
            self.click_button(*ElementSelector.back_button_loc)

    def add_draft(self):
        """
        保存多个个草稿

        :return: None
        """
        for n in range(0, 10):
            self.click_and_jump(1, *ElementSelector.test_field_btn_loc)
            self.change_text(*ElementSelector.draft_name_input_loc, text=n)
            self.click_button(*ElementSelector.save_btn_loc, loading=True)
            self.__assert_equal('草稿保存成功，请在 “文件-打开” 或 “草稿” 中查看。', ElementSelector.save_success_tip_loc)
            self.driver.close()
            self.switch_window(0)

    def do_test_field(self, model):
        """
        试炼场标准编辑turtle和pygame

        :param model: 传入turtle或pygame
        :return: None
        """
        if self.__wait_for_loading():
            self.wait_element_visible(*ElementSelector.code_input_area_loc)
        code_input_element = self.take_element(*ElementSelector.ace_text_input_loc)
        code_input_element.clear()
        if 'turtle' == model:
            code = turtle_code()
            input_code(code, code_input_element)
        elif 'pygame' == model:
            code = pygame_code()
            input_code(code, code_input_element)
        self.click_button(*ElementSelector.run_code_btn_loc)

        if 'pygame' == model:
            try:
                self.click_button(*ElementSelector.close_pygame_btn_loc)
            except Exception as e:
                try:
                    out_text = self.take_text(*ElementSelector.text_out_area_loc)
                    log(self.step_log_path, f'报错为{out_text}')
                except Exception as a:
                    log(self.step_log_path, f'{a}文本输出定位失败')
                log(self.step_log_path, f'{e}pygame代码运行失败，试炼场pygame异常')
        else:
            try:
                self.wait_text('abc', *ElementSelector.text_out_area_loc)
            except Exception as e:
                log(self.step_log_path, e)
        self.change_text(*ElementSelector.draft_name_input_loc, text=f'{model}测试')
        self.click_button(*ElementSelector.save_btn_loc)
        self.__assert_equal('草稿保存成功，请在 “文件-打开” 或 “草稿” 中查看。', ElementSelector.save_success_tip_loc)

    def multiple_files_test_field(self, file_name, draft_name, output):
        """
        试炼场多文件代码

        :param file_name: 添加的模块名称
        :param draft_name: 草稿名称
        :param output: 预期输出
        :return: None
        """
        self.click_button(*ElementSelector.add_file_btn_loc)
        self.send_text(*ElementSelector.create_file_input_loc, text=file_name)
        self.click_button(*ElementSelector.add_file_confirm_btn_loc)
        code_list = multiple_files_code(file_name, output)
        main_code = code_list[0]
        hey_code = code_list[1]
        code_input_element = self.take_element(*ElementSelector.ace_text_input_loc)
        input_code(hey_code, code_input_element)
        self.click_button(*ElementSelector.main_file_tab_loc)
        input_code(main_code, code_input_element)
        self.click_button(*ElementSelector.run_code_btn_loc)
        try:
            self.__assert_equal(output, ElementSelector.text_out_area_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}运行失败，输出错误')
        self.change_text(*ElementSelector.draft_name_input_loc, text=draft_name)
        self.click_button(*ElementSelector.save_btn_loc)
        self.__assert_equal('草稿保存成功，请在 “文件-打开” 或 “草稿” 中查看。', ElementSelector.save_success_tip_loc)

    def open_file(self, output):
        """
        试炼场打开草稿文件

        :param output: 预期输出
        :return: None
        """
        self.click_button(*ElementSelector.my_draft_btn_loc, loading=True)
        draft_name = self.take_text(*ElementSelector.first_draft_loc)
        self.click_button(*ElementSelector.first_draft_loc)
        self.click_button(*ElementSelector.run_code_btn_loc)
        try:
            opened_draft_name = self.take_attribute(*ElementSelector.draft_name_input_loc, 'value')
            self.assert_equal(opened_draft_name, draft_name, '文本框中草稿名称与打开草稿名称不符')
        except Exception as e:
            log(self.step_log_path, f'{e}文本框中草稿名称异常')
        try:
            self.__assert_equal(output, ElementSelector.text_out_area_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}运行失败，输出错误')

    def jieba(self):
        """
        试炼场jieba
        :return:
        """
        self.switch_window(1)

    def three_dimensional(self):
        """
        试炼场3D建模

        :return: None
        """
        self.click_button(*ElementSelector.type_choose_loc, loading=True)
        self.click_button(*ElementSelector.ck_type_loc)
        code = three_dimensional_code()
        code_input_element = self.take_element(*ElementSelector.ace_text_input_loc)
        code_input_element.clear()
        input_code(code, code_input_element)
        self.click_button(*ElementSelector.run_code_btn_loc)
        try:
            self.element_visible(*ElementSelector.ck_type_output_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}3D建模异常，没有输出')
        self.change_text(*ElementSelector.draft_name_input_loc, text='3D建模测试')
        self.click_button(*ElementSelector.save_btn_loc, loading=True)
        self.__assert_equal('草稿保存成功，请在 “文件-打开” 或 “草稿” 中查看。', ElementSelector.save_success_tip_loc)

    def robot(self):
        """
        试炼场机器人

        :return: None
        """
        self.switch_window(1)
        self.click_button(*ElementSelector.type_choose_loc, loading=True)
        self.click_button(*ElementSelector.ck_type_loc)
        self.click_button(*ElementSelector.robot_config_btn_loc)
        self.hover_on_element(*ElementSelector.robot_box_loc)
        self.click_button(*ElementSelector.connect_robot_btn_loc)
        try:
            self.__assert_equal('恭喜你，连接成功！', ElementSelector.tip_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}连接机器人异常')
        self.click_button(*ElementSelector.close_robot_config_btn_loc)
        code = robot_code()
        code_input_element = self.take_element(*ElementSelector.ace_text_input_loc)
        code_input_element.clear()
        input_code(code, code_input_element)
        self.click_button(*ElementSelector.run_code_btn_loc)
        try:
            self.element_visible(*ElementSelector.robot_img_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}机器人图像异常')

    def check_error(self):
        """
        试炼场
        :return:
        """
        code_input_element = self.take_element(*ElementSelector.ace_text_input_loc)
        code_input_element.clear()
        code = wrong_code()
        input_code(code, code_input_element)
        self.click_button(*ElementSelector.run_code_btn_loc)
        self.wait_text('Error', *ElementSelector.text_out_area_loc)

    def submit_work(self, work_name):
        """
        试炼场发布作品

        :param work_name: 发布的作品名称
        :return: None
        """
        self.change_text(*ElementSelector.draft_name_input_loc, text=work_name)
        code = turtle_code()
        code_input_element = self.take_element(*ElementSelector.ace_text_input_loc)
        code_input_element.clear()
        input_code(code, code_input_element)
        self.click_button(*ElementSelector.run_code_btn_loc)
        try:
            self.wait_text('abc', *ElementSelector.text_out_area_loc)
        except ElementNotVisibleException:
            log(self.step_log_path, '试炼场代码运行异常')
        self.click_button(*ElementSelector.save_btn_loc)
        self.__assert_equal('草稿保存成功，请在 “文件-打开” 或 “草稿” 中查看。', ElementSelector.save_success_tip_loc)
        self.click_button(*ElementSelector.submit_work_btn_loc)
        self.click_button(*ElementSelector.work_describe_input_loc)
        self.send_text(*ElementSelector.work_describe_input_loc, '测试试炼场发布作品')
        self.element_not_visible(*ElementSelector.save_success_tip_loc)
        self.click_button(*ElementSelector.confirm_btn_equal_text)
        if self.__wait_for_loading():
            self.wait_text('发布成功，可在作品大厅进行查看', *ElementSelector.save_success_tip_loc)

    def upload_material(self):
        """
        试炼场上传素材

        :return: None
        """
        if self.__wait_for_loading():
            self.hover_and_click(ElementSelector.tools_box_loc,
                                 ElementSelector.material_lib_loc)
        self.click_button(*ElementSelector.add_classify_btn)
        self.send_text(*ElementSelector.classify_name_input, text='分类测试')
        self.click_button(*ElementSelector.confirm_classify_btn)
        self.click_button(*ElementSelector.upload_material_btn_loc,
                          loading=True, wait=True)
        upload_file_by_auto_it('jpg')
        try:
            self.__assert_equal('上传成功!', ElementSelector.tip_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}上传素材异常')

    def edit_material_name(self, material_name):
        """
        试炼场编辑素材名称

        :param material_name: 编辑的名称
        :return: None
        """
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.by import By

        e = self.driver.find_element(By.XPATH, ElementSelector.material_name_loc)
        self.driver.w3c = False  # 框架的hover_on_element问题未得到解决，暂用此方法
        ActionChains(self.driver).move_to_element(e).perform()
        self.click_button(*ElementSelector.edit_name_btn_loc)
        time.sleep(1)
        self.change_text(*ElementSelector.material_name_input_loc, text=material_name)
        self.click_button('.button', loading=True)
        self.click_button(*ElementSelector.upload_confirm_btn_loc)
        try:
            self.wait_text(material_name, *ElementSelector.material_name_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}编辑素材名称异常')

    def delete_material(self):
        """
        试炼场删除素材

        :return: None
        """
        self.click_button(*ElementSelector.delete_material_btn_loc)
        self.click_button(*ElementSelector.upload_confirm_btn_loc)
        try:
            self.__assert_equal('删除素材成功', ElementSelector.tip_loc)
        except Exception as e:
            log(self.step_log_path, f'{e}删除素材异常')

    def del_classify(self):
        """
        试炼场删除素材分类
        :return:
        """

    def __input_code(self, code, code_input):
        self.send_text(code_input, text=(Keys.CONTROL, 'a'))
        self.send_text(code_input, text=Keys.BACKSPACE)
        for c in code.split("\n"):
            self.send_text(code_input, text=c)
            if c != "":
                self.send_text(code_input, text=Keys.ESCAPE)
                self.send_text(code_input, text=Keys.ENTER)
                self.send_text(code_input, text=Keys.HOME)
                self.send_text(code_input, text=(Keys.SHIFT, Keys.TAB))
            else:
                self.send_text(code_input, text=Keys.ENTER)

    @staticmethod
    def __input_time(now=False, front=False, start=False, later=False):
        """
        提供公用的输入时间，格式为YYYY-MM-DD hh:mm:ss
        :param now: 返回当前时间
        :param front: 返回10分钟前
        :param start: 返回30分钟后
        :param later: 返回10分钟后
        :return: 默认返回40分钟后
        """
        time_diff = datetime.timedelta(minutes=10)
        now_time = datetime.datetime.now()
        if now:
            a_time = now_time
        elif front:
            a_time = now_time - time_diff
        elif start:
            a_time = now_time + time_diff * 3
        elif later:
            a_time = now_time + time_diff
        else:
            a_time = now_time + time_diff * 4
        b_time = int(a_time.timestamp())
        time_local = time.localtime(b_time)
        i_time = time.strftime('%Y-%m-%d %H:%M:%S', time_local)

        return i_time

    @staticmethod
    def __choose_course_plan():
        now_time_str = time.strftime('%Y%m%d')
        week_day_index = weekday(int(now_time_str[:4]), int(now_time_str[4:6]), int(now_time_str[6:8]))
        # lis = ['每周一', '每周二', '每周三', '每周四', '每周五', '每周六', '每周日', ]
        # dic = dict(enumerate(lis))
        # day = dic[week_day_index]
        return week_day_index

    def __wait_for_loading(self):
        """
        等待遮罩层消失
        :return:
        """
        for i in range(2):
            self.wait_for_element_absent(
                '//div[@class="ant-spin ant-spin-spinning ant-spin-show-text"]'
            )
            self.wait_for_element_absent(
                '//div[@class="ant-spin-container ant-spin-blur"]'
            )
            time.sleep(0.25)

        return self.wait_for_element_absent(
            '//div[@class="ant-spin ant-spin-spinning ant-spin-show-text"]'
        )

    def __upload_file(self, input_element, file_type):
        """
        上传文件
        :param file_type:
        :return:
        """

    def __assert_equal(self, text, text_loc):
        """
        断言文本相等

        :param text: 期望文本
        :param text_loc: 实际文本定位器
        :return: None
        """
        actual_text = self.take_text(*text_loc)
        log(self.step_log_path, f'期望： "{text}", 实际： "{actual_text}"')
        try:
            self.assert_equal(str(text), actual_text)
        except AssertionError:
            log(self.step_log_path, f'{text}断言异常，与期望不符,')
        except Exception as e:
            log(self.step_log_path, str(e))
