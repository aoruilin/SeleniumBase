import unittest
import requests
import datetime
from base.data import Ips
from base.data import UnPw
from interface.uni_lab.common.login_for_others import login_interface
from interface.uni_lab.common.classId_for_others import getClassList
from interface.uni_lab.common.pointId_for_others import get_point_id
from interface.uni_lab.common.problemId_for_others import get_problem_id


class AddHomework_loop(unittest.TestCase):
    '''覆盖所有发布设置添加作业'''

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

    def test_addHomework(self, enableassert=True):
        '''覆盖所有发布设置添加作业'''
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
        data_d = data_dic[1]
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
        item_list = []
        for problem_id in problem_id_list:
            item_list.append({'pointId': point_id_for_homework, 'problemId': str(problem_id), 'problemLanguageType': 0})

        time_diff = datetime.timedelta(minutes=10)
        now_time = datetime.datetime.now()
        s_time = now_time + time_diff
        e_time = now_time + time_diff * 3
        end_time = int(e_time.timestamp() * 1000)
        start_time = int(s_time.timestamp() * 1000)

        timing_issued_list = ['True', 'False']
        for r in range(0, 2):
            for a in range(0, 3):
                for s in timing_issued_list:
                    data = {"type": 0, 'problemLanguageType': 2}
                    name = '结果' + str(r) + '答案' + str(a) + '定时' + str(s)
                    data['items'] = item_list
                    data['classIds'] = class_ids
                    data['endTime'] = end_time
                    data['name'] = name
                    data['showRunResult'] = r
                    data['showStandardAnswer'] = a
                    data['timingIssued'] = s
                    if 'True' == s:
                        data['timingTime'] = start_time
                    else:
                        data['timingTime'] = ''
                    response = requests.post(url=self.url, headers=self.headers, json=data)
                    if enableassert:
                        self.assertIn('操作成功', response.text)
                        print('%s作业添加成功' % name)
                    else:
                        print('%s作业添加失败' % name)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
