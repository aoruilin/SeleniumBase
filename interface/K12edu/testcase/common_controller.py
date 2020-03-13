import time
import unittest

import requests
from itertools import chain

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class CommonController(unittest.TestCase):
    """公共数据"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.class_list = self.teacher_parm.get_class_list()
        self.teacher_id, self.school_id = self.teacher_parm.get_user_school_id()
        self.student_id, _ = self.student_parm.get_user_school_id()

    def test_01_class(self):
        """
        班级列表
        :return:
        """
        url = f'{self.ip}/common/class/{self.class_list[0]}'
        res = requests.get(url=url, headers=self.teacher_headers)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print({data_ret['data']['name']: data_ret['data']['teachNames']})
        except TypeError:
            print(f'接口/common/class报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/common/class，返回{data_ret},与预期不符')

    def test_02_classes(self):
        """
        班级列表
        :return:
        """
        url = f'{self.ip}/common/classes'
        for i in ['teacher', 'student']:
            user_id = self.teacher_id if i == 'teacher' else self.student_id
            headers = self.teacher_headers if i == 'teacher' else self.student_headers
            data = f'userId={user_id}&schoolId={self.school_id}'
            res = requests.get(url=url, headers=headers, params=data)
            assert_res(res.text)
            data_ret = res.json()
            try:
                data_list = data_ret['data']
                for data in data_list:
                    print({data['name']: data['teachNames']})
            except TypeError:
                print(f'接口/common/classes，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口/common/classes，返回{data_ret},与预期不符')

    def test_03_points(self):
        """
        知识点树
        :return:
        """
        series_id_list = self.teacher_parm.get_series_list()
        if series_id_list:
            for s in series_id_list:
                url = f'{self.ip}/common/points/{s}'
                res = requests.get(url=url, headers=self.teacher_headers)
                assert_res(res.text)
                data_ret = res.json()
                series_point_id_list = []
                try:
                    data_list = data_ret['data']
                    for d in data_list:
                        child_id_list = [c['id'] for c in d['children']]
                        series_point_id_list.append(child_id_list)
                    print(list(chain(*series_point_id_list)))
                except TypeError:
                    print(f'接口/common/points，返回{data_ret["msg"]}')
                except KeyError:
                    print(f'接口/common/points，返回{data_ret},与预期不符')

    def test_04_roles(self):
        """
        角色列表
        :return:
        """
        url = f'{self.ip}/common/roles'
        manager_id, _ = self.manager_parm.get_user_school_id()
        school_id_list = self.manager_parm.get_school_id_list()
        for s in school_id_list:
            data = f'userId={manager_id}&schoolId={s}'
            res = requests.get(url=url, headers=self.manager_headers, params=data)
            assert_res(res.text)
            data_ret = res.json()
            try:
                print(data_ret['data'])
            except TypeError:
                print(f'接口/common/roles，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口/common/roles，返回{data_ret},与预期不符')

    def test_05_schools(self):
        """
        学校列表
        :return:
        """
        url = f'{self.ip}/common/schools'
        data = f'userId={self.student_id}'
        res = requests.get(url=url, headers=self.student_headers, params=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print(data_ret['data'])
        except TypeError:
            print(f'接口/common/schools，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/common/schools，返回{data_ret},与预期不符')

    def test_06_series(self):
        """
        系列课程
        :return:
        """
        url = f'{self.ip}/common/series'
        data = {
            "schoolId": self.school_id,
            "seriesType": 0,
            "types": [
                1
            ]
        }
        res = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            print([{d['id']: d['name']} for d in data_ret['data']])
        except TypeError:
            print(f'接口/common/series，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/common/series，返回{data_ret},与预期不符')


if __name__ == '__main__':
    unittest.main()
