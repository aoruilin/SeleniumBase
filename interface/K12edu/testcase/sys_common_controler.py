import time
import unittest

import requests
from dateutil.parser import parse

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class SysCommonController(unittest.TestCase):
    """系统通用接口"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

    def test_01_get_class_id(self):
        """
        获取classlist接口
        :return:
        """
        id_dic = {}
        series_list = self.teacher_parm.get_series_list()
        for s in series_list:
            url = f'{self.ip}/pc/common/getClassList?seriesId={s}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text, '操作成功')
            class_list_ret = response.json()
            try:
                data_list = class_list_ret['data']
            except TypeError:
                print(f'接口"/pc/common/getClassList"报错，返回{class_list_ret["msg"]}')
            else:
                id_list = [i['id'] for i in data_list]
                id_dic[s] = id_list
        print(id_dic)

    def test_02_get_now_time(self):
        """
        获取服务器当前时间
        :return:
        """
        url = f'{self.ip}/pc/common/getNowTime'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        server_time = None
        try:
            data = data_ret['data']
        except TypeError:
            print(f'接口"/pc/common/getNowTime"报错，返回{data_ret["msg"]}')
        else:
            server_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data / 1000)))
            print(f'服务器时间：{server_time}')
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(f'北京时间：{now_time}')
        if server_time > now_time:
            diff = (parse(server_time) - parse(now_time))
            print(f'服务器时间比北京时间快了：{diff.seconds}秒')
        elif server_time < now_time:
            diff = (parse(now_time) - parse(server_time))
            print(f'服务器时间比北京时间慢了：{diff.seconds}秒')
        else:
            print('服务器时间和北京时间一致')

    def test_03_get_school_point_id(self):
        """
        获取本校能查看的系列及知识点(树型结构)
        :return:
        """
        url = f'{self.ip}/pc/common/getSchoolPointList'
        response = requests.get(url=url, headers=self.manager_headers)
        assert_res(response.text, '操作成功')

    def test_04_switch_identity(self):
        """
        获取用户可切换的学校权限列表
        :return:
        """
        url = f'{self.ip}/pc/common/switchIdentity'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text, '操作成功')


if __name__ == '__main__':
    unittest.main()
