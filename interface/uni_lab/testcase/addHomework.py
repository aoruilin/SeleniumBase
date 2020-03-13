import datetime
import unittest
import requests
from time import time
from base.data import Ips
from base.data import UnPw


class AddHomework(unittest.TestCase):
    '''添加作业'''

    def setUp(self):
        self.ip = Ips.ip_for_uniLab
        self.login_url = self.ip + '/pc/login'
        self.class_id_url = self.ip + '/pc/clbum/self/list'
        self.point_id_url = self.ip + '/pc/common/getPointList?language=2'
        self.url = self.ip + '/pc/exper/master/traditional_teach'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }

    def test_01(self):
        '''添加作业'''
        username = UnPw.username_for_uniLab
        password = UnPw.password_for_uniLab
        login_data = {
            "password": password,
            "username": username
        }
        t = requests.session()
        login_ret = t.post(url=self.login_url, headers=self.headers, json=login_data)
        token = login_ret.json()['data']['token']

        self.headers['token'] = token
        class_id_response = requests.get(url=self.class_id_url, headers=self.headers)
        class_list_ret = class_id_response.json()
        data_dic = class_list_ret['data']
        data_d = data_dic[0]
        class_id_list = []
        class_id = data_d['clbumId']
        class_id_list.append(class_id)
        class_ids = class_id_list

        point_id_response = requests.get(url=self.point_id_url, headers=self.headers)
        point_list_ret = point_id_response.json()
        data_list = point_list_ret['data']
        problem_dic = data_list[3]  # 知识点二级列表
        problem_list = problem_dic['list']
        id_list = []
        for i in problem_list:
            point_id = i['id']
            id_list.append(point_id)
        point_id_for_homework = id_list[0]

        problem_id_url = self.ip + '/pc/problem?klPoints=%s&pageNum=1&pageSize=12&difficulty=1' % point_id_for_homework
        problem_id_response = requests.get(url=problem_id_url, headers=self.headers)
        data_ret = problem_id_response.json()
        data = data_ret['data']
        problem_list = data['list']
        problem_id_list = []
        for d in problem_list:
            problem_id = d['id']
            problem_id_list.append(problem_id)

        data = {
            "name": "测试发布基础实验接口",
            "showRunResult": 1,
            "showStandardAnswer": 1,
            "startTime": "0",
            "timingIssued": 'false',
            "timingTime": 0,
            "type": 0
        }

        time_diff = datetime.timedelta(minutes=10)
        now_time = datetime.datetime.now()
        e_time = now_time + time_diff
        end_time = int(e_time.timestamp() * 1000)

        data['classIds'] = class_ids
        data['endTime'] = end_time
        point_id = point_id_for_homework
        problem_id = problem_id_list
        items = []
        homework = {
            'pointId': point_id,
            'problemId': problem_id[0],
            'problemLanguageType': 2
        }
        items.append(homework)
        data['items'] = items
        response = requests.post(url=self.url, headers=self.headers, json=data)
        self.assertIn('操作成功', response.text)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
