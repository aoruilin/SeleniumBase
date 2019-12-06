from ui_auto.base.data import Data
from ui_auto.page_object.element_loc import ElementSelector
from ui_auto.page_operation import BaseTestCase


class AddHomeworkLoop(BaseTestCase):

    url = Data().ip_for_edu()
    username = Data().teacher_username_for_edu()
    password = Data().password_for_edu
    username_student = Data().student_username_for_edu()
    student_name = Data().student_name_for_edu()
    name = Data().teacher_name_for_edu()

    def test_add_homework_loop_01(self):
        self.driver.get(self.url)
        self.login(self.username, self.name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.click_button(ElementSelector.homework_btn_loc)
        self.add_homework_loop()
        self.add_homework_wrong()
        self.get_new_driver()
        self.login(self.username_student, self.student_name, self.password, student_assert=True)
        self.click_button(ElementSelector.standard_course_btn_loc)
        self.click_button(ElementSelector.homework_btn_loc)
        self.student_do_homework_loop()
        # self.date_selection('作业', Data().homework_name, enable_assert=True)
        # self.search_input(Data().homework_name, enable_assert=True)

    def test_add_homework_loop_02(self):
        self.driver.get(self.url)
        self.login(self.username, self.name, self.password, teacher_assert=True)
        self.click_button(ElementSelector.checkpoint_course_loc)
        self.click_button(ElementSelector.index_homework_btn_loc)
        self.add_homework_loop()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    AddHomeworkLoop().test_add_homework_loop_01()
