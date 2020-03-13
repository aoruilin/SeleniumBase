import unittest
import requests
import time

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class ClassManage(unittest.TestCase):

    def setUp(self) -> None:
        self.manager_param = ParameterForOthers(identity='manager')
        self.teacher_param = ParameterForOthers(identity='teacher')
        self.student_param = ParameterForOthers(identity='student')
        self.ip = self.teacher_param.ip
        self.class_id = self.manager_param.get_class_list(1)[0]
        self.manager_id, _ = self.manager_param.get_user_school_id()
        self.student_id_list = self.teacher_param.get_class_student_id()

    def test_01_add_course(self):
        """
        管理员创建班级
        :return:
        """
        url = f'{self.ip}/pc/class/addCourse'
        data = {
            'className': '接口添加班级，待删除',
            'seriesIds': ['1', '3'],
            'teacherIds': [str(self.manager_id)]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_02_add_form_student(self):
        """
        表单填写信息新建学生
        :return:
        """
        url = f'{self.ip}/pc/class/addFormStudents'
        data = {
            'classId': self.class_id,
            'gender': 1,
            'mobile': '',
            'nickname': '接口学生待删',
            'studentNo': 'E00003'
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_03_add_course_student(self):
        """
        选取添加学生
        :return:
        """
        url = f'{self.ip}/pc/class/addCourseStudents'
        for i in range(2):
            data = {
                'classId': self.class_id,
                'studentIds': [str(self.student_id_list[i])]
            }
            res = requests.post(url=url, headers=self.manager_param.headers, json=data)
            assert_res(res.text)
            time.sleep(1)

    def test_04_upd_student(self):
        """
        班级管理修改学生
        :return:
        """
        url = f'{self.ip}/pc/class/updStudents'
        for s in [3, 2]:
            data = {
                'classId': self.class_id,
                'gender': 2,
                'mobile': None,
                'nickname': '接口修改学生',
                'studentId': self.student_id_list[0],
                'studentNo': f'csxs000{s}'
            }
            res = requests.post(url=url, headers=self.manager_param.headers, json=data)
            assert_res(res.text)
            time.sleep(1)

    def test_05_reset_password(self):
        """
        重置密码
        :return:
        """
        url = f'{self.ip}/pc/class/resetPassword'
        data = {
            'classId': self.class_id,
            'userId': self.student_id_list[0]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_06_reset_student_password(self):
        """
        管理员重置学生密码
        :return:
        """
        url = f'{self.ip}/pc/class/resetStudentPassword'
        data = {'userId': self.student_id_list[0]}
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_07_del_students(self):
        """
        管理员删除班级学生
        :return:
        """
        url = f'{self.ip}/pc/class/delStudents'
        data = {
            'classId': self.class_id,
            'studendIds': [self.student_id_list[0]]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    # def test_08_del_students_all(self):
    #     """
    #     彻底删除学生
    #     :return:
    #     """
    #     url = f'{self.ip}/pc/class/delStudentsAll'
    #     student_id = self.manager_param.get_my_manage_students()[0]
    #     data = {
    #         'studendIds': [student_id]
    #     }
    #     res = requests.post(url=url, headers=self.manager_param.headers, json=data)
    #     assert_res(res.text)
    #     time.sleep(1)

    def test_09_upd_course(self):
        """
        修改课程班
        :return:
        """
        url = f'{self.ip}/pc/class/updCourse'
        teacher_id, _ = self.teacher_param.get_user_school_id()
        data = {
            'classId': self.class_id,
            'className': '接口修改班级',
            'seriesIds': ['1'],
            'teacherIds': [self.manager_id, str(teacher_id)]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_10_del_student_by_teacher(self):
        """
        老师删除班级学生
        :return:
        """
        url = f'{self.ip}/pc/class/delStudentsByTeacher'
        data = {
            'classId': self.class_id,
            'studendIds': [str(self.student_id_list[0])]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_11_del_course(self):
        """
        删除对应班级
        :return:
        """
        url = f'{self.ip}/pc/class/delete'
        data = {'classId': self.class_id}
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_12_teacher_list(self):
        url = f'{self.ip}/pc/manage/teacherList'
        data = 'pageNum=1&pageSize=12&desc=0'
        res = requests.get(url=url, headers=self.manager_param.headers, params=data)
        assert_res(res.text)


if __name__ == "__main__":
    unittest.main()
