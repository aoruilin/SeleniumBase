import unittest
import requests

from interface.uni_teach.common.parameter_for_others import ParameterForOthers


class TestGetClassList(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers('student')
        ip = self.parameter.ip
        self.url = f'{ip}/pc/common/getClassList'
        self.headers = self.parameter.headers

    def test_01(self):
        response = requests.get(url=self.url, params=self.headers)
        # print(response.text)
        self.assertIn('操作成功', response.text)
        class_list_ret = response.json()
        data_dic = class_list_ret['data']
        data = data_dic[0]
        class_id = data['id']
        print(class_id)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
