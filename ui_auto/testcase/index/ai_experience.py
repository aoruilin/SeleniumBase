from ui_auto.base.data import Data
from ui_auto.page_operation import BaseTestCase
from ui_auto.page_object.element_loc import ElementSelector


class TestAIExperience(BaseTestCase):

    username = Data().teacher_username_for_edu()
    name = Data().teacher_name_for_edu()
    password = Data().password_for_edu

    def test_01(self):
        self.login(self.username, self.name, self.password, teacher_assert=True)
        self.click_and_jump(ElementSelector.ai_experience_loc, 1)
        self.ai_experience()


if __name__ == "__main__":
    TestAIExperience().test_01()
