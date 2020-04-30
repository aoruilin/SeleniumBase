import time

from common.get_cwd import get_absolute_path
from interface.base.HTMLTestRunner import HTMLTestRunner
from unittest.suite import TestSuite
from interface.K12edu.testcase.user_controller import TestUser
from interface.K12edu.testcase.addCourse import TestAddCourse
from interface.K12edu.testcase.addHomework import AddHomework
from interface.K12edu.testcase.addHomework_loop import AddHomeworkLoop
from interface.K12edu.testcase.student_homework_controller import DoHomework
from interface.K12edu.testcase.submit_work import SubmitWork

project_cwd = get_absolute_path('testcase')
report_path = project_cwd.joinpath(f'testsuits\\reports\\{time.strftime("%Y%m%d%H%M%S")}.html').as_posix()
fp = open(report_path, 'wb')
suite = TestSuite()
test_01 = TestUser('test_login_01')
test_02 = TestGetClassList('test_01')
test_03 = TestAddCourse('test_01')
test_04 = AddHomework('test_01')
test_05 = DoHomework('test_do_homework_01')
test_06 = AddHomework('test_02')
test_07 = DoHomework('test_do_homework_02')
test_08 = AddHomeworkLoop('test_01')
test_09 = AddHomeworkLoop('test_02')
test_10 = SubmitWork('test_01')
test_11 = SubmitWork('test_02')
test_12 = SubmitWork('test_03')

suite.addTests([test_01, test_02, test_03, test_04, test_05, test_06, test_07, test_08, test_09, test_10,
                test_11, test_12])
runner = HTMLTestRunner(stream=fp, title='叮当码教育版2期接口自动化测试报告', description='登录发布课程、作业')
runner.run(suite)
