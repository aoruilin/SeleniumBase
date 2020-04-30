import unittest
import requests
import time

from interface.common.time_parameter import time_stamp
from interface.uni_teach.common.parameter_for_others import ParameterForOthers


class AddHomeworkLoop(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers('teacher')
        ip = self.parameter.ip
        self.url = f'{ip}/pc/homework'
        self.headers = self.parameter.headers

    def test_addHomework(self):
        class_id = self.parameter.get_class_list()
        end_time = time_stamp(end=True)
        start_time = time_stamp(start=True)
        s_list = ['0', start_time]
        point_id = self.parameter.get_point_id()
        problem_id_list = self.parameter.get_problem_id()
        item_list = []
        for problem_id in problem_id_list:
            item_list.append({"pointId": point_id[0], "problemId": str(problem_id)})

        # for r in range(0, 2):
        for a in range(0, 3):
            for s in s_list:
                name = f'答案{a}定时{s}'
                data = {
                    'classIds': class_id, 'endTime': end_time, 'name': name,
                    'showRunResult': 1, 'showStandardAnswer': a,
                    'startTime': s, 'items': item_list
                }
                response = requests.post(url=self.url, headers=self.headers, json=data)
                try:
                    self.assertIn('操作成功', response.text)
                    print(f'{name}作业添加成功')
                except AssertionError as n:
                    print(f'{n}, {name}作业添加失败')
                except Exception as e:
                    print(f'请求失败，发送作业异常，{e}')
                time.sleep(3)
        # print(data)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
