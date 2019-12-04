import time
import datetime

from seleniumbase import BaseCase
from selenium.webdriver.common.keys import Keys

from ui_auto.base.data import Data, PointIdIndex
from ui_auto.common.get_answer import ParameterForOthers
from ui_auto.common.mysql import get_code, get_choice
from ui_auto.common.upload_file import upload_file_by_auto_it
from ui_auto.common.picture_list_code import turtle_code
from ui_auto.common.input_code import input_code
from ui_auto.page_object.element_loc import ElementSelector


class BaseTestCase(BaseCase):

    def setUp(self, masterqa_mode=False):
        super(BaseTestCase, self).setUp()
        self.url_for_edu = Data().ip_for_edu()
        self.url_for_uni = Data().ip_for_uni_teach()
        self.wait = self.__wait_for_loading()
        self.parameter = ParameterForOthers(identity='student')

    def tearDown(self):
        # Add custom tearDown code for your tests BEFORE the super().tearDown()
        super(BaseTestCase, self).tearDown()

    def click_button(self, btn_loc, wait=False):
        """
        单独点击一个按钮

        :param btn_loc: 按钮定位器
        :param wait: 是否等待
        :return: None
        """
        if wait:
            self.slow_click(btn_loc)
        else:
            self.click(btn_loc)

    def click_and_jump(self, btn_loc, handle_num):
        """
        点击按钮并跳转新开tab
        :param btn_loc: 按钮定位器
        :param handle_num: 窗口句柄索引号
        :return: None
        """
        self.click(btn_loc)
        self.switch_to_window(handle_num)

    def login(self, username, name, password, teacher_assert=False, student_assert=False):
        self.maximize_window()
        self.open(self.url_for_edu)
        self.update_text(ElementSelector.username_input_loc, new_value=username)
        self.update_text(ElementSelector.password_input_loc, new_value=password)
        self.click(ElementSelector.save_login_loc)
        self.click(ElementSelector.login_btn_loc)

        if teacher_assert:
            self.__assert_equal(name, ElementSelector.index_teacher_name_loc)

        if student_assert:
            self.__assert_equal(name, ElementSelector.index_student_name_loc)

    def login_for_uni_teach(self, username, name, password, teacher_assert=False, student_assert=False):
        self.open(self.url_for_uni)
        self.update_text(ElementSelector.username_input_loc, new_value=username)
        self.update_text(ElementSelector.password_input_loc, new_value=password)
        self.click(ElementSelector.save_login_loc)
        self.click(ElementSelector.uni_teach_login_btn_loc)

        if teacher_assert:
            self.__assert_equal(name, ElementSelector.index_teacher_name_loc)

        if student_assert:
            self.__assert_equal(name, ElementSelector.index_student_name_loc)

    def user_login_wrong(self, enable_assert=False):
        self.open(self.url_for_edu)
        self.update_text(ElementSelector.username_input_loc, new_value='152084519491')
        self.update_text(ElementSelector.password_input_loc, new_value='123456')
        self.click(ElementSelector.save_login_loc)
        self.click(ElementSelector.uni_teach_login_btn_loc)

        if enable_assert:
            exp_tip = '用户不存在'
            self.__assert_equal(exp_tip, ElementSelector.wrong_login_tip_loc)
            self.wait_for_element_not_visible(ElementSelector.wrong_login_tip_loc)

        self.update_text(ElementSelector.username_input_loc, new_value='13900000088')
        self.update_text(ElementSelector.password_input_loc, new_value='1234567')
        self.click(ElementSelector.save_login_loc)
        self.click(ElementSelector.uni_teach_login_btn_loc)

        if enable_assert:
            exp_tip = '用户名/密码错误'
            self.__assert_equal(exp_tip, ElementSelector.wrong_login_tip_loc)

        self.refresh()
        self.send_keys(ElementSelector.username_input_loc, text=Keys.ENTER)
        self.send_keys(ElementSelector.password_input_loc, text=Keys.ENTER)
        self.click(ElementSelector.login_btn_loc)

        if enable_assert:
            exp_username_tip = '用户账号在5至18位之间'
            self.__assert_equal(exp_username_tip, ElementSelector.wrong_username_tip_loc)
            exp_password_tip = '请输入6-16位的密码'
            self.__assert_equal(exp_password_tip, ElementSelector.wrong_password_tip_loc)

    def user_logout(self):
        self.click(ElementSelector.head_portrait_loc)
        self.click(ElementSelector.logout_btn_loc)

    def __choice_point(self, subject=False):
        if subject:
            s_list = self.find_elements(ElementSelector.s1_loc)
            s1_btn = s_list[PointIdIndex.checkpoint_level_one_index]
            s1_btn.click()
            level_two_elem_list = self.find_elements(ElementSelector.level_two_loc)
            level_two_elem = level_two_elem_list[PointIdIndex.checkpoint_level_two_index]
            level_two_elem.click()
        else:
            self.slow_click(f'//div[@class="el-cascader-panel"]/div[1]/div[1]/ul/li[{PointIdIndex.level_one_index}]')
            self.click(f'//div[@class="el-cascader-panel"]/div[2]/div[1]/ul/li[{PointIdIndex.level_two_index}]')
            self.click(f'//div[@class="el-cascader-panel"]/div[3]/div[1]/ul/li[{PointIdIndex.level_three_index}]')

    def __choice_problem_for_homework(self):
        self.click(ElementSelector.choice_problem_loc)
        self.click(ElementSelector.choice_all_btn_loc)
        self.click(ElementSelector.operation_problem_loc)
        self.click(ElementSelector.choice_all_btn_loc)
        self.click(ElementSelector.confirm_publish_btn_loc)

    teaching_package_list = ['叮当资源', '校本资源', '我的资源']
    answer_list = ['立即公布', '不公布', '截止时间公布']

    def add_course_simple(self, package_name):
        """
        标准授课添加课件

        :param package_name: 添加的课件类型
        :param enable_assert: 是否检查
        :return: None
        """
        self.slow_click(ElementSelector.add_course_loc)
        self.slow_click(f'//span[text()="{package_name}"]/parent::label/span[1]')  # 授课包选择
        if '叮当资源' == package_name:
            self.click(ElementSelector.selKnow_loc)
            self.__choice_point()
            try:
                self.click(ElementSelector.choice_course_btn_loc)
            except Exception as e:
                self.click(ElementSelector.selKnow_loc)
                self.click(ElementSelector.choice_course_btn_loc)
        else:
            self.click(ElementSelector.choice_course_btn_loc)
        self.slow_click(ElementSelector.choice_class_btn_loc)
        self.click(ElementSelector.add_publish_btn)
        self.click(ElementSelector.add_btn_loc)
        self.__assert_add_course_tip('成功添加课件！', ElementSelector.succ_tip_loc,
                                     ElementSelector.repeated_tip_confirm_loc)
        self.click(ElementSelector.back_btn_loc)
        course_name = self.get_text(ElementSelector.course_name_loc)

        return course_name  # 返回课程名称

    def add_course_loop(self):
        """
        标准授课遍历3中资源类型添加课程

        :return: 返回添加的3个课件名称
        """
        course_name_list = []

        for name in self.teaching_package_list:
            course_name = self.add_course_simple(name)
            course_name_list.append(course_name)
        return course_name_list  # 返回课件名称列表，包含3个课件名称

    def add_course_wrong(self):
        """
        标准授课添加课件错误操作

        :param enable_assert: 是否检查
        :return: None
        """

        # 不选择知识点
        self.click(ElementSelector.add_course_loc)
        self.click(ElementSelector.choice_class_btn_loc)
        self.click(ElementSelector.add_publish_btn)
        self.click(ElementSelector.publish_btn_loc)
        self.__assert_equal('请选择您要发布的课件包！', ElementSelector.fail_tip_loc)

        # 不选择班级
        self.refresh()
        self.click(ElementSelector.selKnow_loc)
        self.__choice_point()
        try:
            self.click(ElementSelector.choice_btn_loc)
        except Exception as e:
            self.click(ElementSelector.selKnow_loc)
            self.click(ElementSelector.choice_btn_loc)
        self.click(ElementSelector.add_publish_btn)
        self.click(ElementSelector.publish_btn_loc)
        self.__assert_equal('请选择您要发往的班级！', ElementSelector.fail_tip_loc)

    def __assert_add_course_tip(self, exp_tip, tip_loc, repeated_tip_confirm_loc):
        try:
            self.find_element(tip_loc)
        except Exception:
            print('已有其他教师在该班级发布这个课件，点击确定继续发布')
            self.click(repeated_tip_confirm_loc)
            self.__assert_equal(exp_tip, tip_loc)
        except BaseException as e:
            print(f'出现未知异常：{e}')
        else:
            self.__assert_equal(exp_tip, tip_loc)

    def add_homework_simple(self, homework_name, answer_config, timing=None):
        """
        标准授课发布作业

        :param answer_config: 答案设置
        :param timing: 定时设置
        :param homework_name: 发布作业的名称
        :param enable_assert: 是否检查
        :return: None
        """
        self.add_text(ElementSelector.homework_name_input_loc, text=homework_name)
        self.click(ElementSelector.choice_pointId_btn_loc)
        self.click(ElementSelector.sel_know_loc)
        self.__choice_point()
        try:
            self.__choice_problem_for_homework()
        except Exception as e:
            self.click(ElementSelector.sel_know_loc)
            self.__choice_problem_for_homework()
        self.slow_click(ElementSelector.choice_class_btn_loc)
        self.click(ElementSelector.show_answer_loc)
        self.click(f'//span[text()="{answer_config}"]/parent::li')
        if 1 == timing:
            self.click(ElementSelector.timing_btn_loc)
            self.update_text(ElementSelector.timing_input_loc,
                             new_value=self.__input_time(start=True))
            self.add_text(ElementSelector.timing_input_loc, text=Keys.ENTER)
        else:
            pass
        self.update_text(ElementSelector.end_time_input_loc, new_value=self.__input_time())
        self.send_keys(ElementSelector.end_time_input_loc, text=Keys.ENTER)
        self.click(ElementSelector.public_homework_btn_loc)
        self.__assert_equal('成功添加作业！', ElementSelector.succ_tip_loc)
        self.__assert_equal(homework_name, ElementSelector.homework_list_name)

    def add_homework_loop(self):
        """
        遍历所有发布设置发布作业

        :return: None
        """
        for a in self.answer_list:
            for t in range(2):
                homework_name = f'答案{a}定时{t}'
                self.click_button(ElementSelector.add_homework_btn_loc)
                self.add_homework_simple(homework_name, a, timing=t)

    def add_homework_wrong(self):
        """
        标准授课发布作业错误操作

        :return: None
        """
        for i in ['名称', '知识点', '班级']:
            homework_name = f'{i}不输入'
            self.click_button(ElementSelector.add_homework_btn_loc, wait=True)
            if '名称' == i:
                self.click(ElementSelector.choice_pointId_btn_loc)
                self.click(ElementSelector.sel_know_loc)
                self.__choice_point()
                self.__choice_problem_for_homework()
                self.slow_click(ElementSelector.choice_class_btn_loc)
                self.click(ElementSelector.public_homework_btn_loc)
                self.__assert_equal('请输入作业名称！', ElementSelector.fail_tip_loc)
            elif '知识点' == i:
                self.add_text(ElementSelector.homework_name_input_loc, text=homework_name)
                self.click(ElementSelector.choice_class_btn_loc)
                self.click(ElementSelector.public_homework_btn_loc)
                self.__assert_equal('请通过知识点选出作业题目！', ElementSelector.fail_tip_loc)
            else:
                self.add_text(ElementSelector.homework_name_input_loc, text=homework_name)
                self.click(ElementSelector.choice_pointId_btn_loc)
                self.click(ElementSelector.sel_know_loc)
                self.__choice_point()
                self.__choice_problem_for_homework()
                self.click(ElementSelector.public_homework_btn_loc)
                self.assert_equal('请选择您要发往的班级！', ElementSelector.fail_tip_loc)
            self.go_back()

        time_list = ['定时', '截止']
        for t in time_list:
            for n in range(0, 2):
                homework_name = f'输入错误{t}时间'
                self.click_button(ElementSelector.add_homework_btn_loc)
                self.add_text(ElementSelector.homework_name_input_loc, text=homework_name)
                self.click(ElementSelector.choice_pointId_btn_loc)
                self.click(ElementSelector.sel_know_loc)
                self.__choice_point()
                self.__choice_problem_for_homework()
                self.slow_click(ElementSelector.choice_class_btn_loc)
                if '定时' == t:
                    self.click(ElementSelector.timing_btn_loc)
                    if 1 == n:
                        self.add_text(ElementSelector.timing_input_loc, text=self.__input_time(now=True))
                    else:
                        self.add_text(ElementSelector.timing_input_loc, text=self.__input_time(front=True))
                    self.send_keys(ElementSelector.timing_input_loc, text=Keys.ENTER)
                    self.update_text(ElementSelector.end_time_input_loc, new_value=self.__input_time())
                    self.send_keys(ElementSelector.end_time_input_loc, text=Keys.ENTER)
                    self.click(ElementSelector.public_homework_btn_loc)
                    self.__assert_equal('定时时间要大于当前时间！', ElementSelector.fail_tip_loc)
                else:
                    if 1 == n:
                        self.update_text(ElementSelector.end_time_input_loc,
                                         new_value=self.__input_time(now=True))
                    else:
                        self.update_text(ElementSelector.end_time_input_loc,
                                         new_value=self.__input_time(front=True))
                    self.send_keys(ElementSelector.end_time_input_loc, text=Keys.ENTER)
                    self.click(ElementSelector.public_homework_btn_loc)
                    self.__assert_equal('截止时间要大于当前时间和定时时间！', ElementSelector.fail_tip_loc)
                self.go_back()

    def student_check_index_course(self, course_name):
        self.__assert_equal(course_name, ElementSelector.index_course_name_loc)
        self.click_button(ElementSelector.standard_course_btn_loc)

    def student_check_course_simple(self, course_name):
        """
        标准授课学生查看课件
        :param course_name: 查看的课件名称
        :return: None
        """
        self.__course_field_operation(turtle_code(), 'abc')

        btn_list = ['课件', '视频', '讲义']
        for btn in btn_list:
            try:
                self.click(f'//p[text()="{btn}"]')
                if '自动上传课件' == course_name:
                    self.click(
                        f'//p[text()="{btn}"]/parent::div/parent::div/parent::div/div[2]/div[2]')
                else:
                    self.click(
                        f'//p[text()="{btn}"]/parent::div/parent::div/parent::div/div[2]')
            except Exception as e:
                print(f'{e}缺少资源')
            self.__check_course_operation(btn)

    def student_check_course_loop(self):
        """
        学生端遍历查看列表前3个课件

        :return: None
        """
        for c in range(1, 4):
            course_name_sel = f'//div[@class="course-container-gird"]/ul/li[{c}]/div/div/div[2]/div[1]/div'
            course_name = self.get_text(course_name_sel)
            self.click(course_name_sel)  # 点击课程名称进入课程详情页面
            self.student_check_course_simple(course_name)
            self.click(ElementSelector.crumbs_loc)

    def uni_teach_student_check_course(self, course_name):
        """
        高校版学生查看课件
        :param course_name:查看的课件名称
        :param enable_assert: 是否检查
        :return: None
        """
        self.__assert_equal(course_name, ElementSelector.index_course_name_loc)
        self.click(ElementSelector.uni_teach_start_course_btn_loc)
        self.click(ElementSelector.first_course_loc)  # 点击课程名称进入课程详情页面
        self.__assert_equal(course_name, ElementSelector.courseCard_tit_loc)

        btn_list = ['课件', '视频', '讲义']
        for btn in btn_list:
            self.click(f'//p[text()="{btn}"]')
            self.click(f'//p[text()="{btn}"]'
                       f'/parent::div/parent::div/parent::div/div[2]/div/div/div')
            self.__check_course_operation(btn)

    def __check_course_operation(self, btn):
        if '课件' == btn:
            self.driver.switch_to_frame(self.driver.find_elements_by_tag_name('iframe')[0])
            self.driver.switch_to_frame('wacframe')
            try:
                page_num_text = self.get_text(ElementSelector.ppt_pages_num_loc)
                page_text = page_num_text[11:]
                num_text = page_text[:2]
                page_num = int(num_text)
                for s in range(page_num):
                    self.slow_click(ElementSelector.ppt_next_btn_loc)
            except Exception as e:
                print(f'{e}PPT显示异常')
            finally:
                self.switch_to_default_content()

    def student_do_homework_simple(self, homework_name):
        """
        标准授课做作业

        :param homework_name: 断言用作业名称
        :param enable_assert: 是否检查
        :return: None
        """
        try:
            self.wait_for_element_visible(ElementSelector.homework_to_do_loc)
        except Exception as e:
            print(f'{e}学生端作业列表返回空列表')
            self.refresh()
        finally:
            self.__assert_equal(homework_name, ElementSelector.homework_to_do_loc)
            self.click(ElementSelector.homework_to_do_loc)
        self.click(ElementSelector.view_code_btn_loc)
        self.switch_to_window(1)

        eval_id_list = self.parameter.get_eval_id(traditional_teach=True)
        eval_id = eval_id_list[0]

        choice_problem_id_list = self.parameter.get_choice_problem_id_for_ui(eval_id)
        c_problem_id_list = [i for i, _ in choice_problem_id_list]
        n = len(c_problem_id_list)  # 选择题题目数量
        self.do_homework_operation(n, c_problem_id_list, problem_type='选择')

        problem_id_list = self.parameter.get_problem_id_for_ui(eval_id, traditional_teach=True)
        m = len(problem_id_list)  # 操作题题目数量
        self.do_homework_operation(m, problem_id_list, problem_type='操作')

        self.click(ElementSelector.push_homework_btn_loc)
        self.click(ElementSelector.confirm_btn_loc)
        try:
            self.click(ElementSelector.standard_emergency_challenge_btn_loc)
        except Exception:
            print('没有出现紧急挑战按钮，请检查题目是否全部正确')
        else:
            for r in range(5):
                problem_name = self.get_text(ElementSelector.standard_enm_problem_name_loc)
                name_list = problem_name.split(' ')
                name = name_list[-1]
                code = get_code(problem_id=None, problem_name=name, challenge=True)
                code_input = self.get_element(ElementSelector.code_view_loc)
                input_code(code, code_input)
                self.click(ElementSelector.standard_challenge_run_btn_loc)
                try:
                    self.wait_for_text_visible('挑战成功', ElementSelector.standard_challenge_result_tip_loc)
                except BaseException as e:
                    print(f'{e}题目"{name}"答案错了，用挑战失败再断言一次')
                    self.wait_for_text_visible('挑战失败', ElementSelector.standard_challenge_result_tip_loc)
                self.click(ElementSelector.standard_keep_challenge_btn_loc)

        self.switch_to_default_window()
        self.refresh()
        self.wait_for_text_visible('已完成', ElementSelector.homework_status_loc)
        self.wait_for_text_visible('优秀', ElementSelector.homework_quality_loc)

    def student_do_homework_loop(self):
        """
        标准授课遍历做作业列表前3个作业

        :param enable_assert: 是否检查
        :return: None
        """

        for a in range(1, 4):  # 依次做作业列表3个作业
            homework_name_sel = f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div'
            try:
                self.wait_for_element_visible(homework_name_sel)
            except Exception as e:
                print(f'{e}作业列表为空，刷新页面')
                self.refresh()
            finally:
                self.click(homework_name_sel)
            self.click(ElementSelector.view_code_btn_loc)
            self.switch_to_window(a)

            # problem_list = self.driver.find_elements(ElementSelector.problem_list_loc, tag=False)
            eval_id_list = self.parameter.get_eval_id(traditional_teach=True)
            eval_id = eval_id_list[a - 1]  # 按顺序取出作业的eval_id
            choice_problem_id_list = self.parameter.get_choice_problem_id_for_ui(eval_id)
            c_problem_list = [i for i, _ in choice_problem_id_list]
            c = len(c_problem_list)
            self.do_homework_operation(c, c_problem_list, problem_type='选择')

            problem_id_list = self.parameter.get_problem_id_for_ui(eval_id, traditional_teach=True)
            n = len(problem_id_list)
            s = n - a
            self.do_homework_operation(s, problem_id_list, problem_type='操作')
            self.click(
                f'//span[contains(text(),"操作")]/parent::div/parent::div/following-sibling::div[{n}]')
            code_input = self.get_element(ElementSelector.code_view_loc)
            wrong_answer = 'wrong_answer = "wrong"'
            code_input.send_keys(wrong_answer)
            self.click(ElementSelector.save_run_btn_loc)
            self.wait_for_text_visible('评测不通过', ElementSelector.unpass_result_text_loc)
            self.click(ElementSelector.push_homework_btn_loc)
            self.click(ElementSelector.confirm_btn_loc)

            do_num = s + c
            try:
                if a == 1:
                    self.__assert_equal('已完成', f'//div[@class="homework-container-gird"]'
                                               f'/ul/li[{a}]/div/div/div/div[2]/div[3]')  # 作业列表的完成状态
                else:
                    complete_text = self.get_text(f'//div[@class="homework-container-gird"]'
                                                  f'/ul/li[{a}]/div/div/div/div[2]/div[2]'
                                                  f'/span[1]')
                    num = complete_text.split('/')
                    complete_num = num[0]
                    assert (complete_num == str(do_num + 1))
            except Exception as e:
                print(f'{e}作业完成状态和质量异常')
            self.click(homework_name_sel)  # 点击作业名称
            try:
                correct_rate = int((do_num / (n + c)) * 100)
                if 100 >= correct_rate >= 85:
                    exp_homework_quality = '优秀'
                elif 85 > correct_rate >= 70:
                    exp_homework_quality = '良好'
                elif 70 > correct_rate >= 60:
                    exp_homework_quality = '及格'
                else:
                    exp_homework_quality = '不及格'

                self.__assert_equal(exp_homework_quality, ElementSelector.homework_quality_loc)
                self.__assert_equal('已完成', ElementSelector.homework_status_loc)
            except Exception as e:
                print(f'{e}作业完成状态和质量异常')
            self.go_back()

    def student_do_homework_for_teach(self):
        """
        高校版做作业操作

        :param enable_assert: 是否检查
        :return: None
        """
        for a in range(1, 7):  # 依次做作业列表6个作业
            homework_name_sel = f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div'
            self.click(homework_name_sel)
            self.click(ElementSelector.view_code_btn_loc)
            self.driver.switch_to_window(a)  # 切换新弹出的table

            problem_list = self.driver.find_elements_by_xpath('//div[@class="el-row"]/div')
            n = len(problem_list)
            s = n - a
            for i in range(1, s + 1):  # 依次点击题目列表的题，做题数量递减
                self.click(f'//div[@class="el-row"]/div[{i}]')

                # DB中把code拿出来
                get_problem_id = self.get_text(ElementSelector.problem_id_loc)
                len_text = len(get_problem_id)
                problem_id = get_problem_id[:len_text - 1]
                code = get_code(problem_id=problem_id, problem_name=None)
                code_input = self.get_element(ElementSelector.uni_teach_code_view_loc)
                input_code(code, code_input)

                self.click(ElementSelector.save_run_btn_loc)
                try:
                    self.wait_for_text_visible('通过', ElementSelector.uni_teach_result_text_loc)
                except Exception as e:
                    print(f'{e}题目运行结果异常')
            problem_list[n - 1].click()
            code_input = self.get_element(ElementSelector.uni_teach_code_view_loc)
            wrong_answer = 'wrong_answer = "wrong"'
            code_input.send_keys(wrong_answer)
            self.click(ElementSelector.save_run_btn_loc)
            try:
                self.wait_for_text_visible('不通过', ElementSelector.unpass_result_text_loc)
            except Exception as e:
                print(f'{e}错误答案运行结果异常')
            self.click(ElementSelector.push_homework_btn_loc)
            self.click(ElementSelector.confirm_btn_loc)
            self.__assert_equal('已完成', f'//div[@class="homework-container-gird"]'
                                       f'/ul/li[{a}]/div/div/div/div[2]/div[3]')
            self.click(homework_name_sel)  # 点击作业名称

            correct_rate = int((s / n) * 100)
            if 100 >= correct_rate >= 85:
                exp_homework_quality = '优秀'
            elif 85 > correct_rate >= 70:
                exp_homework_quality = '良好'
            elif 70 > correct_rate >= 60:
                exp_homework_quality = '及格'
            else:
                exp_homework_quality = '不及格'

            self.__assert_equal(exp_homework_quality, ElementSelector.homework_quality_loc)
            self.__assert_equal('已完成', ElementSelector.homework_status_loc)
            self.go_back()

    def do_homework_operation(self, num, problem_id_list, problem_type=''):
        """
        标准授课作答页面做作业操作题
        :param num: 题目数量
        :param problem_type: 题目类型，选择 或 操作
        :param problem_id_list: problem id 列表
        :return:
        """
        if not problem_type:
            raise Exception('problem_type不能为空，请输入“选择”或“操作”')
        for i in range(1, num + 1):  # 依次点击题目列表的题，做题数量递减
            try:
                self.wait_for_element_visible(
                    f'//span[contains(text(),"{problem_type}")]'
                    f'/parent::div/parent::div/following-sibling::div[{i}]')
            except Exception as e:
                print('学生作业作答页面题目列表返回空列表', e)
                self.refresh()
            finally:
                if self.wait:
                    self.slow_click(f'//span[contains(text(),"{problem_type}")]'
                                    f'/parent::div/parent::div/following-sibling::div[{i}]')

            problem_id = problem_id_list[i - 1]  # 取出对应索引题目的problem_id
            if '操作' == problem_type:
                code = get_code(problem_id=problem_id, problem_name=None)  # 操作题查询代码
                code_input = self.get_element(ElementSelector.code_view_loc)
                input_code(code, code_input)

                self.slow_click(ElementSelector.save_run_btn_loc)
                try:
                    self.wait_for_text_visible('评测通过', ElementSelector.pass_result_text_loc)
                except Exception as e:
                    print(f'{e}DB答案错误导致{problem_id}题目评测异常')
            elif '选择' == problem_type:
                answer = get_choice(problem_id=problem_id, problem_name=None)  # 选择题查询答案
                self.slow_click(f'//div[contains(text(),"{answer}")]/parent::span/preceding-sibling::span')
            else:
                raise Exception('problem_type输入错误，请输入“选择”或“操作”')

    def __course_field_operation(self, code, exp_output, wrong=False):
        """
        查看课件精简试炼场操作
        :return:
        """
        self.slow_click(ElementSelector.edit_btn_loc)
        code_input_element = self.get_element(ElementSelector.edit_cursor_loc)
        input_code(code, code_input_element)
        self.click(ElementSelector.course_run_code_btn_loc)
        if wrong:
            self.wait_for_text_visible(exp_output, ElementSelector.text_output_area_loc)
        else:
            self.__assert_equal(exp_output, ElementSelector.text_output_area_loc)
            self.slow_click(ElementSelector.pic_output_btn_loc)
            try:
                self.wait_for_element_visible(ElementSelector.pic_output_area_loc)
            except BaseException as e:
                print(f'{e},精简试炼场图形输出异常')
            finally:
                self.click(ElementSelector.putback_btn_loc)

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
            self.update_text(ElementSelector.my_work_name_input_loc, new_value=work_name)
            if self.wait:
                code_input_element = self.get_element(ElementSelector.add_work_cursor_loc)
                code = turtle_code()
                input_code(code, code_input_element)
            for a in [ElementSelector.add_work_picture_btn_loc, ElementSelector.add_author_picture_btn_loc]:
                if self.wait:
                    self.click(a)
                    upload_file_by_auto_it('jpg')
        if self.wait:
            self.click(ElementSelector.sel_class_loc)
            self.click(ElementSelector.first_class_loc)
            self.slow_click(ElementSelector.sel_audit_teacher_loc)
        self.click_visible_elements(f'//span[text()="{class_name}"]')
        self.click(f'//span[text()="{Data().teacher_name_for_edu()}"]')
        self.click(ElementSelector.submit_audit_btn_loc)
        if enable_assert:
            exp_tip = '恭喜你，已提交教师进行审核！'
            self.wait_for_text_visible(exp_tip, ElementSelector.succ_tip_loc)

    def audit_work(self, work_name, enable_assert=False):
        """
        教师审核作品

        :param work_name: 审核的作品名称
        :param enable_assert: 是否检查
        :return: None
        """
        self.slow_click(ElementSelector.screening_tab_loc)
        if self.wait:
            self.slow_click(f'//div[text()="{work_name}"]')
        if '直接审核作品' == work_name:
            self.click(ElementSelector.direct_release_btn_loc)
            exp_tip = '发布成功'
        elif '详细审核通过作品' == work_name:
            self.click(ElementSelector.detailed_review_btn_loc)
            self.click(ElementSelector.pass_review_btn_loc)
            exp_tip = '审核成功！'
        else:
            self.click(ElementSelector.detailed_review_btn_loc)
            self.click(ElementSelector.reject_btn_loc)
            exp_tip = '驳回成功！'
        self.__assert_equal(exp_tip, ElementSelector.succ_tip_loc)
        self.click_button(ElementSelector.creative_space_loc)
        if enable_assert:
            try:
                self.wait_for_text_visible(work_name)
            except Exception as e:
                print(f'{e}作品被驳回，不在作品大厅中，此用例PASS')

    def wish_box(self):
        """
        首页意见反馈操作

        :return: None
        """
        if self.wait:
            self.slow_click(ElementSelector.feedback_btn_loc, timeout=6)
        self.add_text(ElementSelector.content_textarea_loc, text='意见反馈测试')
        self.click(ElementSelector.feedback_upload_pic_loc)
        upload_file_by_auto_it('jpg')
        if self.wait:
            self.click(ElementSelector.submit_btn_loc)
            self.__assert_equal('许愿信提交成功！', ElementSelector.succ_tip_loc)

    def ai_experience(self):
        """
        AI体验

        :return: None
        """
        if self.wait:
            self.slow_click(ElementSelector.image_identify_tab_loc)
            self.click(ElementSelector.upload_pic_loc)
        upload_file_by_auto_it('jpg')

        self.__pic_image_identify_operation()
        self.click(ElementSelector.car_pic_loc)
        self.__pic_image_identify_operation()

        word = '叮当码'
        for tab in range(1, 3):
            self.click(f'//div[@class="item-change-box clearfix"]/div[{tab}]')
            self.update_text(ElementSelector.word_input_loc, new_value=word)
            self.click(ElementSelector.generate_btn_loc)
            if tab == 1:
                try:
                    if self.wait:
                        self.wait_for_text_visible(word, ElementSelector.poetry_title_loc)
                except BaseException as a:
                    print(f'{a}用失败提示再次断言')
                    try:
                        self.wait_for_text_visible('我还在学习', ElementSelector.succ_tip_loc)
                    except BaseException as e:
                        print(f'{e}创作诗句异常')
            else:
                try:
                    actual_title = self.get_text(ElementSelector.couples_title_loc)
                    if all([actual_title]):
                        pass
                    else:
                        print('异常：春联标题没有文本')
                except BaseException as e:
                    print(f'{e}创作春联异常')
            self.slow_click(ElementSelector.subject_word_loc)
            actual_word = None
            if self.wait:
                actual_word = self.get_text(ElementSelector.subject_word_loc)
            if tab == 1:
                self.wait_for_text_visible(actual_word, ElementSelector.poetry_title_loc)
            else:
                try:
                    couple_text = self.get_text(ElementSelector.couples_text_loc)
                    c_list = couple_text.split('\n')
                    if any(c_list):
                        for a in actual_word:
                            assert (a in c_list)
                    else:
                        print('异常：没有春联文本')
                except BaseException as e:
                    print(f'{e}创作春联异常')

    def __pic_image_identify_operation(self):
        face_output = '年龄：'
        car_license_output = '车牌号为：'
        pic_tag_output = '这个是'
        fail_output = '上传图片无法识别'
        btn_text_list = ['人脸', '车牌', '图片标签']
        for t in btn_text_list:
            if self.wait:
                self.slow_click(f'//span[contains(text(),"{t}")]', timeout=1)
                try:
                    if '人脸' == t:
                        if self.wait:
                            self.wait_for_text_visible(face_output, selector=ElementSelector.output_text_loc)
                    elif '车牌' == t:
                        if self.wait:
                            self.wait_for_text_visible(car_license_output, selector=ElementSelector.output_text_loc)
                    else:
                        if self.wait:
                            self.wait_for_text_visible(pic_tag_output, selector=ElementSelector.output_text_loc)
                except Exception as a:
                    print(f'{a}用失败提示再次断言')
                    try:
                        self.wait_for_text_visible(fail_output, selector=ElementSelector.output_text_loc)
                    except Exception as e:
                        print(f'{e}图片识别异常')

    def __input_code(self, code, code_input):
        self.add_text(code_input, text=(Keys.CONTROL, 'a'))
        self.add_text(code_input, text=Keys.BACKSPACE)
        for c in code.split("\n"):
            self.add_text(code_input, text=c)
            if c != "":
                self.add_text(code_input, text=Keys.ESCAPE)
                self.add_text(code_input, text=Keys.ENTER)
                self.add_text(code_input, text=Keys.HOME)
                self.add_text(code_input, text=(Keys.SHIFT, Keys.TAB))
            else:
                self.add_text(code_input, text=Keys.ENTER)

    @staticmethod
    def __input_time(now=False, front=False, start=False):
        """
        提供公用的输入时间，格式为YYYY-MM-DD hh:mm:ss
        :param now: 返回当前时间
        :param front: 返回10分钟前
        :param start: 返回30分钟后
        :return:
        """
        time_diff = datetime.timedelta(minutes=10)
        now_time = datetime.datetime.now()
        if now:
            a_time = now_time
        elif front:
            a_time = now_time - time_diff
        elif start:
            a_time = now_time + time_diff * 3
        else:
            a_time = now_time + time_diff * 4
        b_time = int(a_time.timestamp())
        time_local = time.localtime(b_time)
        i_time = time.strftime('%Y-%m-%d %H:%M:%S', time_local)

        return i_time

    def __wait_for_loading(self):
        """
        等待遮罩层消失
        :return:
        """
        self.wait_for_element_absent('//div[@class="el-loading-mask is-fullscreen"]')
        time.sleep(1.5)
        return self.assert_element_absent('//div[@class="el-loading-mask is-fullscreen"]')

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
        self.wait_for_element_visible(text_loc)
        actual_text = self.get_text(text_loc)
        print(f'期望： "{text}", 实际： "{actual_text}"')
        try:
            self.assert_equal(text, actual_text)
        except Exception as e:
            print(f'{text}断言异常，与期望不符,', e)
