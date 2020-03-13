import unittest
import requests
import time

from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.assert_msg import assert_res
from interface.common.time_parameter import time_stamp


class AddHomeworkLoop(unittest.TestCase):
    """覆盖所有发布设置添加作业"""

    def setUp(self):
        self.parameter = ParameterForOthers(identity='teacher')
        self.ip = self.parameter.ip
        self.headers = self.parameter.headers

    def test_01(self):
        """覆盖所有发布设置添加作业"""
        url = f'{self.ip}/pc/homework'
        class_id = self.parameter.get_class_list(1)

        end_time = time_stamp(end=True)
        start_time = time_stamp(start=True)
        s_list = ['0', start_time]

        point_id = self.parameter.get_point_id()
        choice_problem_list = self.parameter.get_choice_problem_id()
        problem_id_list = self.parameter.get_problem_id()
        item_list = []
        for problem_id in problem_id_list:
            item_list.append({'pointId': point_id[1], 'problemId': str(problem_id)})
        choice_items = []
        for choice_problem_id in choice_problem_list:
            choice_items.append({'pointId': point_id[1], 'problemId': str(choice_problem_id)})

        # for r in range(0, 2):
        for a in range(0, 3):
            for s in s_list:
                data = {}
                name = f'答案{a}定时{s}'
                data['choiceItems'] = choice_items
                data['items'] = item_list
                data['classIds'] = class_id
                data['endTime'] = end_time
                data['name'] = name
                data['showRunResult'] = 1
                data['showStandardAnswer'] = a
                data['startTime'] = s
                response = requests.post(url=url, headers=self.headers, json=data)
                assert_res(response.text, '操作成功')
                time.sleep(3)

    def test_02(self):
        """闯关授课发布作业覆盖发布设置组合"""
        url = f'{self.ip}/pc/gate/homework/homework'
        class_id = self.parameter.get_class_list(1)

        end_time = time_stamp(end=True)
        start_time = time_stamp(start=True)
        s_list = ['0', start_time]

        id_dic = self.parameter.get_point_id_checkpoint()
        point_id = id_dic['point_id']
        gate_id = id_dic['gate_id']
        problem_id_list = self.parameter.get_problem_id(check_point=True)
        item_list = []
        for problem_id in problem_id_list:
            item_list.append({'pointId': point_id, 'problemId': str(problem_id)})

        for a in range(0, 3):
            for s in s_list:
                data = {}
                name = f'答案{a}定时{s}'
                data['items'] = item_list
                data['classIds'] = class_id
                data['gateId'] = gate_id
                data['endTime'] = end_time
                data['name'] = name
                data['showRunResult'] = 1
                data['showStandardAnswer'] = a
                data['startTime'] = s
                response = requests.post(url=url, headers=self.headers, json=data)
                assert_res(response.text, '操作成功')
                time.sleep(3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
