import time
import unittest
from itertools import chain

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.homework_operation import add_homework
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class CourseController(unittest.TestCase):
    """课程页面"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.point_id_tup = self.teacher_parm.get_point_id()
        self.all_point_id = self.teacher_parm.get_all_point_id(1)
        self.class_id_list = self.teacher_parm.get_class_list(get_all=True)
        self.series_id_list = self.teacher_parm.get_series_list()
        _, self.school_id = self.teacher_parm.get_user_school_id()

    def test_01_post_homework(self):
        """
        老师发布单个作业
        :return:
        """
        param = {
            'hw_name': '接口发布作业',
            'series_id': self.series_id_list[0],
            'point_id_list': [self.point_id_tup[0]],
            'show_answer': 1,
            'show_difficulty': 1,
            'timing': 0
        }
        add_homework(self.teacher_parm, **param)

    def test_02_post_homework_loop(self):
        """
        老师遍历发布设置发布作业
        :return:
        """
        for a in range(2):
            for d in range(2):
                for t in range(2):
                    param = {
                        'hw_name': f'答案{a}难度{d}定时{t}',
                        'series_id': self.series_id_list[0],
                        'point_id_list': [self.point_id_tup[0]],
                        'show_answer': a,
                        'show_difficulty': d,
                        'timing': t
                    }
                    add_homework(self.teacher_parm, **param)

    def test_03_post_all_problem(self):
        """
        老师发布全部题目，发之前要确定这个班有权限
        :return:
        """
        for series_id in self.series_id_list:
            all_point_id_list = self.teacher_parm.get_all_point_id(series_id)
            add_homework(self.teacher_parm, f'S{series_id}所有题目',
                         series_id, all_point_id_list, [1, 2, 3], 1, 1, 0)

    def test_04_teacher_homework_list(self):
        """
        老师作业列表
        :return:
        """
        url = f'{self.ip}/homework/tchHwList'
        for class_id in list(chain(self.class_id_list, [''])):
            for homework_name in ['', '接口']:
                for status in ['', 1, 2, 3]:  # 待定
                    data = {
                        'schoolId': self.school_id,
                        'classId': class_id,
                        'homeworkName': homework_name,
                        'pageSize': 30,
                        'status': status,
                        'currPage': 1
                    }
                    res = requests.post(url=url, headers=self.teacher_headers, json=data)
                    assert_res(res.text)
                    data_ret = res.json()
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口"/homework/tchHwList"报错，返回{data_ret["msg"]}')
                    except KeyError:
                        print(f'接口"/homework/tchHwList"返回{data_ret}')
                    else:
                        print([{i['homeworkId']: i['homeworkName']} for i in data_list])

    def test_05_teacher_homework_class_list(self):
        """
        老师发布作业班级选择
        :return:
        """
        url = f'{self.ip}/homework/tchHwClassList'
        data = {
            "schoolId": self.school_id,
            "seriesId": self.series_id_list[0]
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print(data_ret['data'])
        except TypeError:
            print(f'接口"/homework/tchHwClassList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwClassList"返回{data_ret}')

    def test_06_teacher_current_student_list(self):
        """
        教师端题目当前学生列表
        :return:
        """
