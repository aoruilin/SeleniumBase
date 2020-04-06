import unittest
import requests

from ui_auto.base.data import Data
from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestUser(unittest.TestCase):

    def setUp(self):
        self.teacher_params = ParameterForOthers(identity='teacher')
        self.ip = self.teacher_params.ip
        self.teacher_headers = self.teacher_params.headers

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

    def test_login_04(self,):
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

    def test_01_send_auth(self):
        """
        忘记密码-身份验证-发送验证码
        :return:
        """
        url = f'{self.ip}/user/forgetPassword/auth/send'
        for i in range(1, 3):
            username = '15208451946' if i == 1 else '646010544@qq.com'
            data = f'type={i}&username={username}'
            response = requests.get(url=url, headers=self.teacher_headers, params=data)
            assert_res(response.text)

    def test_02_modify_password(self):
        """
        账号设置-修改密码
        :return:
        """
        url = f'{self.ip}/user/username/modify/password'
        params = f"password={Data().teacher_data()['password']}&newPassword=1234567re&rePassword=1234567"
        response = requests.get(url=url, headers=self.teacher_headers, params=params)
        assert_res(response.text)

    def test_03_password_reset(self):
        """
        用户-重置密码
        :return:
        """
        user_id, _ = self.teacher_params.get_user_school_id()
        url = f'{self.ip}/user/password/reset/{user_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)

    def test_04_subject_feedback(self):
        url = f'{self.ip}/user/subject/feedback'
        data = {
            "feedbackDetail": "string",
            "feedbackType": 1,
            "subjectId": 251,
            "subjectType": 1
        }
        response = requests.post(url=url, json=data, headers=self.teacher_headers)
        assert_res(response.text,)

    def test_05_logout(self):
        """
        注销
        :return:
        """
        url = f'{self.ip}/user/logout'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)

    def test_06_user_info(self):
        """
        用户信息
        :return:
        """
        url = f'{self.ip}/user/userinfo'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)

    def test_07_switch_school(self):
        """
        切换学校
        :return:
        """
        school_id_list = self.teacher_params.get_school_id_list()
        for i in [1, 0]:
            url = f'{self.ip}/user/switch/school/{school_id_list[i]}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)

    def test_08_user_modify(self):
        """
        用户信息验证
        :return:
        """
        portrait_url, gender = self.teacher_params.get_user_portrait_url_gender()
        data = f'nickname={Data().teacher_data()["name"]}&gender={gender}&portraitUrl={portrait_url}'
        url = f'{self.ip}/user/modify?{data}'
        response = requests.post(url=url, headers=self.teacher_headers)
        assert_res(response.text)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
