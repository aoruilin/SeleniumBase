import unittest
import requests
import time

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TeacherManageController(unittest.TestCase):

    def setUp(self) -> None:
        self.manager_param = ParameterForOthers(identity='manager')
        self.teacher_param = ParameterForOthers(identity='teacher')
        self.student_param = ParameterForOthers(identity='student')
        self.ip = self.manager_param.ip
        self.manager_headers = self.manager_param.headers

        self.teacher_id_list = self.manager_param.get_manage_teacher_list()
        self.manager_id, _ = self.manager_param.get_user_school_id()
        self.teacher_mobile_num = '1520800000'

    def test_01_get_manage_class_list(self):
        """
        管理员获取所有班级列表
        :return:
        """
        url = f'{self.ip}/pc/manage/classList'
        params = f'teacherId={self.manager_id}'
        res = requests.get(url=url, headers=self.manager_headers, params=params)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['id']: i['name']} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/manage/classList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_02_manager_reset_password(self):
        """
        管理员重置密码
        :return:
        """
        url = f'{self.ip}/pc/manage/restPassword'
        teacher_id, _ = self.teacher_param.get_user_school_id()
        student_id, _ = self.student_param.get_user_school_id()
        for user_id in [teacher_id, student_id]:
            data = {
                'userId ': user_id
            }
            res = requests.put(url=url, headers=self.manager_headers, json=data)
            assert_res(res.text)

    def test_03_add_teacher(self):
        """
        管理员添加老师：不添加班级权限
        :return:
        """
        url = f'{self.ip}/pc/manage/teacher'
        data = {
            'classList': [],
            'gender': 1,
            'mobile': f"{self.teacher_mobile_num}0",
            'nickname': "接口添加老师",
            'position': "test"
        }
        res = requests.post(url=url, headers=self.manager_headers, json=data)
        assert_res(res.text)

    def test_04_change_teacher(self):
        """
        管理员修改老师：不修改班级权限
        :return:
        """
        url = f'{self.ip}/pc/manage/teacher'
        for m in [3, 0]:
            data = {
                'classList': [],
                "id": self.teacher_id_list[0],
                'gender': 2,
                'mobile': f"{self.teacher_mobile_num}{m}",
                'nickname': "接口修改老师",
                'position': "change_test"
            }
            res = requests.put(url=url, headers=self.manager_headers, json=data)
            assert_res(res.text)

    def test_05_get_teacher_list(self):
        """
        获取老师管理列表
        :return:
        """
        url = f'{self.ip}/pc/manage/teacherList'
        params = 'pageNum=1&pageSize=12&desc=0'
        response = requests.get(url=url, headers=self.manager_headers, params=params)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/pc/manage/teacherList报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            print([{i['id']: i['nickname']} for i in data_list])

    def test_06_get_user_class(self):
        """
        获取用户所拥有的类型区分的班级
        :return:
        """
        url = f'{self.ip}/pc/manage/userClass'
        params = f'userId={self.manager_id}'
        res = requests.get(url=url, headers=self.manager_headers, params=params)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['id']: i['name']} for i in data_ret['data']])
        except TypeError:
            print(f'接口/pc/manage/userClass报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def test_07_change_user_class(self):
        """
        修改用户班级权限
        :return:
        """
        url = f'{self.ip}/pc/manage/userClass'
        data = {
            "classList": [
                self.manager_param.get_manage_class_list()[0]
            ],
            "id": self.teacher_id_list[0]
        }
        res = requests.put(url=url, headers=self.manager_headers, json=data)
        assert_res(res.text)

    def test_08_delete_teacher(self):
        """
        管理员删除教师
        :return:
        """
        url = f'{self.ip}/pc/manage/teacher'
        params = f'userId={self.teacher_id_list[0]}'
        res = requests.delete(url=url, headers=self.manager_headers, params=params)
        assert_res(res.text)


if __name__ == '__main__':
    unittest.main()
