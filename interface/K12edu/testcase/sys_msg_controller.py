import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class SysMsgController(unittest.TestCase):
    """消息通用接口"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.msg_id_list = self.student_parm.get_msg_id_list()

    def test_01_get_my_msg_list(self):
        """
        获取用户的消息列表
        :return:
        """
        url = f'{self.ip}/pc/msg/getMyMsgList'
        for t in range(3):
            data = f'pageNum=1&pageSize=12&type={t}'
            response = requests.get(url=url, headers=self.teacher_headers,
                                    params=data)
            assert_res(response.text)
            data_ret = response.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                print(f'接口"/pc/msg/getMyMsgList"报错，返回{data_ret["msg"]}')
            else:
                print([{i['id']: i['title']} for i in data_list])

    def test_02_msg_detail(self):
        """
        获取用户的消息列表
        :return:
        """
        for msg_id in self.msg_id_list:
            url = f'{self.ip}/pc/msg/msgDetail/{msg_id}'
            response = requests.get(url=url, headers=self.student_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print({data_ret['data']['title']: data_ret['data']['readFlg']})
            except TypeError:
                print(f'接口"/pc/msg/msgDetail"报错，返回{data_ret["msg"]}')

    def test_03_msg_info(self):
        """
        当前用户是否有新消息
        :return:
        """
        url = f'{self.ip}/pc/msg/msgInfo'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)

    def test_04_read_msg(self):
        """
        将消息设置为已读
        :return:
        """
        url = f'{self.ip}/pc/msg/readMsg'
        data = {
            "msgIds": self.msg_id_list
        }
        response = requests.post(url=url, headers=self.student_headers,
                                 json=data)
        assert_res(response.text)

    def test_05_delete_msg(self):
        """
        删除消息信息
        :return:
        """
        url = f'{self.ip}/pc/msg/deleteMsg'
        data = {
            "msgIds": [
                self.msg_id_list[-1]
            ]
        }
        response = requests.post(url=url, headers=self.student_headers,
                                 json=data)
        assert_res(response.text)


if __name__ == '__main__':
    unittest.main()
