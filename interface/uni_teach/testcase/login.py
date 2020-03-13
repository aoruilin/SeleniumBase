import unittest
import requests

from base.data import Data


class TestLogin(unittest.TestCase):

    def setUp(self):
        ip = Data().api_ip_for_uni_teach()
        self.username = Data().student_username_for_uni_teach()
        self.password = Data().password_for_uniTeach
        self.url = f'{ip}/pc/login'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def test_01(self):
        data = {
            "password": self.password,
            "username": self.password
        }
        response = requests.post(url=self.url, json=data, headers=self.headers)
        self.assertIn('操作成功', response.text)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
