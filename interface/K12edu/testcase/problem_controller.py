import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class ProblemController(unittest.TestCase):
    """题目接口"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.problem_id_list = self.student_parm.get_problem_id()

    def test_01_problem(self):
        """
        获取题目列表
        :return:
        """
        url = f'{self.ip}/pc/problem'
        series_id_list = self.teacher_parm.get_series_list()
        for series_id in series_id_list:
            point_id_list = self.teacher_parm.get_all_point_id(series_id)
            for point_id in point_id_list:
                for d in range(1, 4):
                    data = f'klPoints={point_id}&pageNum=1&pageSize=12&difficulty={d}'
                    response = requests.get(url=url, headers=self.teacher_headers,
                                            params=data)
                    assert_res(response.text)
                    time.sleep(1)
                    data_ret = response.json()
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口"/pc/problem"报错，返回{data_ret["msg"]}')
                    else:
                        print([{i['id']: i['title']} for i in data_list])

    def test_02_problem_multi(self):
        """
        获取题目详情,在多文件编辑器中展示
        :return:
        """
        url = f'{self.ip}/pc/problem/multi/{self.problem_id_list[0]}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print({data_ret['data']['title']: data_ret['data']['homeworkRunEvalInfoModule']['result']})
        except TypeError:
            print(f'接口"/pc/problem/multi"报错，返回{data_ret["msg"]}')

    def test_03_problem_id(self):
        """
        获取题目
        :return:
        """
        url = f'{self.ip}/pc/problem/{self.problem_id_list[0]}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print({data_ret['data']['title']: data_ret['data']['id']})
        except TypeError:
            print(f'接口"/pc/problem"报错，返回{data_ret["msg"]}')

    def test_04_problem_feedback(self):
        """
        提交题目有误信息
        :return:
        """
        url = f'{self.ip}/pc/problemFeedback'
        user_id, _ = self.student_parm.get_user_school_id()
        for f in range(1, 4):
            for t in range(1, 3):
                data = {
                    "feedbackDetail": "string",
                    "feedbackType": [
                        f
                    ],
                    "problemId": self.problem_id_list[0],
                    "targetType": t,
                    "userId": user_id
                }
                response = requests.post(url=url, headers=self.student_headers,
                                         json=data)
                assert_res(response.text)
                time.sleep(1)


if __name__ == '__main__':
    unittest.main()
