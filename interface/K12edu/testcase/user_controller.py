import unittest
import requests

from base.data import Data
from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestUser(unittest.TestCase):

    def setUp(self):
        self.parameters = ParameterForOthers(identity='teacher')
        self.ip = self.parameters.ip
        self.headers = self.parameters.headers

    def test_login_01(self):
        """
        登录接口
        :return:
        """
        headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }
        url = f'{self.ip}/user/login'
        username = Data().teacher_data()['username']
        password = Data().teacher_data()['password']
        data = {
            "password": password,
            "username": username
        }
        response = requests.post(url=url, json=data, headers=headers)
        assert_res(response.text)

    def test_login_02(self):
        headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }
        url = f'{self.ip}/user/login'
        username = Data().teacher_data()['username']
        data = {
            "password": '1234567',
            "username": username
        }
        response = requests.post(url=url, json=data, headers=headers)
        assert_res(response.text, '用户名/密码错误')

    def test_login_03(self):
        headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }
        url = f'{self.ip}/user/login'
        data = {
            "password": '123456',
            "username": 'wrong'
        }
        response = requests.post(url=url, json=data, headers=headers)
        assert_res(response.text, '账号不存在')

    def test_login_04(self):
        headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }
        url = f'{self.ip}/user/login'
        data = {
            "password": '123456',
            "username": None
        }
        response = requests.post(url=url, json=data, headers=headers)
        assert_res(response.text, '参数校验失败')

    def test_login_05(self):
        headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }
        username = Data().teacher_data()['username']
        url = f'{self.ip}/user/login'
        data = {
            "password": None,
            "username": username
        }
        response = requests.post(url=url, json=data, headers=headers)
        assert_res(response.text, '参数校验失败')

    def test_send_auth(self):
        """
        忘记密码-身份验证-发送验证码
        :return:
        """
        url = f'{self.ip}/user/forgetPassword/auth/send'
        for i in range(1, 3):
            username = '15208451946' if i == 1 else '646010544@qq.com'
            data = f'type={i}&username={username}'
            response = requests.get(url=url, headers=self.headers, params=data)
            assert_res(response.text)

    def test_auth_mobile_code(self):   # 没改
        """
        获取更换绑定手机验证码
        :return:
        """
        url = f'{self.ip}/pc/authMobileCode?mobile=15208451946'
        response = requests.get(url=url, headers=self.headers)
        assert_res(response.text, '认证未通过')

    def test_update_password_01(self):   # 没改
        """
        根据旧密码修改新密码
        :return:
        """
        url = f'{self.ip}/pc/updatePwdByOldPwd'
        data = {
            'newPassword': '123456',
            'password': '123456'
        }
        response = requests.post(url=url, json=data, headers=self.headers)
        assert_res(response.text)

    def test_update_password_02(self):   # 没改
        url = f'{self.ip}/pc/updatePwdByOldPwd'
        data = {
            'newPassword': '123456',
            'password': '12345'
        }
        response = requests.post(url=url, json=data, headers=self.headers)
        assert_res(response.text, '旧密码有误')

    def test_update_password_03(self):   # 没改
        url = f'{self.ip}/pc/updatePwdByOldPwd'
        data = {
            'newPassword': '123456',
            'password': None
        }
        response = requests.post(url=url, json=data, headers=self.headers)
        assert_res(response.text, '参数校验失败')

    def test_logout(self):
        """
        注销
        :return:
        """
        url = f'{self.ip}/user/logout'
        response = requests.get(url=url, headers=self.headers)
        assert_res(response.text)

    def test_user_info(self):
        """
        用户信息
        :return:
        """
        url = f'{self.ip}/user/userinfo'
        response = requests.get(url=url, headers=self.headers)
        assert_res(response.text)

    def test_switch_school(self):
        """
        切换学校
        :return:
        """
        school_id_list = self.parameters.get_school_id_list()
        for i in [1, 0]:
            url = f'{self.ip}/user/switch/school/{school_id_list[i]}'
            response = requests.get(url=url, headers=self.headers)
            assert_res(response.text)

    def test_user_modify(self):
        """
        用户信息验证
        :return:
        """
        portrait_url, gender = self.parameters.get_user_portrait_url_gender()
        data = f'nickname={Data().teacher_data()["name"]}&gender={gender}&portraitUrl={portrait_url}'
        url = f'{self.ip}/user/modify?{data}'
        response = requests.post(url=url, headers=self.headers)
        assert_res(response.text)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
