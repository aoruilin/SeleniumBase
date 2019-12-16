import unittest

from ui_auto.base.data import Data
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class AddResourcesCase(BaseTestCase):

    url = Data().ip_for_edu()
    username_teacher = Data().teacher_username_for_edu()
    teacher_name = Data().teacher_name_for_edu()
    password = Data().password_for_edu

    def test_add_resources(self):
        self.login(self.username_teacher, self.teacher_name, self.password,
                   teacher_assert=True)
        self.click_button(ElementSelector.teach_management_btn_loc)
        self.click_button(ElementSelector.resource_manage_tab_loc)
        self.click_button(ElementSelector.resource_type_sel_loc,
                          loading=False, wait=True)
        self.click_button(ElementSelector.school_resource_btn_loc)
        self.add_resources()


if __name__ == "__main__":
    unittest.main()
