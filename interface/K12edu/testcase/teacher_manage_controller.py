import os
import time
import unittest
from pprint import pprint

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.files_operation import file_write
from ui_auto.common.get_cwd import get_absolute_path


class TeacherManageController(unittest.TestCase):

    def setUp(self) -> None:
        self.manager_param = ParameterForOthers(identity='manager')
        self.teacher_param = ParameterForOthers(identity='teacher')
        self.student_param = ParameterForOthers(identity='student')
        self.ip = self.manager_param.ip
        self.manager_headers = self.manager_param.headers

        self.teacher_id_list = self.manager_param.get_manage_teacher_list()
        self.manager_id, self.school_id = self.manager_param.get_user_school_id()
        self.class_id = self.manager_param.get_class_list(get_all=True)
        self.teacher_mobile_num = '1520840000'
        self.file_path = f'{get_absolute_path("interface")}\\K12edu\\files\\'

    def test_01_add_teacher(self):
        """
        管理员添加老师
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/add'
        data = {
            "classIds": self.class_id[:1],
            "gender": 1,
            "mobile": f"{self.teacher_mobile_num}0",
            "position": "test",
            "schoolId": self.school_id,
            "tchName": "接口添加老师"
        }
        res = requests.post(url=url, headers=self.manager_headers, json=data)
        assert_res(res.text)

    def test_02_change_teacher(self):
        """
        管理员修改老师
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/edit'
        for m in [3, 0]:
            data = {
                "classIds": self.class_id[:2],
                "gender": 2,
                "mobile": f"{self.teacher_mobile_num}{m}",
                "position": "change_test",
                "schoolId": self.school_id,
                "tchId": self.teacher_id_list[0],
                "tchName": "接口修改老师"
            }
            res = requests.post(url=url, headers=self.manager_headers, json=data)
            assert_res(res.text)

    def test_03_get_teacher_list(self):
        """
        获取老师管理列表
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/list'
        for t in range(1, 4):
            for k in ['', '接口']:
                data = {
                    "currPage": 1,
                    "keyword": k,
                    "pageSize": 40,
                    "schoolId": self.school_id,
                    "tchType": t
                }
                res = requests.post(url=url, headers=self.manager_headers, json=data)
                assert_res(res.text)
                time.sleep(1)
                data_ret = res.json()
                try:
                    data_list = data_ret['data']['list']
                except TypeError:
                    print(f'接口/teachcenter/teachermanage/list报错，返回{data_ret["msg"]}')
                except KeyError:
                    print(f'接口/teachcenter/teachermanage/list返回{data_ret}')
                else:
                    pprint([{i['tchId']: i['tchName']} for i in data_list])

    def test_04_delete_teacher(self):
        """
        管理员删除教师
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/remove'
        data = {
            "schoolId": self.school_id,
            "tchIds": self.teacher_id_list[:1]
        }
        res = requests.post(url=url, headers=self.manager_headers, json=data)
        assert_res(res.text)

    def test_05_teacher_select_list(self):
        """
        教师管理-查询下拉-列表
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/selectList'
        params = f'schoolId={self.school_id}'
        res = requests.get(url=url, headers=self.manager_headers, params=params)
        assert_res(res.text)

    def test_06_export(self):
        """
        教师管理-批量导出
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/export'
        params = f'exportType=1&tchType=1&schoolId={self.school_id}'
        res = requests.get(url=url, headers=self.manager_headers, params=params)
        file_name = 'teacher_export.xls'
        file_write(f'{self.file_path}export\\', file_name, res.content)

    def test_07_export_temp(self):
        """
        教师管理-模板导出
        :return:
        """
        url = f'{self.ip}/teachcenter/teachermanage/exportTemp'
        res = requests.get(url=url, headers=self.manager_headers)
        file_name = 'teacher_temp.xls'
        file_write(f'{self.file_path}export\\', file_name, res.content)

    def test_08_file_import(self):
        """
        教师管理-批量导入
        :return:
        """
        from requests_toolbelt.multipart.encoder import MultipartEncoder

        url = f'{self.ip}/teachcenter/teachermanage/fileImport'
        file_name = 'teacher.xls'
        with open(f'{self.file_path}upload\\{file_name}', 'rb') as f:
            m = MultipartEncoder(
                {
                    'file': (file_name, f, 'application/vnd.ms-excel')
                }
            )
            self.manager_headers['Content-Type'] = m.content_type
            params = f'schoolId={self.school_id}'
            res = requests.post(url=url, headers=self.manager_headers, data=m, params=params)
            assert_res(res.text, '批量导入用户失败')
            data_ret = res.json()
            try:
                print(data_ret['data']['errMsg'])
            except TypeError:
                print(f'接口/teachcenter/teachermanage/fileImport报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口/teachcenter/teachermanage/fileImport返回{data_ret}')


if __name__ == '__main__':
    unittest.main()
