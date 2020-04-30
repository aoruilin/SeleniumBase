import os
import time
from interface.base.HTMLTestRunner import HTMLTestRunner
from unittest.suite import TestSuite
from interface.uni_lab.testcase.login import TestLogin
from interface.uni_lab.testcase.getClassList import TestGetClassList
from interface.uni_lab.testcase.addCourse import TestAddCourse
from interface.uni_lab.testcase.addHomework_loop import AddHomework_loop

project_path = os.path.dirname(os.getcwd())
print(project_path)
report_path = project_path + '\\reports' + time.strftime('%Y%m%d%H%M%S') + '.html'
fp = open(report_path, 'wb')
suite = TestSuite()
test_01 = TestLogin('test_01')
test_02 = TestGetClassList('test_01')
test_03 = TestAddCourse('test_01')
test_04 = AddHomework_loop('test_addHomework')

suite.addTests([test_01, test_02, test_03, test_04])
runner = HTMLTestRunner(stream=fp, title='叮当码教育版2期接口自动化测试报告', description='登录发布课程、作业')
runner.run(suite)

