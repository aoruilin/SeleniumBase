import requests
import unittest

from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestFastRequests(unittest.TestCase):

    def setUp(self) -> None:
        self.parameter = ParameterForOthers(identity='student')
        self.ip = self.parameter.ip
        self.headers = self.parameter.headers

    def test_01(self) -> None:
        url = f'{self.ip}/pc/userInfo'
        for i in range(0, 21):
            res = requests.get(url=url, headers=self.headers)
            response = res.json()
            msg = response['msg']
            print(msg)
