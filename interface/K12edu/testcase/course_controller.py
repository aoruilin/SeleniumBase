import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.course_operation import add_course, edit_course
from interface.K12edu.common.course_operation import finish_course, del_course


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

        self.course_id_list = self.teacher_parm.get_user_course_list()
        self.point_id_tup = self.teacher_parm.get_point_id()
        self.all_point_id = self.teacher_parm.get_all_point_id(1)
        self.class_id_list = self.teacher_parm.get_class_list(get_all=True)
        self.series_id_list = self.teacher_parm.get_series_list()

    def test_01_teacher_issue(self):
        """
        老师单独发布一个课程并编辑删除
        :return:
        """
        add_course(self.teacher_parm, self.class_id_list[-1], self.series_id_list[0])
        edit_course(self.teacher_parm, self.course_id_list[0], course_plan=True)
        finish_course(self.teacher_parm, self.course_id_list[0])
        del_course(self.teacher_parm, self.course_id_list[0])

    def test_02_teacher_issue(self):
        """
        老师发布所有系列课程
        :return:
        """
        for series_id in self.series_id_list:
            add_course(self.teacher_parm, self.class_id_list[-1], series_id)
            time.sleep(1)

    def test_03_teacher_switch_point(self):
        """
        老师切换知识点标识
        :return:
        """
        for f in [1, 0]:
            url = f'{self.ip}/course/teacher/' \
                  f'{self.course_id_list[0]}/{self.class_id_list[-1]}/{self.point_id_tup[1]}/switch/{f}'
            res = requests.get(url=url, headers=self.teacher_headers)
            assert_res(res.text)
            time.sleep(1)

    def test_04_user_courses(self):
        """
        用户课程列表
        :return:
        """
        url = f'{self.ip}/course/user/courses'
        for class_id in self.class_id_list:
            for series_id in self.series_id_list:
                data = {
                    "classId": class_id,
                    "flag": 1,
                    "pageNum": 1,
                    "pageSize": 12,
                    "seriesId": series_id
                }
                res = requests.post(url=url, headers=self.student_headers, json=data)
                assert_res(res.text)
                time.sleep(1)
                data_ret = res.json()
                try:
                    data_list = data_ret['data']['list']
                except TypeError:
                    print(f'接口"/course/user/courses"报错，返回{data_ret["msg"]}')
                except KeyError:
                    print(f'接口"/course/user/courses"返回{data_ret}')
                else:
                    print([{i['id']: [i['seriesName'], i['issueName']]} for i in data_list])

    def test_05_user_course_point_tag(self):
        """
        课程知识点标签信息
        :return:
        """
        url = f'{self.ip}/course/user/tag/course/points'
        for course_id in self.course_id_list:
            params = f'courseId={course_id}&classId={self.class_id_list[-1]}'
            res = requests.get(url=url, headers=self.teacher_headers, params=params)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                data_list = data_ret['data']
                print([{i['label']: [{s['label']: s['flag']} for s in i['children']]} for i in data_list])
            except TypeError:
                print(f'接口"/course/user/tag/course/points"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/course/user/tag/course/points"返回{data_ret}')

    def test_06_teacher_practises(self):
        """
        老师查看学生练习
        :return:
        """
        for point_id in self.all_point_id:
            url = f'{self.ip}/course/teacher/' \
                  f'{self.course_id_list[0]}/{self.class_id_list[-1]}/{point_id}/practises'
            res = requests.get(url=url, headers=self.teacher_headers)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                print(f"{data_ret['practisedCount']}/{data_ret['practiseCount']},{data_ret['avgCorrectRate']}")
                practises_data = data_ret['practises']
                print(
                    [
                        {i['name']: i['correctRate'], 'subject': [{p['name']: p['result']}
                                                                  for p in
                                                                  practises_data['subjects']]}
                        for i
                        in practises_data
                    ]
                )
                print('#################################################')
            except TypeError:
                print(f'接口"/course/user/tag/course/points"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/course/user/tag/course/points"返回{data_ret}')
