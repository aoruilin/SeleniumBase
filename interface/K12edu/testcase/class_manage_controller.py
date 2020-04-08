import unittest
import requests
import time
from pprint import pprint

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class ClassManage(unittest.TestCase):

    def setUp(self) -> None:
        self.manager_param = ParameterForOthers(identity='manager')
        self.teacher_param = ParameterForOthers(identity='teacher')
        self.student_param = ParameterForOthers(identity='student')
        self.ip = self.teacher_param.ip
        self.manager_id, self.school_id = self.manager_param.get_user_school_id()
        self.class_id_list = self.manager_param.get_manage_class_list(self.school_id)
        self.student_id_list = self.manager_param.get_class_student_id(self.class_id_list[1], self.school_id)

    def test_01_add_course(self):
        """
        管理员创建班级
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/create'
        data = {
            'className': '接口添加班级，待删除',
            'schoolId': self.school_id,
            'teachersId': [self.manager_id]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            success = data_ret['data']['success']
            if success:
                print('创建成功')
                self.class_id_list = self.manager_param.get_manage_class_list(self.school_id)
            if not success:
                print(f'创建失败,{data_ret["data"]["msg"]}')
        except KeyError:
            print(f"添加班级失败,{data_ret}")

    def test_02_add_form_student(self):
        """
        表单填写信息新建学生
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuAdd'
        data = {
            "classId": self.class_id_list[0],
            "gender": 1,
            "mobile": "",
            "schoolId": self.school_id,
            "stuName": "接口学生待删",
            "stuNo": "E00003"
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_03_add_course_student(self):
        """
        选取添加学生
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuBatchAdd'
        for i in range(2):
            data = {
                'classId': self.class_id_list[0],
                'stuIds': [str(self.student_id_list[i])]
            }
            res = requests.post(url=url, headers=self.manager_param.headers, json=data)
            assert_res(res.text)
            time.sleep(1)
        self.student_id_list = self.manager_param.get_class_student_id(self.class_id_list[0], self.school_id)

    def test_04_upd_student(self):
        """
        班级管理修改学生
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuEdit'
        for m in ['', '15208451946']:
            data = {
                "gender": 2,
                "mobile": m,
                "stuId": self.student_id_list[0],
                "stuName": "接口修改学生"
            }
            res = requests.post(url=url, headers=self.manager_param.headers, json=data)
            assert_res(res.text)
            data_ret = res.json()
            try:
                success = data_ret['data']['success']
                if success:
                    print('修改成功')
                if not success:
                    assert '电话[15208451946]号码已被注册' == data_ret["data"]["msg"]
            except KeyError:
                print(f"添加班级失败,{data_ret}")

    def test_05_student_list(self):
        """
        班级管理-学生列表
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuList'
        for k in ['', '接口']:
            data = {
                "classId": self.class_id_list[0],
                "currPage": 1,
                "keyword": k,
                "pageSize": 30,
                "schoolId": self.school_id
            }
            res = requests.post(url=url, headers=self.manager_param.headers, json=data)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                print(f'接口/teachcenter/classmanage/stuList报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口/teachcenter/classmanage/stuList返回{data_ret}')
            else:
                print([(i['stuNo'], i['stuName'], i['mobile']) for i in data_list])

    def test_06_student_info(self):
        """
        班级管理-学生列表-学生信息查询
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuInfo/{self.student_id_list[0]}'
        res = requests.get(url=url, headers=self.manager_param.headers)
        assert_res(res.text)
        pprint(res.json())

    def test_07_del_students(self):
        """
        删除班级学生
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuRemove'
        data = {
            'classId': self.class_id_list[0],
            'stuId': [self.student_id_list[0]]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_08_upd_course(self):
        """
        修改课程班
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/edit'
        teacher_id, _ = self.teacher_param.get_user_school_id()
        data = {
            "classId": self.class_id_list[0],
            "className": "接口修改班级",
            "schoolId": self.school_id,
            "teachersId": [
                self.manager_id, teacher_id
            ]
        }
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_09_class_list(self):
        """
        班级管理-列表
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/list'
        for t in range(1, 3):
            for k in ['', '接口']:
                data = {
                    "classType": t,
                    "currPage": 1,
                    "keyword": k,
                    "pageSize": 30,
                    "schoolId": self.school_id
                }
                res = requests.post(url=url, headers=self.manager_param.headers, json=data)
                assert_res(res.text)
                time.sleep(1)
                data_ret = res.json()
                try:
                    data_list = data_ret['data']['list']
                except TypeError:
                    print(f'接口/teachcenter/classmanage/stuList报错，返回{data_ret["msg"]}')
                except KeyError:
                    print(f'接口/teachcenter/classmanage/stuList返回{data_ret}')
                else:
                    pprint([(i['classId'], i['className'], i['stuCount']) for i in data_list])

    def test_10_del_course(self):
        """
        删除对应班级
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/remove'
        data = {'classId': [self.class_id_list[0]]}
        res = requests.post(url=url, headers=self.manager_param.headers, json=data)
        assert_res(res.text)
        time.sleep(1)

    def test_11_get_class_list(self):
        """
        班级管理-列表
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/list/{self.school_id}'
        res = requests.get(url=url, headers=self.manager_param.headers)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{i['id']: i['name']} for i in data_ret['data']])
        except TypeError:
            print(f'接口/teachcenter/classmanage/list报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/teachcenter/classmanage/list返回{data_ret}')

    def test_12_select_list(self):
        """
        班级管理-查询下拉-列表
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/selectList'
        params = f'schoolId={self.school_id}'
        res = requests.get(url=url, headers=self.manager_param.headers, params=params)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([i.values() for i in data_ret['data']])
        except TypeError:
            print(f'接口/teachcenter/classmanage/selectList报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/teachcenter/classmanage/selectList返回{data_ret}')

    def test_13_student_class_list(self):
        """
        班级管理-添加学生-学生列表
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuClassList/{self.school_id}/{self.class_id_list[0]}'
        res = requests.get(url=url, headers=self.manager_param.headers)
        assert_res(res.text)
        data_ret = res.json()
        try:
            pprint([{i['name']: [{s['id']: s['name']} for s in i['students']]} for i in data_ret['data']])
        except TypeError:
            print(f'接口/teachcenter/classmanage/stuClassList报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/teachcenter/classmanage/stuClassList返回{data_ret}')


if __name__ == "__main__":
    unittest.main()
