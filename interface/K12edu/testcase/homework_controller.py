import time
import unittest
from itertools import chain

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.homework_operation import add_homework, oj_data, do_homework_simple
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class HomeworkController(unittest.TestCase):
    """作业页面"""

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
        self.teacher_class_id_list = self.teacher_parm.get_class_list(get_all=True)
        self.student_class_id_list = self.student_parm.get_class_list(get_all=True)
        self.series_id_list = self.teacher_parm.get_series_list(2)
        self.teacher_id, self.school_id = self.teacher_parm.get_user_school_id()
        self.student_id, _ = self.student_parm.get_user_school_id()
        self.teacher_homework_id_list = self.teacher_parm.get_homework_id_list(teacher=True)
        self.student_homework_id_list = self.student_parm.get_homework_id_list()
        self.teacher_problem_id_list = self.teacher_parm.teacher_get_homework_problem_id_list()
        self.student_problem_id_list = self.student_parm.student_get_problem_id_list()

    def test_01_post_homework(self):
        """
        老师发布单个作业
        :return:
        """
        param = {
            'hw_name': '接口发布作业',
            'series_id': self.series_id_list[1],
            'point_id_list': [self.point_id_tup[0]],
            'show_answer': 1,
            'show_difficulty': 1,
            'timing': 0
        }
        add_result = add_homework(self.teacher_parm, **param)
        if add_result:
            c = 0
            for student_username in self.teacher_parm.teacher_get_hw_student_num():
                student_param = ParameterForOthers('student', student_username)
                do_homework_simple(student_param, cut_num=c)
                c -= 1

    def test_02_post_homework_loop(self):
        """
        老师遍历发布设置发布作业
        :return:
        """
        for a in range(3):
            for d in range(2):
                for t in range(2):
                    param = {
                        'hw_name': f'答案{a}难度{d}定时{t}',
                        'series_id': self.series_id_list[1],
                        'point_id_list': [self.point_id_tup[0]],
                        'show_answer': a,
                        'show_difficulty': d,
                        'timing': t
                    }
                    add_result = add_homework(self.teacher_parm, **param)
                    if add_result and t == 0:
                        c = 0
                        for student_username in self.teacher_parm.teacher_get_hw_student_num():
                            student_param = ParameterForOthers('student', student_username)
                            do_homework_simple(student_param, cut_num=c)
                            c -= 1

    def test_03_post_simple_series_problem(self):
        """
        教师发布单个系列全部题目
        :return:
        """
        series_id = 1
        all_point_id_list = self.teacher_parm.get_all_point_id(series_id)
        for point_id in all_point_id_list:
            param = {
                'hw_name': f'S{series_id}的{point_id}',
                'series_id': series_id,
                'point_id_list': [point_id],
                'show_answer': 1,
                'show_difficulty': 1,
                'timing': 0
            }
            add_result = add_homework(self.teacher_parm, **param)
            if add_result:
                c = 0
                for student_username in self.teacher_parm.teacher_get_hw_student_num():
                    student_param = ParameterForOthers('student', student_username)
                    do_homework_simple(student_param, cut_num=c)
                    c -= 1

    def test_03_post_all_problem(self):
        """
        老师发布全部题目，发之前要确定这个班有权限
        :return:
        """
        for series_id in self.series_id_list:
            all_point_id_list = self.teacher_parm.get_all_point_id(series_id)
            for point_id in all_point_id_list:
                param = {
                    'hw_name': f'S{series_id}的{point_id}',
                    'series_id': series_id,
                    'point_id_list': all_point_id_list,
                    'show_answer': 1,
                    'show_difficulty': 1,
                    'timing': 0
                }
                add_homework(self.teacher_parm, **param)
                do_homework_simple(self.student_parm, cut_num=None)

    def test_04_teacher_homework_list(self):
        """
        老师作业列表
        :return:
        """
        url = f'{self.ip}/homework/tchHwList'
        for class_id in list(chain(self.teacher_class_id_list, [''])):
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
            "seriesId": self.series_id_list[1]
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

    def test_06_teacher_homework_analysis_list(self):
        """
        教师端题目分析统计列表
        :return:
        """
        url = f'{self.ip}/homework/tchHwAnalysisList'
        data = {
            "currPage": 1,
            "hwId": self.teacher_homework_id_list[0],
            "pageSize": 30
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/homework/tchHwAnalysisList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwAnalysisList"返回{data_ret}')
        else:
            print([{i['problemId']: [i['problemName'], i['correctRate']]} for i in data_list])

    def test_07_teacher_homework_analysis_problem_list(self):
        """
        教师端-题目分析-题目列表
        :return:
        """
        url = f'{self.ip}/homework/tchHwAnsProblemList'
        data = {
            "hwId": self.teacher_homework_id_list[0]
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['problemId']: [i['problemName'], i['correctRate']]} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/homework/tchHwAnsProblemList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwAnsProblemList"返回{data_ret}')

    def test_08_teacher_homework_class_list(self):
        """
        教师端作业发布班级选择
        :return:
        """
        url = f'{self.ip}/homework/tchHwClassList'
        data = {
            "schoolId": self.school_id,
            "seriesId": self.series_id_list[1],
            "seriesType": 0
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['id']: i['name']} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/homework/tchHwClassList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwClassList"返回{data_ret}')

    def test_09_teacher_homework_current_student_list(self):
        """
        教师端当前作业学生下拉列表
        :return:
        """
        self.teacher_problem_id_list = self.teacher_parm.teacher_get_homework_problem_id_list()
        url = f'{self.ip}/homework/tchHwCurrentStuList'
        for subject_id, subject_type in self.teacher_problem_id_list:
            data = {
                "hwId": self.teacher_homework_id_list[0],
                "subjectId": subject_id,
                "subjectType": subject_type
            }
            res = requests.post(url=url, headers=self.teacher_parm.headers, json=data)
            assert_res(res.text)
            data_ret = res.json()
            try:
                print([(i['studentId'], i['studentName'], i['status']) for i in data_ret['data']])
            except TypeError:
                print(f'接口"/homework/tchHwCurrentStuList"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/homework/tchHwCurrentStuList"返回{data_ret}')

    def test_10_teacher_homework_list(self):
        """
        教师作业信息查询
        :return:
        """
        url = f'{self.ip}/homework/tchHwList/{self.teacher_homework_id_list[0]}'
        res = requests.get(url=url, headers=self.teacher_headers)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print({data_ret['data']['hwName']: data_ret['data']['status']})
        except TypeError:
            print(f'接口"/homework/tchHwList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwList"返回{data_ret}')

    def test_11_teacher_homework_problem_info(self):
        """
        教师端题目查看
        :return:
        """
        url = f'{self.ip}/homework/tchHwProblemInfo'
        for subject_id, subject_type in self.teacher_problem_id_list:
            data = {
                "hwId": self.teacher_homework_id_list[0],
                "studentId": self.student_id,
                "subjectId": subject_id,
                "subjectType": subject_type
            }
            res = requests.post(url=url, headers=self.teacher_headers, json=data)
            assert_res(res.text)
            data_ret = res.json()
            try:
                print({data_ret['data']['problemId']: data_ret['data']['problemName']})
            except TypeError:
                print(f'接口"/homework/tchHwProblemInfo"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/homework/tchHwProblemInfo"返回{data_ret}')

    def test_12_teacher_homework_problem_list(self):
        """
        教师端-学生列表-题目列表查询
        :return:
        """
        url = f'{self.ip}/homework/tchHwProblemList'
        data = {
            "hwId": self.teacher_homework_id_list[0],
            "stuId": self.student_id
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['problemName']: i['problemStatus']} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/homework/tchHwProblemList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwProblemList"返回{data_ret}')

    def test_13_teacher_homework_problem_oj(self):
        """
        教师端-测评-预览测评/指定学生
        :return:
        """
        url = f'{self.ip}/homework/tchHwProblemOj'
        for subject_id, subject_type in self.teacher_problem_id_list:
            data = oj_data(subject_id, subject_type, self.teacher_homework_id_list[0])
            res = requests.post(url=url, headers=self.teacher_headers, json=data)
            assert_res(res.text)

    def test_14_teacher_homework_series_list(self):
        """
        教师端-作业发布-系列下拉选取
        :return:
        """
        url = f'{self.ip}/homework/tchHwSeriesList'
        data = {
            "classIds": self.teacher_class_id_list,
            "schoolId": self.school_id
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['name']: i['id']} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/homework/tchHwSeriesList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwSeriesList"返回{data_ret}')

    def test_15_teacher_homework_student_list(self):
        """
        教师端-学生成绩列表
        :return:
        """
        url = f'{self.ip}/homework/tchHwStuList'
        data = {
            "currPage": 1,
            "hwId": self.teacher_homework_id_list[0],
            "pageSize": 30
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/homework/tchHwStuList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwStuList"返回{data_ret}')
        else:
            print([{
                      i['studentName']: [i['result'], i['correctCount'], i['finishedCount'], i['level']]
                  } for i in data_list])

    def test_16_teacher_homework_student_resend(self):
        """
        教师端-学生作业重交
        :return:
        """
        url = f'{self.ip}/homework/tchHwStuResend'
        data = {
            "studentEvalId": self.teacher_parm.teacher_get_student_eval_id_list()[-1]
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)

    def test_17_teacher_homework_delete(self):
        """
        教师删除作业
        :return:
        """
        url = f'{self.ip}/homework/tchHwDelete'
        data = {
            "classId": self.teacher_class_id_list[-1],
            "hwId": self.teacher_homework_id_list[0]
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)

    def test_18_student_homework_list(self):
        """
        学生端-作业列表-作业列表查询
        :return:
        """
        url = f'{self.ip}/homework/stuHwList'
        class_id_list = self.student_class_id_list
        class_id_list.append('')
        for class_id in class_id_list:
            for status in ['', 0, 1, 2]:
                for homework_name in ['', '接口']:
                    data = {
                        "classId": class_id,
                        "currPage": 1,
                        "homeworkName": homework_name,
                        "pageSize": 100,
                        "schoolId": self.school_id,
                        "status": status
                    }
                    res = requests.post(url=url, headers=self.student_headers, json=data)
                    assert_res(res.text)
                    time.sleep(1)
                    data_ret = res.json()
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口"/homework/stuHwList"报错，返回{data_ret["msg"]}')
                    except KeyError:
                        print(f'接口"/homework/stuHwList"返回{data_ret}')
                    else:
                        print([{i['homeworkId']: i['homeworkName']} for i in data_list])

    def test_19_student_homework_add_eval(self):
        """
        学生端-作业列表-开始做作业(exist为0时调用)
        :return:
        """
        url = f'{self.ip}/homework/stuHwAddEval'
        data = {
            "hwId": self.student_homework_id_list[0]
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_dic = data_ret['data']
            print((data_dic['studentName'], data_dic['result']))
        except TypeError:
            print(f'接口"/homework/stuHwAddEval"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/stuHwAddEval"返回{data_ret}')

    def test_20_student_homework_problem_info(self):
        """
        学生端-作业题目-详细查询
        :return:
        """
        url = f'{self.ip}/homework/stuHwProblemInfo'
        for p, t in self.student_problem_id_list:
            data = {
                "hwId": self.student_homework_id_list[0],
                "subjectId": p,
                "subjectType": t
            }
            res = requests.post(url=url, headers=self.student_headers, json=data)
            assert_res(res.text)
            data_ret = res.json()
            try:
                data_dic = data_ret['data']
                print((data_dic['problemName'], data_dic['problemAnswer'], data_dic['userCode']))
            except TypeError:
                print(f'接口"/homework/stuHwProblemInfo"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/homework/stuHwProblemInfo"返回{data_ret}')

    def test_21_student_homework_student_info(self):
        """
        学生端-作业列表-学生信息栏查询
        :return:
        """
        url = f'{self.ip}/homework/stuHwStuInfo'
        data = {
            "hwId": self.student_homework_id_list[0]
        }
        res = requests.post(url=url, headers=self.student_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_dic = data_ret['data']
            print((data_dic['studentName'], data_dic['result'], data_dic['finishedCount']))
        except TypeError:
            print(f'接口"/homework/stuHwStuInfo"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/stuHwStuInfo"返回{data_ret}')


if __name__ == '__main__':
    unittest.main()
