import unittest

from ui_auto.base.data import Data
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_object.page_operation import BaseTestCase


class TestCases(BaseTestCase):
    url = Data().ip_for_edu()
    username_manager = Data().manager_username_for_edu()
    username_teacher = Data().teacher_username_for_edu()
    username_student = Data().student_username_for_edu()
    password = Data().password_for_edu
    manager_name = Data().edu_manager_name()
    teacher_name = Data().teacher_name_for_edu()
    student_name = Data().student_name_for_edu()
    homework_name = Data().homework_name
    admin_class_name = Data().admin_class_name_for_edu()
    pro_class_name = Data().pro_class_name_for_edu()
    work_name = Data().direct_release_work_name
    direct_release_work_name = Data().direct_release_work_name
    detailed_review_work_name = Data().detailed_review_work_name
    reject_work_name = Data().reject_work_name

    def test_MainProcess_01(self):
        # self.teacher_login.user_login(self.username_manager, self.manager_name, self.password, teacher_assert=True)
        # self.teacher_click.click_button(ElementSelector.teach_management_btn_loc)
        # self.teacher_manage.add_account_class(self.username_teacher, self.teacher_name,
        #                                       self.username_student, self.student_name,
        #                                       self.admin_class_name, self.pro_class_name,
        #                                       enable_assert=True)
        # self.teacher_login.user_logout()
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        course_name = self.add_course_simple(self.teaching_package_list[0])
        self.click_button(ElementSelector.homework_btn_loc)
        self.click_button(ElementSelector.add_homework_btn_loc, loading=True)
        self.add_homework_simple(self.homework_name, self.answer_list[0])

        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.student_check_index_course(course_name)
        self.click_button(ElementSelector.first_course_loc)
        self.student_check_course_simple(course_name)
        self.click_button(ElementSelector.crumbs_loc)
        self.click_button(ElementSelector.homework_btn_loc, loading=True)
        self.student_do_homework_simple(self.homework_name)

    def test_MainProcess_02(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.start_discover_btn_loc)
        self.click_china_map()
        self.click_map_path()
        self.click_and_jump(ElementSelector.watch_course_btn_loc,
                            1, loading=True, wait=True)
        self.click_button(ElementSelector.kj_add_checkpoint_course_loc)
        checkpoint_course_name = self.subject_add_course_simple(self.teaching_package_list[0],
                                                                discover=True)
        self.click_and_jump(ElementSelector.watch_homework_btn_loc, 1)
        self.click_button(ElementSelector.add_checkpoint_homework_loc, loading=True)
        self.subject_add_homework_simple(self.homework_name, self.subject_answer_list[0])
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.start_discover_btn_loc)
        self.click_china_map()
        self.click_map_path()
        self.click_and_jump(ElementSelector.watch_course_btn_loc,
                            1, loading=True, wait=True)
        self.subject_student_check_course_simple(checkpoint_course_name,
                                                 discover=True)
        self.click_and_jump(ElementSelector.watch_homework_btn_loc, 1)
        self.subject_student_do_homework_simple(self.homework_name)
        
    def test_add_resources(self):
        self.login(self.username_teacher, self.teacher_name, self.password,
                   teacher_assert=True)
        self.click_button(ElementSelector.teach_management_btn_loc)
        self.click_button(ElementSelector.resource_manage_tab_loc)
        self.click_button(ElementSelector.resource_type_sel_loc,
                          loading=False, wait=True)
        self.click_button(ElementSelector.school_resource_btn_loc)
        self.add_resources()
        
    def test_package_course_01(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.add_course_loop()
        self.add_course_wrong()
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.date_selection('课件', '自动上传课件')
        self.search_input('自动上传课件')
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.student_check_course_loop()
        self.date_selection('课件', '自动上传课件', student=True)
        self.search_input('自动上传课件')

    def test_package_course_02(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_course_btn_loc, loading=True)
        self.subject_add_course_loop()
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_course_btn_loc, loading=True)
        self.subject_student_check_course_loop()
        
    def test_homework_loop_01(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.click_button(ElementSelector.homework_btn_loc)
        self.add_homework_loop()
        self.add_homework_wrong()
        self.date_selection('作业', Data().homework_name)
        self.search_input(Data().homework_name)
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.click_button(ElementSelector.homework_btn_loc)
        self.student_do_homework_loop()
        self.date_selection('作业', Data().homework_name, student=True)
        self.search_input(Data().homework_name)

    def test_homework_loop_02(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_homework_btn_loc, loading=True)
        self.subject_add_homework_loop()
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_homework_btn_loc, loading=True)
        self.subject_student_do_homework_loop()
        
    def test_field_01(self):
        """turtle"""
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.do_test_field('turtle')

    def test_field_02(self):
        """pygame"""
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.do_test_field('pygame')

    def test_field_03(self):
        """多文件"""
        filename = Data().test_field_file_name
        output = Data().test_field_output
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.multiple_files_test_field(filename, '多文件测试', output)

    def test_field_04(self):
        """打开草稿"""
        output = Data().test_field_output
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.open_file(output)

    def test_field_05(self):
        """3D打印"""
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.three_dimensional()

    def test_field_06(self):
        """素材库"""
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.upload_material()
        self.edit_material_name(Data().material_name)
        self.delete_material()

    def test_field_07(self):
        """机器人"""
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.robot()

    def test_my_creation_01(self):
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.my_works_tab_loc)
        self.click_button(ElementSelector.public_work_btn_loc, loading=True)
        self.add_work(self.work_name, self.pro_class_name)
        self.get_new_driver()
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.student_work_tab_loc)
        self.audit_work(self.work_name)

    def test_works_hall_01(self):
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.submit_work(self.direct_release_work_name)
        self.add_work(self.direct_release_work_name, self.pro_class_name, test_field=True)
        self.get_new_driver()
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.student_work_tab_loc)
        self.audit_work(self.direct_release_work_name)

    def test_works_hall_02(self):
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.submit_work(self.detailed_review_work_name)
        self.add_work(self.detailed_review_work_name, self.pro_class_name, test_field=True)
        self.get_new_driver()
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.student_work_tab_loc)
        self.audit_work(self.detailed_review_work_name)

    def test_works_hall_03(self):
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.submit_work(self.reject_work_name)
        self.add_work(self.reject_work_name, self.pro_class_name, test_field=True)
        self.get_new_driver()
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.student_work_tab_loc)
        self.audit_work(self.reject_work_name)

    def test_ai_exp_01(self):
        self.login(self.username_teacher, self.teacher_name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.ai_experience_loc, 1)
        self.ai_experience()

    def test_wish_box(self):
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.wish_box()

    def test_wrong_login(self):

        self.user_login_wrong()

    def test_field_error(self):
        """
        试炼场
        :return:
        """
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_and_jump(ElementSelector.test_field_btn_loc, 1)
        self.check_error()

    def test_course_field_error(self):
        """
        课件查看页面精简试炼场
        :return:
        """
        from ui_auto.common.picture_list_code import wrong_code

        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.click_button(ElementSelector.first_course_loc)
        code = wrong_code()
        self.course_field_operation(code, 'Error', wrong=True)


if __name__ == "__main__":
    unittest.main()
