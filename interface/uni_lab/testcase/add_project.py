import requests
import unittest
import datetime
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
        DATA = {
            "password": password,
            "username": username
        }
        t = requests.session()
        login_ret = t.post(url=self.login_url, headers=self.headers, json=DATA)
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
        data = {"langType": 2, "difficulty": 1,"timingIssued": 'false',"timingTime": ''}
        data['name'] = '测试发布接口'
        data['classIds'] = class_ids
        data['projectId'] = project_id
        now_time = datetime.datetime.now()
        time_diff = datetime.timedelta(minutes=10)
        e_time = now_time + time_diff * 3
        end_time = int(e_time.timestamp() * 1000)
        data['endTime'] = end_time
        data['showStandardAnswer'] = 1
        response = requests.post(url=self.url, headers=self.headers, json=data)
        print(type(data), response.text)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
