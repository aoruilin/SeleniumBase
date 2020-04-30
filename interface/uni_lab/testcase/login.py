import unittest
import requests
from base.data import Ips
from base.data import UnPw

class TestLogin(unittest.TestCase):
    '''登录接口'''
    def setUp(self):
        ip = Ips.ip_for_uni_lab
        self.url = ip + '/pc/login'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def test_01(self):
        '''登录接口'''
        username = UnPw.username_for_uniLab
        password = UnPw.password_for_uniLab
        data = {
            "password": password,
            "username": username
        }
        response = requests.post(url=self.url, json=data, headers=self.headers)
        self.assertIn('操作成功', response.text)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()