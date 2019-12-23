import datetime
import smtplib
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

from ui_auto.base.data import EmailData
from ui_auto.common.get_cwd import get_absolute_path
from ui_auto.common.file_operation import zip_dir
from ui_auto.base.HTMLTestRunner import HTMLTestRunner
from unittest.suite import TestSuite
from ui_auto.testcase.edu_main_process import TestMainProcess
from ui_auto.testcase.packages_course import TestPackageCourse
from ui_auto.testcase.homework_loop import HomeworkLoop
from ui_auto.testcase.edu_do_homework_loop import DoHomework
from ui_auto.testcase.test_field_operation import TestFieldCase
from ui_auto.testcase.add_draft import TestAddDraft
from ui_auto.testcase.my_creation_work import TestMyCreation
from ui_auto.testcase.test_field_work import WorksHall
from ui_auto.testcase.user_login_wrong import UserLoginWrong
from ui_auto.testcase.add_resources import AddResourcesCase
from ui_auto.testcase.ai_experience import TestAIExperience
from ui_auto.testcase.wish_box import TestWishBox
from ui_auto.testcase.error_check import TestErrorCheck

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour='23', minute='0', second='0')
def do_test():
    print(f'当前时间：{datetime.datetime.now()}')
    project_cwd = get_absolute_path('testcase')
    report_path = project_cwd.joinpath(f'testsuits\\reports\\{time.strftime("%Y%m%d%H%M%S")}.html')
    fp = open(report_path, 'wb')
    suite = TestSuite()
    test01 = TestMainProcess('test_MainProcess_01')
    test02 = TestMainProcess('test_MainProcess_02')
    test03 = AddResourcesCase('test_add_resources')
    test04 = TestPackageCourse('test_package_course_01')
    test05 = TestPackageCourse('test_package_course_02')
    test06 = HomeworkLoop('test_add_homework_loop_01')
    test07 = DoHomework('test_do_homework_loop_01')
    test08 = HomeworkLoop('test_homework_loop_01')
    test09 = DoHomework('test_homework_loop_02')
    test10 = TestAddDraft('test_save_draft_loop')
    test11 = TestFieldCase('test_01')
    test12 = TestFieldCase('test_02')
    test13 = TestFieldCase('test_03')
    test14 = TestFieldCase('test_04')
    test15 = TestFieldCase('test_05')
    test16 = TestFieldCase('test_06')
    test17 = TestMyCreation('test_01')
    test18 = WorksHall('test_01')
    test19 = WorksHall('test_02')
    test20 = WorksHall('test_03')
    test21 = TestAIExperience('test_01')
    test22 = TestWishBox('test_wish_box')
    test23 = UserLoginWrong('test_wrong_login')
    test24 = TestErrorCheck('test_field_error')
    test25 = TestErrorCheck('test_course_field_error')

    suite.addTests([
        test01, test02, test03, test04, test05, test06, test07, test08, test09, test10, test11, test12, test13,
        test14, test15, test16, test17, test18, test19, test20, test21, test22, test23, test24, test25
    ])
    runner = HTMLTestRunner(stream=fp, title='叮当码教育版2期ui自动化测试报告',
                            description='测试模块：标准授课，主题授课，试炼场，创作空间，AI体验')
    runner.run(suite)

    mail_server = EmailData.mail_server
    port = EmailData.port
    sender_email = EmailData.sender_email
    sender_password = EmailData.sender_password
    receive_email = EmailData.receive_email
    try:
        msg = MIMEMultipart('related')
        msg['From'] = formataddr(['sender', sender_email])
        msg['To'] = formataddr(['receiver', receive_email])
        msg['Subject'] = '自动测试报告'

        body = """
        <h1>UI自动化测试报告，详情见附件。</h1>
        """
        text = MIMEText(body, 'html', 'utf-8')
        msg.attach(text)

        file_path = f'{project_cwd.as_posix()}\\testsuits\\reports'
        zip_path = f'{get_absolute_path("ui_auto")}\\testcase\\testsuits\\reports.zip'
        zip_dir(file_path, zip_path)
        with open(zip_path, 'rb') as f:
            attach = MIMEBase('application', 'octet-stream')
            attach.set_payload(f.read())
            attach.add_header('Content-Disposition', 'attachment', filename='Report.zip')
            encoders.encode_base64(attach)
            f.close()
        msg.attach(attach)

        server = smtplib.SMTP(mail_server, port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receive_email, msg.as_string())
        server.quit()
        print('邮件已发送')
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(wait=False)
