import time
import unittest
import requests
import datetime

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestTotal(unittest.TestCase):

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.student_class_id = self.student_parm.get_class_list(1, get_all=True)
        self.teacher_class_id = self.student_parm.get_class_list(1, get_all=True)

    def test_get_homework_complete_total(self):
        """
        获取首页个人发布的作业完成率统计数据
        :return:
        """
        complete_num_list = []
        for t in range(5):
            url = f'{self.ip}/pc/total/getHomeworkCompleteTotal?classId={self.teacher_class_id[-1]}&timeType={t}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                complete_num = data_ret['data']['complete']
            except TypeError:
                print(f'接口"/pc/total/getHomeworkCompleteTotal"报错，返回{data_ret["msg"]}')
            else:
                complete_num_list.append(complete_num)
                print(complete_num_list)

    def test_get_homework_total(self):
        """
        获取首页个人发布的作业最近操作统计数据
        :return:
        """
        for t in range(5):
            url = f'{self.ip}/pc/total/getHomeworkTotal?classId={self.teacher_class_id[0]}&timeType={t}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            data_ret = response.json()
            try:
                data_list = data_ret['data']
                print({data['name']: data['ratio'] for data in data_list})
            except TypeError:
                print(f'接口"/pc/total/getHomeworkTotal"报错，返回{data_ret["msg"]}')

    def test_get_event_info_total(self):
        """
        获取首页个人数据被人操作统计数据
        :return:
        """
        n_time = datetime.datetime.now()
        now_time = int(n_time.timestamp() * 1000)
        time_diff = datetime.timedelta(weeks=10)
        start_time = int((n_time - time_diff).timestamp() * 1000)
        url = f'{self.ip}/pc/total/getEventInfoTotal?' \
              f'classId={self.teacher_class_id[0]}' \
              f'&startTime={start_time}' \
              f'&endTime={now_time}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            events = data_ret['data']['events']
        except TypeError:
            print(f'接口"/pc/total/getEventInfoTotal"报错，返回{data_ret["msg"]}')
        else:
            print({event['title']: event['nickName'] for event in events})

    def test_get_index_info_total(self):
        """
        获取首页个人统计数据
        :return:
        """
        url = f'{self.ip}/pc/total/getIndexInfoTotal?classId={self.teacher_class_id[0]}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        info = data_ret['data']
        print(info)


if __name__ == '__main__':
    unittest.main()
