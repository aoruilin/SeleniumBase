import unittest
import requests

from interface.common.time_parameter import time_stamp
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.assert_msg import assert_res


class AddHomework(unittest.TestCase):
    """添加作业"""

    def setUp(self):
        self.parameter = ParameterForOthers(identity='teacher')
        self.ip = self.parameter.ip
        self.headers = self.parameter.headers

    def test_01(self):
        """添加作业"""
        url = f'{self.ip}/pc/homework'

        class_id = self.parameter.get_class_list(1)
        point_id = self.parameter.get_point_id()
        choice_problem_list = self.parameter.get_choice_problem_id()
        problem_id_list = self.parameter.get_problem_id()

        end_time = time_stamp(end=True)

        items = []
        for problem_id in problem_id_list:
            items.append({'pointId': point_id[1], 'problemId': str(problem_id)})
        choice_items = []
        for choice_problem_id in choice_problem_list:
            choice_items.append({'pointId': point_id[1],  'problemId': str(choice_problem_id)})
        data = {
            "showRunResult": 1,
            "showStandardAnswer": 2,
            "startTime": "0"
        }
        name = '接口发布作业'
        data['name'] = name
        data['choiceItems'] = choice_items
        data['items'] = items
        data['classIds'] = class_id
        data['endTime'] = end_time

        response = requests.post(url=url, headers=self.headers, json=data)
        assert_res(response.text, '操作成功')

    def test_02(self):
        """闯关授课添加作业"""
        url = f'{self.ip}/pc/gate/homework/homework'

        class_id = self.parameter.get_class_list(1)
        id_dic = self.parameter.get_point_id_checkpoint()
        point_id = id_dic['point_id']
        gate_id = id_dic['gate_id']
        problem_id_list = self.parameter.get_problem_id(check_point=True)

        end_time = time_stamp(end=True)

        items = []
        for problem_id in problem_id_list:
            items.append({'pointId': point_id, 'problemId': str(problem_id)})

        data = {
            "showRunResult": 1,
            "showStandardAnswer": 2,
            'name': '接口发布作业',
            'items': items,
            'classIds': class_id,
            'endTime': end_time,
            'gateId': gate_id
        }

        response = requests.post(url=url, headers=self.headers, json=data)
        assert_res(response.text, '操作成功')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
