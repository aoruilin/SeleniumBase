import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.course_operation import add_course, edit_course
from interface.K12edu.common.course_operation import finish_course, del_course
from interface.K12edu.common.picture_list_code import turtle_code


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
        for f in [1, 0]:  # 0-关闭 1-开启
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
                data_dic = data_ret['data']
                print(f"{data_dic['practisedCount']}/{data_dic['practiseCount']},{data_dic['avgCorrectRate']}")
                practises_data = data_dic['practises']
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

    def test_07_teacher_classes(self):
        """
        老师-可选班级
        :return:
        """
        url = f'{self.ip}/course/teacher/classes'
        for series_id in self.series_id_list:
            params = f'seriesId={series_id}'
            res = requests.get(url=url, headers=self.teacher_headers, params=params)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                print([{i['id']: i['name']} for i in data_ret['data']])
            except TypeError:
                print(f'接口"/course/teacher/classes"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/course/teacher/classes"返回{data_ret}')

    def test_08_user_course(self):
        """
        课程信息
        :return:
        """
        course_id_list = self.teacher_parm.get_user_course_list()
        for course_id in course_id_list:
            url = f'{self.ip}/course/user/course/{course_id}'
            res = requests.get(url=url, headers=self.teacher_headers)
            assert_res(res.text)
            data_ret = res.json()
            try:
                data_dic = data_ret['data']
                print((data_dic['id'], data_dic['issuer']))
            except TypeError:
                print(f'接口"/course/user/course"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/course/user/course"返回{data_ret}')

    def test_09_save_play_code(self):
        """
        课程-保存试炼场用户代码
        :return:
        """
        url = f'{self.ip}/course/user/save/playCode'
        data = {
            "classId": self.class_id_list[0],
            "courseId": self.course_id_list[0],
            "pointId": self.point_id_tup[0],
            "seriesId": self.series_id_list[0],
            "userCode": turtle_code()
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            save = data_ret['data']
        except TypeError:
            print(f'接口"/course/user/save/playCode"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/course/user/save/playCode"返回{data_ret}')
        else:
            if save:
                url = f'{self.ip}/course/user/query/playCode'
                res = requests.post(url=url, headers=self.teacher_headers, json=data)
                assert_res(res.text)
                data_ret = res.json()
                try:
                    print(data_ret['data'])
                except TypeError:
                    print(f'接口"/course/user/query/playCode"报错，返回{data_ret["msg"]}')
                except KeyError:
                    print(f'接口"/course/user/query/playCode"返回{data_ret}')

    def test_10_tag_course_current(self):
        """
        课程-已发布-当前授课标签信息
        :return:
        """
        url = f'{self.ip}/course/user/tag/course/current'
        res = requests.get(url=url, headers=self.teacher_headers)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_dic = data_ret['data']
            print((data_dic['className'], data_dic['id']))
        except TypeError:
            print(f'接口"/course/user/tag/course/current"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/course/user/tag/course/current"返回{data_ret}')

    def test_11_tag_course_point_current(self):
        """
        课程-已发布-当前授课知识点标签信息
        :return:
        """
        url = f'{self.ip}/course/user/tag/course/point/current'
        params = f'courseId={self.course_id_list[0]}&classId={self.class_id_list[-1]}'
        res = requests.get(url=url, headers=self.teacher_headers, params=params)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_dic = data_ret['data']
            print((data_dic['label'], data_dic['resourceId']))
        except TypeError:
            print(f'接口"/course/user/tag/course/point/current"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/course/user/tag/course/point/current"返回{data_ret}')


if __name__ == '__main__':
    unittest.main()
