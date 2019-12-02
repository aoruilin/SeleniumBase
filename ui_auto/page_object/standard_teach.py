from unittest import TestCase

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys

from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.common.mysql import get_code, get_choice
from ui_auto.common.input_code import input_code
from ui_auto.common.input_time import input_time
from ui_auto.page_object.common import Common
from ui_auto.page_object.element_loc import AddCourseElement, AddHomeworkElement
from ui_auto.page_object.element_loc import CheckCourseElement, DoHomeWorkElement
from ui_auto.page_object.element_loc import StandardTeachElement, IndexElement
from ui_auto.page_object.page_operation import Assert, ClickButton
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.picture_list_code import turtle_code


# from interface.K12edu.common.eval_id_for_others import get_eval_id
# from interface.K12edu.common.student_homework.problem_id_for_ui_test import get_problem_id_for_ui


class StandardTeach:
    teaching_package_list = ['叮当资源', '校本资源', '我的资源']
    answer_list = ['立即公布', '不公布', '截止时间公布']

    def __init__(self, driver):
        self.driver = driver
        self.parameter = ParameterForOthers('student')

    def add_course_simple(self, package_name, enable_assert=False):
        """
        标准授课添加课件

        :param package_name: 添加的课件类型
        :param enable_assert: 是否检查
        :return: None
        """
        self.driver.find_element(*StandardTeachElement.add_course_loc, click=True)
        self.driver.find_element_by_xpath(f'//span[text()="{package_name}"]/parent::label/span[1]',
                                          msg=f'选择{package_name}', click=True)  # 授课包选择
        # self.driver.find_element(*AddCourseElement.choice_teaching_package_loc, click=True)  # 授课包选择
        if '叮当资源' == package_name:
            self.driver.find_element(*AddCourseElement.selKnow_loc, tag=False, click=True)
            Common.choice_point(self.driver)
            self.driver.find_element(*AddCourseElement.choice_btn_loc, click=True)
        else:
            self.driver.find_element(*AddCourseElement.choice_btn_loc, click=True)
        self.driver.find_element(*AddCourseElement.choice_class_btn_loc, tag=False, click=True)
        self.driver.find_element(*AddCourseElement.add_publish_btn, click=True)
        self.driver.find_element(*AddCourseElement.publish_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '成功添加课件！'
            Assert(self.driver).assert_add_course_tip(exp_tip, AddCourseElement.succ_tip_loc,
                                                      AddCourseElement.repeated_tip_confirm_loc)
        self.driver.find_element(*AddCourseElement.back_btn_loc, click=True)
        course_name_elem = self.driver.find_element(*AddCourseElement.course_name_loc, tag=False)
        course_name = course_name_elem.text

        return course_name  # 返回课程名称

    def add_course_loop(self):
        """
        标准授课遍历3中资源类型添加课程

        :return: 返回添加的3个课件名称
        """
        course_name_list = []

        for name in self.teaching_package_list:
            course_name = self.add_course_simple(name, enable_assert=True)
            course_name_list.append(course_name)
        return course_name_list  # 返回课件名称列表，包含3个课件名称

    def add_course_wrong(self, enable_assert=False):
        """
        标准授课添加课件错误操作

        :param enable_assert: 是否检查
        :return: None
        """

        # 不选择知识点
        self.driver.find_element(*StandardTeachElement.add_course_loc, click=True)
        self.driver.find_element(*AddCourseElement.choice_class_btn_loc, click=True)
        self.driver.find_element(*AddCourseElement.add_publish_btn, click=True)
        self.driver.find_element(*AddCourseElement.publish_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '请选择您要发布的课件包！'
            Assert(self.driver).assert_equal(exp_tip, AddCourseElement.fail_tip_loc)

        # 不选择班级
        self.driver.refresh()
        self.driver.find_element(*AddCourseElement.selKnow_loc, click=True)
        Common.choice_point(self.driver)
        self.driver.find_element(*AddCourseElement.choice_btn_loc, click=True)
        self.driver.find_element(*AddCourseElement.add_publish_btn, click=True)
        self.driver.find_element(*AddCourseElement.publish_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '请选择您要发往的班级！'
            Assert(self.driver).assert_equal(exp_tip, AddCourseElement.fail_tip_loc)

    def add_homework_simple(self, homework_name, answer_config, timing=None, enable_assert=False):
        """
        标准授课发布作业

        :param answer_config: 答案设置
        :param timing: 定时设置
        :param homework_name: 发布作业的名称
        :param enable_assert: 是否检查
        :return: None
        """
        self.driver.find_element(*AddHomeworkElement.homework_name_input_loc, send_keys=True, content=homework_name)
        self.driver.find_element(*AddHomeworkElement.choice_pointId_btn_loc, tag=False, click=True)
        self.driver.find_element(*AddHomeworkElement.sel_know_loc, click=True)
        Common.choice_point(self.driver)
        try:
            Common.choice_problem_for_homework(self.driver)
        except Exception as e:
            self.driver.find_element(*AddHomeworkElement.sel_know_loc, click=True)
            Common.choice_problem_for_homework(self.driver)
        self.driver.find_element(*AddHomeworkElement.choice_class_btn_loc, click=True)
        self.driver.find_element(*AddHomeworkElement.show_answer_loc, tag=False, click=True)
        self.driver.find_element_by_xpath(f'//span[text()="{answer_config}"]/parent::li',
                                          msg=answer_config, tag=False, click=True)
        if 1 == timing:
            self.driver.find_element(*AddHomeworkElement.timing_btn_loc, tag=False, click=True)
            self.driver.find_element(*AddHomeworkElement.timing_input_loc,
                                     send_keys=True, content=input_time(start=True))
            self.driver.find_element(*AddHomeworkElement.timing_input_loc,
                                     send_keys=True, content=Keys.ENTER)
        else:
            pass
        end_time_input_elem = self.driver.find_element(*AddHomeworkElement.end_time_input_loc)
        end_time_input_elem.clear()
        end_time_input_elem.send_keys(input_time())
        end_time_input_elem.send_keys(Keys.ENTER)
        self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, tag=False, click=True)
        if enable_assert:
            exp_tip = '成功添加作业！'
            Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.succ_tip_loc)

    def add_homework_loop(self):
        """
        遍历所有发布设置发布作业

        :return: None
        """
        for a in self.answer_list:
            for t in range(2):
                homework_name = f'答案{a}定时{t}'
                ClickButton(self.driver).click_button(StandardTeachElement.add_homework_btn_loc)
                self.add_homework_simple(homework_name, a, timing=t, enable_assert=True)

    def add_homework_wrong(self, enable_assert=False):
        """
        标准授课发布作业错误操作

        :param enable_assert: 是否检查
        :return: None
        """
        for i in ['名称', '知识点', '班级']:
            homework_name = f'{i}不输入'
            ClickButton(self.driver).click_button(StandardTeachElement.add_homework_btn_loc)
            if '名称' == i:
                self.driver.find_element(*AddHomeworkElement.choice_pointId_btn_loc, click=True)
                self.driver.find_element(*AddHomeworkElement.sel_know_loc, click=True)
                Common.choice_point(self.driver)
                Common.choice_problem_for_homework(self.driver)
                self.driver.find_element(*AddHomeworkElement.choice_class_btn_loc, click=True)
                self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, tag=False, click=True)
                if enable_assert:
                    exp_tip = '请输入作业名称！'
                    Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.fail_tip_loc)
            elif '知识点' == i:
                self.driver.find_element(*AddHomeworkElement.homework_name_input_loc, send_keys=True,
                                         content=homework_name)
                self.driver.find_element(*AddHomeworkElement.choice_class_btn_loc, tag=False, click=True)
                self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, tag=False, click=True)
                if enable_assert:
                    exp_tip = '请通过知识点选出作业题目！'
                    Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.fail_tip_loc)
            else:
                self.driver.find_element(*AddHomeworkElement.homework_name_input_loc, send_keys=True,
                                         content=homework_name)
                self.driver.find_element(*AddHomeworkElement.choice_pointId_btn_loc, tag=False, click=True)
                self.driver.find_element(*AddHomeworkElement.sel_know_loc, click=True)
                Common.choice_point(self.driver)
                Common.choice_problem_for_homework(self.driver)
                self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, tag=False, click=True)
                if enable_assert:
                    exp_tip = '请选择您要发往的班级！'
                    Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.fail_tip_loc)
            self.driver.back()

        time_list = ['定时', '截止']
        for t in time_list:
            for n in range(0, 2):
                homework_name = f'输入错误{t}时间'
                ClickButton(self.driver).click_button(StandardTeachElement.add_homework_btn_loc)
                self.driver.find_element(*AddHomeworkElement.homework_name_input_loc, send_keys=True,
                                         content=homework_name)
                self.driver.find_element(*AddHomeworkElement.choice_pointId_btn_loc, tag=False, click=True)
                self.driver.find_element(*AddHomeworkElement.sel_know_loc, click=True)
                Common.choice_point(self.driver)
                Common.choice_problem_for_homework(self.driver)
                self.driver.find_element(*AddHomeworkElement.choice_class_btn_loc, click=True)
                end_time_input_elem = self.driver.find_element(*AddHomeworkElement.end_time_input_loc, tag=False)
                if '定时' == t:
                    self.driver.find_element(*AddHomeworkElement.timing_btn_loc, tag=False, click=True)
                    if 1 == n:
                        self.driver.find_element(*AddHomeworkElement.timing_input_loc, tag=False,
                                                 send_keys=True, content=input_time(now=True))
                    else:
                        self.driver.find_element(*AddHomeworkElement.timing_input_loc, tag=False,
                                                 send_keys=True, content=input_time(front=True))
                    self.driver.find_element(*AddHomeworkElement.timing_input_loc, tag=False,
                                             send_keys=True, content=Keys.ENTER)
                    end_time_input_elem.clear()
                    end_time_input_elem.send_keys(input_time())
                    end_time_input_elem.send_keys(Keys.ENTER)
                    self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, click=True)
                    if enable_assert:
                        exp_tip = '定时时间要大于当前时间！'
                        Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.fail_tip_loc)
                else:
                    end_time_input_elem.clear()
                    if 1 == n:
                        end_time_input_elem.send_keys(input_time(now=True))
                    else:
                        end_time_input_elem.send_keys(input_time(front=True))
                    end_time_input_elem.send_keys(Keys.ENTER)
                    self.driver.find_element(*AddHomeworkElement.public_homework_btn_loc, click=True)
                    if enable_assert:
                        exp_tip = '截止时间要大于当前时间和定时时间！'
                        Assert(self.driver).assert_equal(exp_tip, AddHomeworkElement.fail_tip_loc)
                self.driver.back()

    def student_check_index_course(self, course_name, enable_assert=False):
        if enable_assert:
            Assert(self.driver).assert_equal(course_name, IndexElement.index_course_name_loc)
        ClickButton(self.driver).click_button(IndexElement.standard_course_btn_loc)

    def student_check_course_simple(self, course_name, enable_assert=False):
        """
        标准授课学生查看课件
        :param course_name: 查看的课件名称
        :param enable_assert: 是否检查
        :return: None
        """

        if enable_assert:
            Assert(self.driver).assert_equal(course_name, CheckCourseElement.courseCard_tit_loc)
            exp_number = ' 1'
            Assert(self.driver).assert_equal(exp_number, CheckCourseElement.lookNumber_loc)

        self.course_field_operation(turtle_code(), 'abc')

        btn_list = ['课件', '视频', '讲义']
        for btn in btn_list:
            try:
                self.driver.find_element_by_xpath(f'//p[text()="{btn}"]', tag=False, msg=btn, click=True)
                if '自动上传课件' == course_name:
                    self.driver.find_element_by_xpath(
                        f'//p[text()="{btn}"]/parent::div/parent::div/parent::div/div[2]/div[2]',
                        tag=False, msg=btn, click=True)
                else:
                    self.driver.find_element_by_xpath(
                        f'//p[text()="{btn}"]/parent::div/parent::div/parent::div/div[2]',
                        tag=False, msg=btn, click=True)
            except Exception as e:
                print(f'{e}缺少资源')
            if '课件' == btn:
                self.driver.switch_to_frame(self.driver.find_elements_by_tag_name('iframe', msg='切换子页面')[0])
                self.driver.switch_to_frame('wacframe')
                try:
                    wait = SeleniumDriver.webdriver_wait(self.driver)
                    show_up = SeleniumDriver.element_presence(self.driver, CheckCourseElement.ppt_pages_num_loc)
                    wait.until(show_up)
                    page_num_text = self.driver.find_element(*CheckCourseElement.ppt_pages_num_loc,
                                                             no_wait=True, text=True)
                    page_text = page_num_text[11:]
                    num_text = page_text[:2]
                    page_num = int(num_text)
                    for s in range(page_num):
                        self.driver.find_element(*CheckCourseElement.ppt_next_btn_loc, tag=False, click=True)
                except Exception as e:
                    print(f'{e}PPT显示异常')
                finally:
                    self.driver.switch_to_default_content()

    def student_check_course_loop(self):
        """
        学生端遍历查看列表前3个课件

        :return: None
        """
        for c in range(1, 4):
            course_name_elem = self.driver.find_element_by_xpath(
                f'//div[@class="course-container-gird"]/ul/li[{c}]/div/div/div[2]/div[1]/div', msg=f'第{c}个课件')
            course_name = course_name_elem.text
            course_name_elem.click()  # 点击课程名称进入课程详情页面
            self.student_check_course_simple(course_name, enable_assert=True)
            self.driver.find_element(*CheckCourseElement.crumbs_loc, click=True)

    def uni_teach_student_check_course(self, course_name, enable_assert=False):
        """
        高校版学生查看课件
        :param course_name:查看的课件名称
        :param enable_assert: 是否检查
        :return: None
        """

        if enable_assert:
            Assert(self.driver).assert_equal(course_name, IndexElement.index_course_name_loc)
        self.driver.find_element(*IndexElement.uni_teach_start_course_btn_loc, tag=False, click=True)
        self.driver.find_element(*StandardTeachElement.first_course_loc, click=True)  # 点击课程名称进入课程详情页面

        if enable_assert:
            Assert(self.driver).assert_equal(course_name, CheckCourseElement.courseCard_tit_loc)
            exp_number = ' 1'
            Assert(self.driver).assert_equal(exp_number, CheckCourseElement.lookNumber_loc)

        btn_list = ['课件', '视频', '讲义']
        for btn in btn_list:
            self.driver.find_element_by_xpath(f'//p[text()="{btn}"]', msg=btn, tag=False, click=True)
            self.driver.find_element_by_xpath(f'//p[text()="{btn}"]'
                                              f'/parent::div/parent::div/parent::div/div[2]/div/div/div',
                                              msg=btn, tag=False, click=True)
            if '课件' == btn:
                self.driver.switch_to_frame(self.driver.find_elements_by_tag_name('iframe', msg='切换子页面')[0])
                self.driver.switch_to_frame('wacframe')
                try:
                    wait = SeleniumDriver.webdriver_wait(self.driver)
                    show_up = SeleniumDriver.element_presence(self.driver, CheckCourseElement.ppt_pages_num_loc)
                    wait.until(show_up)
                    page_num_text = self.driver.find_element(*CheckCourseElement.ppt_pages_num_loc,
                                                             no_wait=True, text=True)
                    page_text = page_num_text[11:]
                    num_text = page_text[:2]
                    page_num = int(num_text)
                    for s in range(page_num):
                        self.driver.find_element(*CheckCourseElement.ppt_next_btn_loc, tag=False, click=True)
                except Exception as e:
                    print(f'{e}PPT显示异常')
                finally:
                    self.driver.switch_to_default_content()

    def student_do_homework_simple(self, homework_name, enable_assert=False):
        """
        标准授课做作业

        :param homework_name: 断言用作业名称
        :param enable_assert: 是否检查
        :return: None
        """
        try:
            self.driver.find_element(*DoHomeWorkElement.homework_to_do_loc)
        except Exception as e:
            print(f'{e}学生端作业列表返回空列表')
            self.driver.refresh()
        finally:
            if enable_assert:
                Assert(self.driver).assert_equal(homework_name, DoHomeWorkElement.homework_to_do_loc)
            self.driver.find_element(*DoHomeWorkElement.homework_to_do_loc, tag=False, click=True)
        self.driver.find_element(*DoHomeWorkElement.view_code_btn_loc, click=True)
        handle = self.driver.window_handles(1)
        self.driver.switch_to_window(handle)

        eval_id_list = self.parameter.get_eval_id(traditional_teach=True)
        eval_id = eval_id_list[0]

        choice_problem_id_list = self.parameter.get_choice_problem_id_for_ui(eval_id)
        c_problem_id_list = [i for i, _ in choice_problem_id_list]
        n = len(c_problem_id_list)
        self.do_homework_operation(n, c_problem_id_list, problem_type='选择')

        problem_id_list = self.parameter.get_problem_id_for_ui(eval_id, traditional_teach=True)
        m = len(problem_id_list)  # 操作题题目数量
        self.do_homework_operation(m, problem_id_list, problem_type='操作')

        self.driver.find_element(*DoHomeWorkElement.push_homework_btn_loc, click=True)
        self.driver.find_element(*DoHomeWorkElement.confirm_btn_loc, tag=False, click=True)
        self.driver.find_element(*DoHomeWorkElement.standard_emergency_challenge_btn_loc, click=True)
        for r in range(5):
            problem_name = self.driver.find_element(*DoHomeWorkElement.standard_enm_problem_name_loc, text=True)
            name_list = problem_name.split(' ')
            name = name_list[-1]
            code = get_code(problem_id=None, problem_name=name, challenge=True)
            code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
            input_code(code, code_input)
            self.driver.find_element(*DoHomeWorkElement.save_run_btn_loc, tag=False, click=True)
            if enable_assert:
                actual_tip = self.driver.find_element(*DoHomeWorkElement.standard_challenge_result_tip_loc, text=True)
                tc = TestCase()
                try:
                    exp_tip = '挑战成功'
                    tc.assertIn(exp_tip, actual_tip, '紧急挑战结果提示错误')
                except BaseException as e:
                    print(f'{e}题目"{name}"答案错了，用挑战失败再断言一次')
                    exp_tip = '挑战失败'
                    Assert(self.driver).assert_in(exp_tip, DoHomeWorkElement.standard_challenge_result_tip_loc)
            self.driver.find_element(*DoHomeWorkElement.standard_keep_challenge_btn_loc, tag=False, click=True)

        self.driver.close()
        handle = self.driver.window_handles(0)
        self.driver.switch_to_window(handle)
        self.driver.refresh()
        if enable_assert:
            exp_status = '已完成'
            exp_quality = '优秀'
            Assert(self.driver).assert_equal(exp_quality, DoHomeWorkElement.homework_quality_loc)
            Assert(self.driver).assert_equal(exp_status, DoHomeWorkElement.homework_status_loc)

    def student_do_homework_loop(self, enable_assert=False):
        """
        标准授课遍历做作业列表前3个作业

        :param enable_assert: 是否检查
        :return: None
        """

        for a in range(1, 4):  # 依次做作业列表3个作业
            try:
                self.driver.find_element_by_xpath(  # 点击作业名称
                    f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div',
                    msg=f'第{a}个作业')
            except Exception as e:
                self.driver.refresh()
                print(f'{e}作业列表为空，刷新页面')
            finally:
                homework_name_elem = self.driver.find_element_by_xpath(  # 点击作业名称
                    f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div',
                    msg=f'点击第{a}个作业')
                homework_name_elem.click()
            self.driver.find_element(*DoHomeWorkElement.view_code_btn_loc, click=True)
            handle = self.driver.window_handles(a)
            self.driver.switch_to_window(handle)

            # problem_list = self.driver.find_elements(*DoHomeWorkElement.problem_list_loc, tag=False)
            eval_id_list = self.parameter.get_eval_id(traditional_teach=True)
            eval_id = eval_id_list[a - 1]
            choice_problem_id_list = self.parameter.get_choice_problem_id_for_ui(eval_id)
            c_problem_list = [i for i, _ in choice_problem_id_list]
            c = len(c_problem_list)
            self.do_homework_operation(c, c_problem_list, problem_type='选择')

            problem_id_list = self.parameter.get_problem_id_for_ui(eval_id, traditional_teach=True)
            n = len(problem_id_list)
            s = n - a
            self.do_homework_operation(s, problem_id_list, problem_type='操作')
            self.driver.find_element_by_xpath(
                f'//span[contains(text(),"操作")]/parent::div/parent::div/following-sibling::div[{n}]',
                msg=f'操作题第{n}个题目', tag=False, click=True)
            code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc, tag=False)
            wrong_answer = 'wrong_answer = "wrong"'
            code_input.send_keys(wrong_answer)
            self.driver.find_element(*DoHomeWorkElement.save_run_btn_loc, click=True)
            if enable_assert:
                Assert(self.driver).assert_in('测评不通过', DoHomeWorkElement.unpass_result_text_loc)
            self.driver.find_element(*DoHomeWorkElement.push_homework_btn_loc, click=True)
            self.driver.find_element(*DoHomeWorkElement.confirm_btn_loc, click=True)

            do_num = s + c
            if enable_assert:
                tc = TestCase()
                try:
                    if a == 1:
                        homework_list_status = self.driver.find_element_by_xpath(  # 作业列表的完成状态
                            f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[2]/div[3]',
                            msg=f'第{a}个作业的完成状态', text=True)

                        tc.assertEqual(homework_list_status, '已完成', '作业列表状态错误')
                    else:
                        complete_text = self.driver.find_element_by_xpath(f'//div[@class="homework-container-gird"]'
                                                                          f'/ul/li[{a}]/div/div/div/div[2]/div[2]'
                                                                          f'/span[1]', msg=f'第{a}个作业的完成题目数量',
                                                                          text=True)
                        num = complete_text.split('/')
                        complete_num = num[0]
                        tc.assertEqual(complete_num, str(do_num + 1), '作业完成题目数错误')
                except Exception as e:
                    print(f'{e}作业完成状态和质量异常')
                self.driver.find_element_by_xpath(  # 点击作业名称
                    f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div',
                    msg=f'第{a}个作业', tag=False, click=True)
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

                    Assert(self.driver).assert_equal(exp_homework_quality, DoHomeWorkElement.homework_quality_loc)
                    Assert(self.driver).assert_equal('已完成', DoHomeWorkElement.homework_status_loc)
                except Exception as e:
                    print(f'{e}作业完成状态和质量异常')
                self.driver.back()

    def student_do_homework_for_teach(self, enable_assert=False):
        """
        高校版做作业操作

        :param enable_assert: 是否检查
        :return: None
        """
        for a in range(1, 7):  # 依次做作业列表6个作业
            homework_name_elem = self.driver.find_element_by_xpath(  # 点击作业名称
                f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div',
                msg=f'第{a}个作业')
            homework_name_elem.click()
            self.driver.find_element(*DoHomeWorkElement.view_code_btn_loc, click=True)
            handle = self.driver.window_handles(a)  # 切换新弹出的table
            self.driver.switch_to_window(handle)

            problem_list = self.driver.find_elements_by_xpath('//div[@class="el-row"]/div',
                                                              msg='题目列表', tag=False)
            n = len(problem_list)
            s = n - a
            for i in range(1, s + 1):  # 依次点击题目列表的题，做题数量递减
                self.driver.find_element_by_xpath(f'//div[@class="el-row"]/div[{i}]',
                                                  msg=f'第{i}道题', click=True)

                # DB中把code拿出来
                get_problem_id = self.driver.find_element(*DoHomeWorkElement.problem_id_loc, text=True)
                len_text = len(get_problem_id)
                problem_id = get_problem_id[:len_text - 1]
                code = get_code(problem_id=problem_id, problem_name=None)
                code_input = self.driver.find_element(*DoHomeWorkElement.uni_teach_code_view_loc)
                input_code(code, code_input)

                self.driver.find_element(*DoHomeWorkElement.save_run_btn_loc, tag=False, click=True)
                if enable_assert:
                    tc = TestCase()
                    try:
                        pass_result_text = self.driver.find_element(*DoHomeWorkElement.uni_teach_result_text_loc,
                                                                    text=True)
                        tc.assertIn(pass_result_text, '通过', '运行结果错误')
                    except Exception as e:
                        print(f'{e}题目运行结果异常')
            problem_list[n - 1].click()
            code_input = self.driver.find_element(*DoHomeWorkElement.uni_teach_code_view_loc, tag=False)
            wrong_answer = 'wrong_answer = "wrong"'
            code_input.send_keys(wrong_answer)
            self.driver.find_element(*DoHomeWorkElement.save_run_btn_loc, tag=False, click=True)
            if enable_assert:
                tc = TestCase()
                try:
                    unpass_result_text = self.driver.find_element(*DoHomeWorkElement.unpass_result_text_loc,
                                                                  text=True)
                    tc.assertIn(unpass_result_text, '不通过', '运行结果错误')
                except Exception as e:
                    print(f'{e}错误答案运行结果异常')
            self.driver.find_element(*DoHomeWorkElement.push_homework_btn_loc, click=True)
            self.driver.find_element(*DoHomeWorkElement.confirm_btn_loc, tag=False, click=True)
            if enable_assert:
                homework_list_status = self.driver.find_element_by_xpath(  # 作业列表的完成状态
                    f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[2]/div[3]',
                    msg=f'第{a}个作业的完成状态', text=True)
                tc = TestCase()
                tc.assertEqual(homework_list_status, '已完成', '作业列表状态错误')
                self.driver.find_element_by_xpath(  # 点击作业名称
                    f'//div[@class="homework-container-gird"]/ul/li[{a}]/div/div/div/div[1]/div[1]/div',
                    msg=f'第{a}个作业', tag=False, click=True)
                actual_homework_quality = self.driver.find_element(*DoHomeWorkElement.homework_quality_loc,
                                                                   text=True)
                homework_status = self.driver.find_element(*DoHomeWorkElement.homework_status_loc,
                                                           tag=False, text=True)

                correct_rate = int((s / n) * 100)
                if 100 >= correct_rate >= 85:
                    exp_homework_quality = '优秀'
                elif 85 > correct_rate >= 70:
                    exp_homework_quality = '良好'
                elif 70 > correct_rate >= 60:
                    exp_homework_quality = '及格'
                else:
                    exp_homework_quality = '不及格'

                tc.assertEqual(actual_homework_quality, exp_homework_quality, '作业质量错误')
                tc.assertEqual(homework_status, '已完成', '作业状态错误')
                self.driver.back()

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
                self.driver.find_element_by_xpath(
                    f'//span[contains(text(),"{problem_type}")]/parent::div/parent::div/following-sibling::div[{i}]',
                    msg=f'操作题第{i}个题目')
            except Exception as e:
                print('学生作业作答页面题目列表返回空列表', e)
                self.driver.refresh()
            finally:
                self.driver.find_element_by_xpath(
                    f'//span[contains(text(),"{problem_type}")]/parent::div/parent::div/following-sibling::div[{i}]',
                    msg=f'操作题第{i}个题目', tag=False, click=True)

            problem_id = problem_id_list[i - 1]
            if '操作' == problem_type:
                code = get_code(problem_id=problem_id, problem_name=None)
                code_input = self.driver.find_element(*DoHomeWorkElement.code_view_loc)
                input_code(code, code_input)

                self.driver.find_element(*DoHomeWorkElement.save_run_btn_loc, click=True)
                tc = TestCase()
                try:
                    pass_result_text = self.driver.find_element(*DoHomeWorkElement.pass_result_text_loc, text=True)
                    tc.assertIn('测评通过', pass_result_text, '运行结果错误')
                except Exception as e:
                    print(f'{e}DB答案错误导致{problem_id}题目评测异常')
            elif '选择' == problem_type:
                answer = get_choice(problem_id=problem_id, problem_name=None)
                self.driver.find_element_by_xpath(
                    f'//div[contains(text(),"{answer}")]/parent::span/preceding-sibling::span',
                    msg=f'点击选项{answer}', click=True)
            else:
                raise Exception('problem_type输入错误，请输入“选择”或“操作”')

    def course_field_operation(self, code, exp_output, wrong=False):
        """
        查看课件精简试炼场操作
        :return:
        """
        self.driver.find_element(*CheckCourseElement.edit_btn_loc, click=True)
        code_input_element = self.driver.find_element(*CheckCourseElement.edit_cursor_loc)
        input_code(code, code_input_element)
        self.driver.find_element(*CheckCourseElement.run_code_btn_loc, tag=False, click=True)
        if wrong:
            Assert(self.driver).assert_in(exp_output, CheckCourseElement.text_output_area_loc)
        else:
            Assert(self.driver).assert_equal(exp_output, CheckCourseElement.text_output_area_loc)
            self.driver.find_element(*CheckCourseElement.pic_output_btn_loc, tag=False, click=True)
            try:
                self.driver.find_element(*CheckCourseElement.pic_output_area_loc)
            except BaseException as e:
                print(f'{e},精简试炼场图形输出异常')
            finally:
                self.driver.find_element(*CheckCourseElement.putback_btn_loc, tag=False, click=True)
