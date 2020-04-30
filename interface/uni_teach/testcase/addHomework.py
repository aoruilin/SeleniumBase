import unittest
import requests
from time import time

from interface.uni_teach.common.parameter_for_others import ParameterForOthers


class AddHomework(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers('teacher')
        ip = self.parameter.ip
        self.url = f'{ip}/pc/traditional_teach'
        self.headers = self.parameter.headers

    def test_01(self):
        data = {
            "items": [
                {'pointId': "e58184a61563424abb532195e0b0b9df", 'problemId': 8858}],
            "name": "测试发布作业接口",
            # "showRunResult": 1,
            "showStandardAnswer": 1,
            "startTime": "0"
        }
        class_id = self.parameter.get_class_list()
        data['classIds'] = class_id
        end_time = str(time() * 10000)[:14]
        data['endTime'] = end_time
        # items = []
        # traditional_teach = {'pointId': "e58184a61563424abb532195e0b0b9df", 'problemId': 8853}
        # items.append(traditional_teach)
        # print(items)
        # data['items'] = items
        response = requests.post(url=self.url, headers=self.headers, json=data)
        self.assertIn('操作成功', response.text)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
