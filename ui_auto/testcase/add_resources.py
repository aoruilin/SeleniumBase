import unittest

from ui_auto.base.data import Data
from ui_auto.base.logs import get_log_path
from ui_auto.page_object.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class AddResourcesCase(BaseTestCase):
    file_name = __file__
    name = __name__

    url = Data().ip_for_edu()
    teacher_data = Data().teacher_data()
    username_teacher = Data().teacher_username_for_edu()
    teacher_name = Data().teacher_name_for_edu()
    password = Data().password_for_edu

    def test_add_resources(self):
        self.step_log_path = get_log_path(self.file_name, self.name)
        self.login(**self.teacher_data, teacher_assert=True)
        self.click_button(*ElementSelector.teach_management_btn_loc)
        self.click_button(*ElementSelector.resource_manage_tab_loc,
                          loading=True)
        self.click_button(*ElementSelector.resource_type_sel_loc,
                          loading=False, wait=True)
        self.click_button(*ElementSelector.school_resource_btn_loc,
                          wait=True)
        self.add_resources()


if __name__ == "__main__":
    unittest.main()
