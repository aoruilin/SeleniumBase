from ui_auto.base.data import Data
from ui_auto.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class TestMyCreation(BaseTestCase):

    student_username = Data().student_username_for_edu()
    teacher_username = Data().teacher_username_for_edu()
    student_name = Data().student_name_for_edu()
    teacher_name = Data().teacher_name_for_edu()
    password = Data().password_for_edu
    class_name = Data().pro_class_name_for_edu()
    work_name = Data().direct_release_work_name

    def test_01(self):
        self.login(self.student_username, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.my_works_tab_loc)
        self.click_button(ElementSelector.public_work_btn_loc, wait=True)
        self.add_work(self.work_name, self.class_name, enable_assert=True)
        self.get_new_driver()
        self.login(self.teacher_username, self.teacher_name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.creative_space_loc)
        self.click_button(ElementSelector.student_work_tab_loc)
        self.audit_work(self.work_name, enable_assert=True)
