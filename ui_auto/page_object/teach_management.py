from random import choice

from ui_auto.base.selenium_driver import SeleniumDriver
from ui_auto.common.upload_file import upload_file_by_auto_it
from ui_auto.page_object.element_loc import IndexElement, TeachManagementElement
from ui_auto.page_object.page_operation import Assert


class TeachManagement:
    exp_tip = '添加成功'

    def __init__(self, driver):
        self.driver = driver

    def add_account_class(self, username_teacher, teacher_name, username_student, student_name, admin_class_name,
                          pro_class_name, enable_assert=False):
        """
        管理员创建账号班级

        :param username_teacher: 创建的教师账号
        :param teacher_name: 创建的教师名称
        :param username_student: 创建的学生账号
        :param student_name: 创建的学生名称
        :param admin_class_name: 创建的行政班名称
        :param pro_class_name: 创建的课程班名称
        :param enable_assert: 是否检查
        :return: None
        """

        # 创建教师账号
        self.driver.find_element(*TeachManagementElement.teacher_manage_tab_loc, click=True)
        self.driver.find_element(*TeachManagementElement.add_teacher_btn_loc, click=True)
        add_teacher_input_list = self.driver.find_elements(*TeachManagementElement.add_input_loc)  # 创建教师表单输入框
        teacher_acc_elem = add_teacher_input_list[0]
        teacher_acc_elem.send_keys(username_teacher)
        teacher_name_elem = add_teacher_input_list[1]
        teacher_name_elem.send_keys(teacher_name)
        teacher_gender_input_list = self.driver.find_elements(*TeachManagementElement.gender_input_loc,
                                                              tag=False)
        teacher_gender_elem = choice(teacher_gender_input_list)  # 随机选择1个性别
        teacher_gender_elem.click()
        teacher_position_elem = add_teacher_input_list[2]
        teacher_position_elem.send_keys('tester')
        self.driver.find_element(*TeachManagementElement.confirm_btn_loc,
                                 tag=False, click=True)
        if enable_assert:
            Assert(self.driver).assert_equal(self.exp_tip, TeachManagementElement.success_tip_loc)
        self.driver.find_element(*TeachManagementElement.return_management_btn_loc,
                                 tag=False, click=True)

        # 创建行政班
        self.driver.find_element(*TeachManagementElement.class_manage_tab_loc, click=True)
        self.driver.find_element(*TeachManagementElement.add_class_btn_loc, click=True)
        add_admin_class_input_list = self.driver.find_elements(*TeachManagementElement.add_input_loc)  # 创建行政班表单输入框
        admin_class_name_elem = add_admin_class_input_list[0]
        admin_class_name_elem.send_keys(admin_class_name)
        manage_teacher_elem = add_admin_class_input_list[1]
        manage_teacher_elem.click()
        self.driver.find_element(*TeachManagementElement.sel_teacher_loc,
                                 tag=False, click=True)  # 管理老师下拉框选择第1个老师
        self.driver.find_element(*TeachManagementElement.confirm_btn_loc,
                                 tag=False, click=True)
        if enable_assert:
            Assert(self.driver).assert_equal(self.exp_tip, TeachManagementElement.success_tip_loc)
        self.driver.find_element(*TeachManagementElement.return_management_btn_loc,
                                 tag=False, click=True)

        # 行政班创建学生账号
        self.driver.find_element(*TeachManagementElement.admin_class_list_first_loc, click=True)
        self.driver.find_element(*TeachManagementElement.add_student_btn_loc, click=True)
        add_student_input_list = self.driver.find_elements(*TeachManagementElement.add_input_loc)  # 添加学生表单输入框
        student_id_input_elem = add_student_input_list[0]
        student_id_input_elem.send_keys(username_student)
        student_name_input_elem = add_student_input_list[2]
        student_name_input_elem.send_keys(student_name)
        student_gender_input_list = self.driver.find_elements(*TeachManagementElement.gender_input_loc,
                                                              tag=False)
        student_gender_elem = choice(student_gender_input_list)  # 随机选择1个性别
        student_gender_elem.click()
        self.driver.find_element(*TeachManagementElement.confirm_btn_loc, tag=False, click=True)
        if enable_assert:
            Assert(self.driver).assert_equal(self.exp_tip, TeachManagementElement.success_tip_loc)
        self.driver.find_element(*TeachManagementElement.return_management_btn_loc,
                                 tag=False, click=True)

        # 创建课程班
        self.driver.find_element(*TeachManagementElement.course_manage_tab_loc, click=True)
        self.driver.find_element(*TeachManagementElement.add_pro_class_btn_loc, click=True)
        add_pro_class_input_list = self.driver.find_elements(*TeachManagementElement.add_input_loc)
        pro_class_name_input_elem = add_pro_class_input_list[0]
        pro_class_name_input_elem.send_keys(pro_class_name)
        index_list = [1, 2, 3, 4]
        index = choice(index_list)  # 随机选择1个班级配图
        class_img_elem = self.driver.find_element_by_xpath(f'//div[@class="item-card-center"]/ul/li[{index}]',
                                                           msg=f'第{index}张图片')
        class_img_elem.click()
        pro_class_manage_teacher_elem = add_pro_class_input_list[2]
        pro_class_manage_teacher_elem.click()
        self.driver.find_element(*TeachManagementElement.sel_teacher_loc,
                                 tag=False, click=True)  # 选择课程班管理教师
        self.driver.find_element(*TeachManagementElement.confirm_btn_loc,
                                 tag=False, click=True)
        if enable_assert:
            Assert(self.driver).assert_equal(self.exp_tip, TeachManagementElement.success_tip_loc)
        self.driver.find_element(*TeachManagementElement.return_management_btn_loc,
                                 tag=False, click=True)

        # 课程班添加学生
        self.driver.find_element(*TeachManagementElement.pro_class_list_first_loc, click=True)
        self.driver.find_element(*TeachManagementElement.add_student_btn_loc, click=True)
        self.driver.find_element(*TeachManagementElement.sel_admin_class_loc, click=True)
        self.driver.find_element(*TeachManagementElement.sel_all_student_loc, click=True)
        self.driver.find_element(*TeachManagementElement.confirm_sel_btn_loc, tag=False, click=True)
        if enable_assert:
            Assert(self.driver).assert_equal('成功添加！', TeachManagementElement.add_success_tip_loc)

    def add_resources(self, enable_assert=False):
        """
        教师添加资源

        :param enable_assert: 是否检查
        :return: None
        """

        resource_name = '自动上传课件'
        options_list = ['校内公开', '仅自己']
        for visibility in options_list:
            self.driver.find_element(*TeachManagementElement.want_publish_btn_loc, click=True)
            self.driver.find_element(*TeachManagementElement.resource_name_input_loc,
                                     send_keys=True, content=resource_name)
            resource_img_list = self.driver.find_elements(*TeachManagementElement.resource_img_loc, tag=False)
            resource_img_elem = choice(resource_img_list)
            resource_img_elem.click()
            self.driver.find_element(*TeachManagementElement.course_describe_loc,
                                     tag=False, send_keys=True, content=resource_name)

            format_list = ['ppt', 'video', 'word', 'doc']
            for f in format_list:
                upload_btns = self.driver.find_elements(*TeachManagementElement.upload_file_btns_loc,
                                                        tag=False, loading=True)
                upload_btn = upload_btns[0]
                upload_btn.click()
                upload_file_by_auto_it(f)

            i = 0
            for f in format_list:
                continue_upload_btns = self.driver.find_elements(*TeachManagementElement.continue_to_upload_loc,
                                                                 tag=False, loading=True)
                continue_upload_btn = continue_upload_btns[i]
                continue_upload_btn.click()
                upload_file_by_auto_it(f)
                i += 1

            '''
            #win32gui文件上传
            upload_btns = self.driver.find_elements(*TeachManagementElement.upload_file_btns_loc, 
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
            '''
            '''
            #上帝之眼文件上传
            path = os.path.dirname(os.getcwd())
            j_path = get_default_jvm_path()
            jvm_path = r'C:\Program Files (x86)\Java\jdk1.8.0_151\jre\bin\client\jvm.dll'
            #jvm_path = r"C:\Program Files\Java\jdk1.8.0_191\jre\bin\server\jvm.dll"
            jar_path = '-Djava.class.path=' + path + r'\base\libs\sikulixapi.jar'
            print(j_path, jar_path)
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
            '''

            self.driver.find_element(*TeachManagementElement.visibility_sel_loc, loading=True, click=True)

            self.driver.find_element_by_xpath(f'//span[text()="{visibility}"]', msg=visibility, tag=False, click=True)
            self.driver.find_element(*TeachManagementElement.publish_btn_loc, click=True)
            if enable_assert:
                Assert(self.driver).assert_equal(self.exp_tip, TeachManagementElement.succ_tip_loc)
                self.driver.find_element(*TeachManagementElement.back_button_loc, tag=False, click=True)
