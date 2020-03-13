import time
import unittest
from itertools import chain

import requests

from interface.common.time_parameter import time_stamp
from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.homework_operation import do_homework_simple


class DoAllProblem(unittest.TestCase):
    """
    一次发布单个系列所有知识点的所有题目并作答提交
    """

    def setUp(self) -> None:
        self.teacher_param = ParameterForOthers(identity='teacher')
        self.student_param = ParameterForOthers(identity='student')
        self.ip = self.teacher_param.ip
        self.teacher_headers = self.teacher_param.headers
        self.student_headers = self.student_param.headers

    def test_01(self):
        series_id_list = self.teacher_param.get_series_list()
        for s in series_id_list:
            add_homework_url = f'{self.ip}/pc/homework'
            class_id = self.teacher_param.get_class_list(s)
            point_id_list = self.teacher_param.get_all_point_id(s)
            series_problem_id_list = []
            series_choice_problem_id_list = []
            if point_id_list:
                for point_id in point_id_list:
                    try:
                        choice_problem_id_list = self.teacher_param.get_all_choice_problem_id(point_id)
                        time.sleep(1)
                        choice_item = [{'pointId': str(point_id), 'problemId': str(choice_problem_id)}
                                       for choice_problem_id in choice_problem_id_list]
                    except TypeError:
                        pass
                    else:
                        series_choice_problem_id_list.append(choice_item)
                    problem_id_list = self.teacher_param.get_all_problem_id(point_id)
                    time.sleep(1)
                    item = [{'pointId': str(point_id), 'problemId': str(problem_id)} for problem_id in problem_id_list]
                    series_problem_id_list.append(item)
                all_problem_id = list(chain(*series_problem_id_list))
                all_choice_problem_id = list(chain(*series_choice_problem_id_list))
                end_time = time_stamp(end=True)
                add_homework_data = {
                    "showRunResult": 1,
                    "showStandardAnswer": 1,
                    "startTime": None,
                    'name': f'S{s}全部题目',
                    'classIds': class_id,
                    'endTime': end_time,
                    'choiceItems': all_choice_problem_id,
                    'items': all_problem_id
                }
                response = requests.post(url=add_homework_url, headers=self.teacher_param.headers,
                                         json=add_homework_data)
                assert_res(response.text)
                do_homework_simple(self.student_param, cut_num=None, traditional_teach=True)

    def test_02_do_problem_num(self):
        """
        做指定数量的题
        :return:
        """
        add_homework_url = f'{self.ip}/pc/homework'
        class_id = self.teacher_param.get_class_list(1)
        point_id_list = self.teacher_param.get_all_point_id(1)
        series_problem_id_list = []
        series_choice_problem_id_list = []
        if point_id_list:
            for c in [-1, -15, -16, -30, -31, -40, -41]:
                for point_id in point_id_list:
                    try:
                        choice_problem_id_list = self.teacher_param.get_all_choice_problem_id(point_id)
                        time.sleep(1)
                        choice_item = [{'pointId': str(point_id), 'problemId': str(choice_problem_id)}
                                       for choice_problem_id in choice_problem_id_list]
                    except TypeError:
                        pass
                    else:
                        series_choice_problem_id_list.append(choice_item)
                    problem_id_list = self.teacher_param.get_all_problem_id(point_id)
                    time.sleep(1)
                    item = [{'pointId': str(point_id), 'problemId': str(problem_id)} for problem_id in problem_id_list]
                    series_problem_id_list.append(item)
                all_problem_id = list(chain(*series_problem_id_list))
                all_choice_problem_id = list(chain(*series_choice_problem_id_list))
                end_time = time_stamp(end=True)
                add_homework_data = {
                    "showRunResult": 1,
                    "showStandardAnswer": 1,
                    "startTime": None,
                    'name': 'S1的100道题',
                    'classIds': class_id,
                    'endTime': end_time,
                    'choiceItems': all_choice_problem_id[0: 41],
                    'items': all_problem_id[0: 59]
                }
                response = requests.post(url=add_homework_url, headers=self.teacher_param.headers,
                                         json=add_homework_data)
                assert_res(response.text)
                do_homework_simple(self.student_param, cut_num=c, traditional_teach=True)

    def test_03(self):
        """
        主题授课发布一个系列所有知识点的所有题目
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homework'
        class_id = self.teacher_param.get_class_list()
        point_id_list = self.teacher_param.get_all_point_id_checkpoint(1)
        end_time = time_stamp(end=True)
        for gate in range(1, 15):
            point_id = point_id_list[gate - 1]
            problem_id_list = self.teacher_param.get_all_problem_id(point_id, check_point=True)
            time.sleep(1)
            problem_item = [{'pointId': point_id, 'problemId': problem_id} for problem_id in problem_id_list]
            data = {
                'classIds': class_id,
                'endTime': end_time,
                'gateId': str(gate),
                'items': problem_item,
                'name': f'关卡{gate}',
                "showRunResult": 1,
                "showStandardAnswer": 2,
                "startTime": None
            }
            res = requests.post(url=url, headers=self.teacher_param.headers, json=data)
            assert_res(res.text)
            time.sleep(1)
            do_homework_simple(self.student_param, cut_num=None)
