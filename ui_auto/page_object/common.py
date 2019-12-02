from ui_auto.base.data import PointIdIndex
from ui_auto.page_object.element_loc import ElementSelector


class Common:
    @staticmethod
    def choice_point(driver, subject=False):
        if subject:
            s_list = driver.find_elements(*ElementSelector.s1_loc, tag=False)
            s1_btn = s_list[PointIdIndex.checkpoint_level_one_index]
            s1_btn.click()
            level_two_elem_list = driver.find_elements(*ElementSelector.level_two_loc, tag=False)
            level_two_elem = level_two_elem_list[PointIdIndex.checkpoint_level_two_index]
            level_two_elem.click()
        else:
            s_list = driver.find_elements(*ElementSelector.s1_loc, tag=False)
            s1_btn = s_list[PointIdIndex.level_one_index]
            s1_btn.click()
            level_two_elem_list = driver.find_elements(*ElementSelector.level_two_loc, tag=False)
            level_two_elem = level_two_elem_list[PointIdIndex.level_two_index]
            level_two_elem.click()
            level_three_elem_list = driver.find_elements(*ElementSelector.level_three_loc, tag=False)
            level_three_elem = level_three_elem_list[PointIdIndex.level_three_index]
            level_three_elem.click()

    @staticmethod
    def choice_problem_for_homework(driver):
        driver.find_element(*ElementSelector.choice_problem_loc, click=True)
        driver.find_element(*ElementSelector.choice_all_btn_loc, click=True)
        driver.find_element(*ElementSelector.operation_problem_loc, tag=False, click=True)
        driver.find_element(*ElementSelector.choice_all_btn_loc, click=True)
        driver.find_element(*ElementSelector.confirm_btn_loc, tag=False, click=True)
