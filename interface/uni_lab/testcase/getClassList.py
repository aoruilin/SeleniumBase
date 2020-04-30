import unittest
import requests
from base.data import Ips
from interface.uni_lab.common.login_for_others import login_interface

class TestGetClassList(unittest.TestCase):
    '''获取classlist接口'''
    def setUp(self):
        ip = Ips.ip_for_uniLab
        self.url = ip + '/pc/clbum/self/list'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def test_01(self):
        '''获取classlist接口'''
        token = login_interface()
        self.headers['token'] = token
        response = requests.get(url=self.url, headers=self.headers)
        # print(response.text)
        self.assertIn('操作成功', response.text)
        class_list_ret = response.json()
        data_dic = class_list_ret['data']
        data = data_dic[0]
        class_id = data['clbumId']
        print(class_id)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()