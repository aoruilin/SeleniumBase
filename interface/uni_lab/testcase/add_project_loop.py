import requests
import unittest
import datetime
from interface.uni_lab.common.login_for_others import login_interface
from interface.uni_lab.common.classId_for_others import getClassList
from interface.uni_lab.common.project_id_for_others import get_project_id
from base.data import Ips
from base.data import UnPw


class AddProject(unittest.TestCase):
    '''发布项目实验'''

    def setUp(self):
        ip = Ips.ip_for_uniLab
        self.login_url = ip + '/pc/login'
        self.class_id_url = ip + '/pc/clbum/self/list'
        self.project_id_url = ip + '/pc/project'
        self.url = ip + '/pc/experProject/master/project'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }

    def test_01(self, enableassert=True):
        '''发布项目实验'''
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
        project_id_response = requests.get(url=self.project_id_url, headers=self.headers)
        res_data = project_id_response.json()
        data_list = res_data['data']
        data_dic = data_list[0]
        project_id = data_dic['projectId']

        now_time = datetime.datetime.now()
        time_diff = datetime.timedelta(minutes=10)
        s_time = now_time + time_diff
        e_time = now_time + time_diff * 3
        start_time = int(s_time.timestamp() * 1000)
        end_time = int(e_time.timestamp() * 1000)
        timing_issued_list = ['True', 'False']

        for d in range(0, 4):
            for a in range(0, 3):
                for t in timing_issued_list:
                    name = '难度' + str(d) + '答案' + str(a) + '定时' + t
                    data = {"langType": 2}
                    data['name'] = name
                    data['classIds'] = class_ids
                    data['projectId'] = project_id
                    data['endTime'] = end_time
                    data['difficulty'] = d
                    data['showStandardAnswer'] = a
                    data['timingIssued'] = t
                    if 'True' == t:
                        data['timingTime'] = start_time
                    else:
                        data['timingTime'] = ''
                    response = requests.post(url=self.url, headers=self.headers, json=data)
                    if enableassert:
                        self.assertIn('操作成功', response.text)
                        print('项目实验%s成功发布' % name)
                    else:
                        print('项目实验%s发布失败' % name)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
