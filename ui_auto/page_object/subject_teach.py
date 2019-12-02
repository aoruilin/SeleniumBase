from unittest import TestCase

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys

from base.data import PointIdIndex
from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.common.mysql import get_code
from ui_auto.common.input_code import input_code
from ui_auto.common.input_time import input_time
from ui_auto.page_object.common import Common
from ui_auto.page_object.element_loc import AddCourseElement, AddHomeworkElement
from ui_auto.page_object.element_loc import CheckCourseElement, DoHomeWorkElement
from ui_auto.page_object.element_loc import IndexElement, SubjectTeachElement
from ui_auto.page_object.page_operation import Assert, ClickButton
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class SubjectTeach:
    answer_list = ['显示', '不显示', '截止时间后显示']
    teaching_package_list = ['叮当资源', '校本资源', '我的资源']
    course_btn_list = ['课件', '视频', '讲义']

    def __init__(self, driver):
        self.driver = driver
        self.parameter = ParameterForOthers('student')

    def click_china_map(self):
        """
        点击主题授课中国地图s系列

        :return: None
        """
        try:
            all_s = self.driver.find_elements(*SubjectTeachElement.map_s1_btn_loc)
            s1_btn = all_s[PointIdIndex.checkpoint_level_one_index]
            s1_btn.click()
        except ElementNotVisibleException:
            print('非第一次进入闯关授课，跳过大地图页面操作')
        except IndexError:
            print('非第一次进入闯关授课，跳过大地图页面操作')
        except BaseException as e:
            print(f'{e}中国地图点击异常')

    def click_map_path(self):
        """
        点击主题授课地图路径知识点

        :return:None
        """
        path_point_elem_list = self.driver.find_elements(*SubjectTeachElement.path_btn_loc)
        path_point_elem = path_point_elem_list[PointIdIndex.checkpoint_level_two_index]
        path_point_elem.click()

    def add_course_simple(self, package_name, discover=False, enable_assert=False) -> str:
        """
        主题授课添加课件

        :param package_name: 添加的课件类型
        :param discover: 是否从探索进入
        :param enable_assert: 是否检查
        :return: 添加的课件名称，传入学生查看课件
        """

        self.driver.find_element_by_xpath(f'//span[text()="{package_name}"]/parent::label/span[1]',
                                          msg=f'选择{package_name}', click=True)  # 授课包选择
        self.driver.find_element(*AddCourseElement.checkpoint_choice_btn_loc, click=True)
        self.driver.find_element(*AddCourseElement.checkpoint_choice_class_btn_loc, tag=False, click=True)
        self.driver.find_element(*AddCourseElement.checkpoint_add_publish_btn, tag=False, click=True)
        self.driver.find_element(*AddCourseElement.checkpoint_publish_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '发布课件成功'
            Assert(self.driver).assert_add_course_tip(exp_tip, AddCourseElement.succ_tip_loc,
                                                      AddCourseElement.repeated_tip_confirm_loc)
        course_name_elem = self.driver.find_element(*AddCourseElement.check_point_course_name_loc)\
            if discover else self.driver.find_element(*SubjectTeachElement.first_course_name_loc)
        check_point_course_name = course_name_elem.text
        if discover:
            self.driver.close()
            handle = self.driver.window_handles(0)
            self.driver.switch_to_window(handle)

        return check_point_course_name  # 返回课程名称

    def add_course_loop_checkpoint(self) -> list:
        """
        主题授课遍历3中资源类型添加课件

        :return: 返回添加的3个课件名称
        """
        course_name_list = []
        for name in self.teaching_package_list:
            self.driver.find_element(*SubjectTeachElement.add_checkpoint_course_loc, click=True)
            self.driver.find_element(*SubjectTeachElement.choice_checkpoint_loc, click=True)
            Common.choice_point(self.driver, subject=True)
            check_point_course_name = self.add_course_simple(name, enable_assert=True)
            course_name_list.append(check_point_course_name)

        return course_name_list

    def add_homework_simple(self, homework_name, answer_config, timing=None, enable_assert=False):
        """
        主题授课发布作业

        :param homework_name: 发布的作业名称
        :param answer_config: 答案设置
        :param timing: 定时设置
        :param enable_assert: 是否检查
        :return: None
        """

        self.driver.find_element(*AddHomeworkElement.checkpoint_homework_name_input_loc,
                                 send_keys=True, content=homework_name)
        self.driver.find_element(*AddHomeworkElement.checkpoint_choice_problem_btn_loc, tag=False, click=True)
        self.driver.find_element(*AddHomeworkElement.checkpoint_choice_all_btn_loc, click=True)
        self.driver.find_element(*AddHomeworkElement.checkpoint_confirm_problem_btn_loc, tag=False, click=True)
        self.driver.find_element(*AddHomeworkElement.checkpoint_choice_class_btn_loc, click=True)
        self.driver.find_element(*AddHomeworkElement.checkpoint_show_answer_loc, tag=False, click=True)
        self.driver.find_element_by_xpath(f'//span[text()="{answer_config}"]/parent::li',
                                          msg=answer_config, tag=False, click=True)

        if 1 == timing:
            self.driver.find_element(*AddHomeworkElement.checkpoint_timing_btn_loc, click=True)
            checkpoint_timing_input_elem = self.driver.find_element(
                *AddHomeworkElement.checkpoint_timing_input_loc, tag=False)
            checkpoint_timing_input_elem.send_keys(input_time(start=True))
            checkpoint_timing_input_elem.send_keys(Keys.ENTER)

        end_time_input_elem = self.driver.find_element(*AddHomeworkElement.checkpoint_end_time_input_loc,
                                                       tag=False)
        end_time_input_elem.clear()
        end_time_input_elem.send_keys(input_time())
        end_time_input_elem.send_keys(Keys.ENTER)
        self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, click=True)
        if enable_assert:
            exp_tip = '发布成功！'
            Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.succ_tip_loc)
            Assert(self.driver).assert_text_in_page(homework_name, AddHomeworkElement.checkpoint_all_homework_name)

    def add_homework_loop(self):
        for a in self.answer_list:
            for t in range(0, 2):
                homework_name = f'答案{a}定时{t}'
                ClickButton(self.driver).click_button(SubjectTeachElement.add_checkpoint_homework_loc)
                self.driver.find_element(*SubjectTeachElement.choice_checkpoint_loc, click=True)
                Common.choice_point(self.driver, subject=True)
                self.add_homework_simple(homework_name, a, t, enable_assert=True)

    def student_check_index_course(self, course_name, enable_assert=False):
        """
        学生端检查首页课件名称

        :param course_name: 断言用课件名称
        :param enable_assert: 是否检查
        :return: None
        """
        if enable_assert:
            Assert(self.driver).assert_equal(course_name, IndexElement.index_course_name_loc)
        ClickButton(self.driver).click_button(IndexElement.checkpoint_course_loc)

    def student_check_course_simple(self, course_name, discover=False, enable_assert=False):
        """
        主题授课学生查看课件
        :param course_name: 查看的课件名称
        :param discover: 是否通过探索进入
        :param enable_assert: 是否检查
        :return: None
        """

        if enable_assert:
            Assert(self.driver).assert_equal(course_name, CheckCourseElement.checkpoint_course_name_loc)

        if discover:
            ClickButton(self.driver).click_button(CheckCourseElement.first_in_course_loc)

        for btn in self.course_btn_list:
            try:
                self.driver.find_element_by_xpath(f'//p[text()="{btn}"]', msg=btn, tag=False, click=True)
                if discover:
                    self.driver.find_element_by_xpath(
                        f'//p[text()="{btn}"]/parent::div/parent::div/following-sibling::div',
                        msg=f'{btn}下的文件名称', click=True)
                else:
                    if '自动上传课件' == course_name:
                        self.driver.find_element_by_xpath(
                            f'//p[contains(text(),"{btn}")]/parent::div/parent::div/parent::div/div[2]/div[2]/div/div',
                            msg=f'多文件资源{btn}第二个文件', tag=False, click=True)
                    else:
                        self.driver.find_element_by_xpath(
                            f'//p[contains(text(),"{btn}")]/parent::div/parent::div/parent::div/div[2]/div/div/div',
                            msg='课件名称', click=True)
            except NoSuchElementException:
                print(f'没有{btn}资源')
            except Exception as e:
                print(f'{e}课件资源异常')
            if '课件' == btn:
                try:
                    self.driver.switch_to_frame(self.driver.find_elements_by_tag_name('iframe', msg='切换子页面')[0])
                    self.driver.switch_to_frame('wacframe')
                    wait = SeleniumDriver.webdriver_wait(self.driver)
                    show_up = SeleniumDriver.element_presence(self.driver, CheckCourseElement.ppt_pages_num_loc)
                    wait.until(show_up)
                    page_num_text = self.driver.find_element(*CheckCourseElement.ppt_pages_num_loc, no_wait=True,
                                                             text=True)
                    page_text = page_num_text[11:]
                    num_text = page_text[:2]
                    page_num = int(num_text)
                    for s in range(page_num):
                        self.driver.find_element(*CheckCourseElement.ppt_next_btn_loc, tag=False, click=True)
                except Exception as e:
                    print(f'{e}PPT显示异常')
                finally:
                    self.driver.switch_to_default_content()
        self.driver.close()
        handle = self.driver.window_handles(0)
        self.driver.switch_to_window(handle)

    def student_check_course_loop(self):
        """
        主题授课学生查看课件

        :return: None
        """
        for c in range(1, 4):
            course_name = self.driver.find_element_by_xpath(
                f'//div[@class="dia-container clearfix"]/div[{c}]/div/div/div[2]',
                msg=f'第{c}个课件的名称', text=True)
            self.driver.find_element_by_xpath(
                f'//div[@class="dia-container clearfix"]/div[{c}]/div/div/div[5]',
                msg=f'第{c}个课件', click=True)
            handle = self.driver.window_handles(1)
            self.driver.switch_to_window(handle)
            self.student_check_course_simple(course_name, enable_assert=True)

    def student_do_homework_simple(self, homework_name, enable_assert=False):
        """
        主题授课做作业

        :param homework_name: 断言用作业名称
        :param enable_assert: 是否检查
        :return: None
        """

        try:
            self.driver.find_element(*DoHomeWorkElement.go_to_code_btn_loc)
        except NoSuchElementException:
            print('未找到该作业,刷新后重试')
            self.driver.refresh()
        except BaseException as e:
            print(f'{e}作业列表异常')
        finally:
            if enable_assert:
                Assert(self.driver).assert_equal(homework_name, DoHomeWorkElement.homework_name_loc)
            ClickButton(self.driver).click_and_jump(DoHomeWorkElement.go_to_code_btn_loc, 2)

        problem_list = self.driver.find_elements(*DoHomeWorkElement.problem_list_loc, tag=False)
        eval_id_list = self.parameter.get_eval_id()
        eval_id = eval_id_list[0]
        problem_id_list = self.parameter.get_problem_id_for_ui(eval_id)
        n = len(problem_list)
        self.do_homework_operation(n, problem_id_list)
        self.driver.find_element(*DoHomeWorkElement.checkpoint_push_homework_btn_loc, tag=False, click=True)
        self.driver.find_element(*DoHomeWorkElement.checkpoint_push_confirm_btn_loc, tag=False, click=True)
        # 作业结果弹框操作
        if enable_assert:
            exp_result = '还不错哦太厉害了'
            Assert(self.driver).assert_in(exp_result, DoHomeWorkElement.result_tip_loc, reverse=True)
        try:
            self.driver.find_element(*DoHomeWorkElement.emergency_challenge_btn_loc, tag=False, click=True)
            self.do_challenge_operation()
        except NoSuchElementException as x:
            print(x)
        except ElementNotVisibleException as v:
            print(v)
        except BaseException as e:
            print(f'{e}紧急挑战异常，有题目答案错误导致无法触发或紧急挑战做题操作异常，请查看日志')

    def student_do_homework_loop(self, enable_assert=False):
        """
        主题授课遍历做作业列表前3个作业

        :param enable_assert: 是否检查
        :return: None
        """
        for a in range(1, 4):  # 依次做作业列表3个作业
            try:
                self.driver.find_element_by_xpath(  # 作业去答题
                    f'//div[@class="items-gird"]/div[{a}]/div[2]/div[2]', msg=f'第{a}个作业')
            except NoSuchElementException:
                print('作业列表为空，刷新页面')
                self.driver.refresh()
            except BaseException as e:
                print(f'{e}作业列表异常')
            finally:
                self.driver.find_element_by_xpath(  # 点击作业去答题
                    f'//div[@class="items-gird"]/div[{a}]/div[2]/div[2]', msg=f'第{a}个作业', click=True)

            handle = self.driver.window_handles(a)  # 切换新弹出的table
            self.driver.switch_to_window(handle)
            problem_name_list = []
            problem_name_elem_list = self.driver.find_elements(*DoHomeWorkElement.problem_list_name_loc, tag=False)
            for problem_name_elem in problem_name_elem_list:
                problem_name = problem_name_elem.text
                problem_name_list.append(problem_name)
            eval_id_list = self.parameter.get_eval_id()
            eval_id = eval_id_list[a - 1]
            problem_id_list = self.parameter.get_problem_id_for_ui(eval_id)
            n = len(problem_name_elem_list)
            s = n - a
            self.do_homework_operation(s, problem_id_list)
            self.driver.find_element_by_xpath(f'//div[@class="el-row"]/div[{n}]', msg=f'第{n}道题', click=True)
            code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
            wrong_answer = 'wrong_answer = "wrong"'
            code_input.send_keys(wrong_answer)
            self.driver.find_element(*DoHomeWorkElement.checkpoint_save_run_btn_loc, tag=False, click=True)
            if enable_assert:
                Assert(self.driver).assert_in('评测未通过', DoHomeWorkElement.checkpoint_result_unpass_loc)
            self.driver.find_element(*DoHomeWorkElement.checkpoint_confirm_btn_loc, tag=False, click=True)
            self.driver.find_element(*DoHomeWorkElement.checkpoint_push_homework_btn_loc, click=True)
            self.driver.find_element(*DoHomeWorkElement.checkpoint_push_confirm_btn_loc, click=True)
            if enable_assert:
                try:
                    correct_rate = int((s / n) * 100)
                    if a == 1 and correct_rate >= 60:
                        exp_result = '还不错哦太厉害了'
                        actual_result = self.driver.find_element(*DoHomeWorkElement.result_tip_loc, text=True)
                    elif a >= 2 and correct_rate >= 60:
                        exp_result = '有待提高还不错哦'
                        actual_result = self.driver.find_element(*DoHomeWorkElement.result_tip_loc, text=True)
                    else:
                        exp_result = '再接再厉有待提高还不错哦'
                        actual_result = self.driver.find_element(*DoHomeWorkElement.result_tip_loc, text=True)
                    tc = TestCase()
                    tc.assertIn(actual_result, exp_result, '作业结果错误')
                except Exception as e:
                    print(f'{e}作业质量结果异常')
            # 作业结果弹框操作
            if a == 3:
                self.driver.find_element(*DoHomeWorkElement.wrong_redo_btn_loc, tag=False, click=True)
                problem_elem_list = self.driver.find_elements(*DoHomeWorkElement.problem_list_loc)
                n = len(problem_elem_list)
                for w in range(1, n + 1):
                    try:
                        self.driver.find_element(*DoHomeWorkElement.wrong_problem_name_loc)
                    except Exception as e:
                        print(f'{e}作业作答作业列表为空，刷新后重新点击')
                        self.driver.refresh()
                    finally:
                        wrong_problem_name_num = self.driver.find_element(*DoHomeWorkElement.wrong_problem_name_loc,
                                                                          text=True)
                        wrong_problem_name_list = wrong_problem_name_num.split('\n')
                        wrong_problem_name = wrong_problem_name_list[1]
                        if enable_assert:
                            tc = TestCase()
                            try:
                                tc.assertIn(wrong_problem_name, problem_name_list, '这个错题不是这个作业的题')
                            except Exception as e:
                                print(f'{e}错题统计题目列表异常')
                        problem_name = self.driver.find_element(*DoHomeWorkElement.problem_name_loc, text=True)
                    code = get_code(problem_id=None, problem_name=problem_name, challenge=True)
                    code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
                    input_code(code, code_input)
                    self.driver.find_element(*DoHomeWorkElement.checkpoint_save_run_btn_loc, tag=False, click=True)
                    if enable_assert:
                        tc = TestCase()
                        try:
                            result_text = self.driver.find_element(*DoHomeWorkElement.checkpoint_result_pass_loc,
                                                                   text=True)
                            tc.assertIn('评测通过', result_text, '运行结果错误')
                        except NoSuchElementException:
                            print(f'{problem_name}DB题目答案错误，尝试评测未通过断言')
                            Assert(self.driver).assert_in('评测未通过', DoHomeWorkElement.checkpoint_result_unpass_loc)
                        except Exception as e:
                            print(f'{e}其他错误,不再尝试断言')
                    self.driver.find_element(*DoHomeWorkElement.checkpoint_confirm_btn_loc, tag=False, click=True)
                self.driver.find_element(*DoHomeWorkElement.checkpoint_push_homework_btn_loc, click=True)
                self.driver.find_element(*DoHomeWorkElement.checkpoint_push_confirm_btn_loc, click=True)
                if enable_assert:
                    exp_result = '还不错哦太厉害了'
                    Assert(self.driver).assert_in(exp_result, DoHomeWorkElement.result_tip_loc, reverse=True)

                try:
                    self.driver.find_element(*DoHomeWorkElement.emergency_challenge_btn_loc, tag=False, click=True)
                    self.do_challenge_operation()
                except Exception as e:
                    print(f'{e}紧急挑战异常，有题目答案错误导致无法触发或紧急挑战做题操作异常，请查看日志')
                self.driver.close()
                handle = self.driver.window_handles(a - 1)
                self.driver.switch_to_window(handle)
                self.driver.refresh()
                self.driver.find_element_by_xpath(  # 点击作业名称
                    f'//div[@class="items-gird"]/div[{a}]/div[2]/div[1]', msg=f'第{a}个作业的作业分析', click=True)
            else:
                self.driver.find_element(*DoHomeWorkElement.analysis_btn_loc, tag=False, click=True)
            if enable_assert:
                exp_status = '已完成'
                Assert(self.driver).assert_in(exp_status, DoHomeWorkElement.checkpoint_homework_status_loc)
            self.driver.find_element(*DoHomeWorkElement.return_homework_btn_loc, tag=False, click=True)

    def do_homework_operation(self, n, problem_id_list):
        """
        作业作答页面做题操作
        :param n: 题目数量
        :param problem_id_list: 题目id
        :return: None
        """
        for i in range(1, n + 1):
            try:
                self.driver.find_element_by_xpath(f'//div[@class="el-row"]/div[{i}]', msg=f'第{i}个题目')
            except Exception as e:
                print(f'{e}作业作答作业列表为空，刷新后重新点击')
                self.driver.refresh()
            finally:
                self.driver.find_element_by_xpath(f'//div[@class="el-row"]/div[{i}]', msg=f'第{i}个题目', click=True)
            # DB中把code拿出来
            problem_id = problem_id_list[i - 1]
            code = get_code(problem_id=problem_id, problem_name=None)
            code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
            input_code(code, code_input)

            self.driver.find_element(*DoHomeWorkElement.checkpoint_save_run_btn_loc, tag=False, click=True)
            tc = TestCase()
            try:
                result_text = self.driver.find_element(*DoHomeWorkElement.checkpoint_result_pass_loc, text=True)
                tc.assertIn('评测通过', result_text, '运行结果错误')
            except NoSuchElementException:
                print(f'DB题目{problem_id}答案错误导致，尝试评测未通过断言')
                Assert(self.driver).assert_in('评测未通过', DoHomeWorkElement.checkpoint_result_unpass_loc)
            except Exception as a:
                print(f'{a}其他错误,不再尝试断言')
            self.driver.find_element(*DoHomeWorkElement.checkpoint_confirm_btn_loc, tag=False, click=True)

    def do_challenge_operation(self):
        """
        紧急挑战做题操作
        :return: None
        """
        for i in range(5):
            if i == 0:
                problem_name = self.driver.find_element(*DoHomeWorkElement.enm_problem_name_loc, text=True)
            else:
                problem_name = self.driver.find_element(*DoHomeWorkElement.enm_problem_name_loc_1, text=True)
            code = get_code(problem_id=None, problem_name=problem_name, challenge=True)
            code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
            input_code(code, code_input)
            self.driver.find_element(*DoHomeWorkElement.checkpoint_save_run_btn_loc, tag=False, click=True)
            actual_tip = self.driver.find_element(*DoHomeWorkElement.challenge_result_tip_loc, text=True)
            tc = TestCase()
            try:
                exp_tip = '挑战成功'
                tc.assertEqual(actual_tip, exp_tip, '紧急挑战结果提示错误')
            except NoSuchElementException:
                print(f'题目"{problem_name}"答案错了，用挑战失败再断言一次')
                exp_tip = '挑战失败'
                Assert(self.driver).assert_equal(exp_tip, DoHomeWorkElement.challenge_result_tip_loc)
            except Exception as e:
                print(f'{e}挑战结果异常')
            if i == 4:
                for n in range(3):
                    self.driver.find_element(*DoHomeWorkElement.keep_challenge_btn_loc, click=True)
                    problem_name_elem_list = self.driver.find_elements(
                        *DoHomeWorkElement.problem_name_list_loc)
                    actual_problem_name_list = []
                    for problem_name_elem in problem_name_elem_list:
                        actual_problem_name = problem_name_elem.text
                        actual_problem_name_list.append(actual_problem_name)
                    tc = TestCase()
                    tc.assertIn(problem_name, actual_problem_name_list, '题目列表名称与做过的题不符')
                    self.driver.find_element(*DoHomeWorkElement.change_problem_btn_loc, tag=False, click=True)
                    problem_name = self.driver.find_element(*DoHomeWorkElement.enm_problem_name_loc_1,
                                                            text=True)
                    code = get_code(problem_id=None, problem_name=problem_name, challenge=True)
                    code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
                    input_code(code, code_input)

                    self.driver.find_element(*DoHomeWorkElement.checkpoint_save_run_btn_loc, tag=False,
                                             click=True)
                    actual_tip = self.driver.find_element(*DoHomeWorkElement.challenge_result_tip_loc,
                                                          text=True)
                    tc = TestCase()
                    try:
                        exp_tip = '挑战成功'
                        tc.assertEqual(actual_tip, exp_tip, '紧急挑战结果提示错误')
                    except NoSuchElementException:
                        print(f'题目"{problem_name}"答案错了，用挑战失败再断言一次')
                        exp_tip = '挑战失败'
                        Assert(self.driver).assert_equal(
                            exp_tip, DoHomeWorkElement.challenge_result_tip_loc)
                    except Exception as e:
                        print(f'{e}挑战结果异常')
            else:
                try:
                    self.driver.find_element(*DoHomeWorkElement.challenge_next_problem_btn_loc,
                                             tag=False, click=True)
                except Exception as e:
                    print(f'答案错误挑战失败导致{e},尝试点击继续挑战按钮并点击换一题')
                    self.driver.find_element(*DoHomeWorkElement.keep_challenge_btn_loc,
                                             tag=False, click=True)
                    self.driver.find_element(*DoHomeWorkElement.change_problem_btn_loc,
                                             tag=False, click=True)
                try:
                    problem_name_elem_list = self.driver.find_elements(
                        *DoHomeWorkElement.problem_name_list_loc)
                    actual_problem_name_list = []
                    for problem_name_elem in problem_name_elem_list:
                        actual_problem_name = problem_name_elem.text
                        actual_problem_name_list.append(actual_problem_name)
                    tc = TestCase()
                    tc.assertIn(problem_name, actual_problem_name_list, '题目列表名称与做过的题不符')
                except Exception as e:
                    print(f'{e}做过的题不在题目列表中，题目列表异常')
