import unittest
import requests
import time

from interface.common.time_parameter import time_stamp
from interface.uni_teach.common.parameter_for_others import ParameterForOthers


class AddProjectLoop(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers('teacher')
        ip = self.parameter.ip
        self.url = f'{ip}/pc/new/experProject/master/issue'
        self.headers = self.parameter.headers

    def test_01(self):
        class_id = self.parameter.get_class_list()
        end_time = time_stamp(end=True)
        start_time = time_stamp(start=True)
        s_list = ['', start_time]
        data = {
            'langType': 2,
        }
        for i in range(1, 6):
            for d in range(1, 4):
                for a in range(0, 3):
                    for s in s_list:
                        name = f'项目{i}难度{d}答案{a}定时{s}'
                        data['classIds'] = class_id
                        data['difficulty'] = d
                        data['endTime'] = end_time
                        data['name'] = name
                        data['projectId'] = i
                        data['showStandardAnswer'] = a
                        data['timingTime'] = s
                        if s == '':
                            data['timingIssued'] = 'false'
                        else:
                            data['timingIssued'] = 'true'
                        response = requests.post(url=self.url, headers=self.headers, json=data)
                        try:
                            self.assertIn('操作成功', response.text)
                            print(f'{name}项目添加成功')
                        except AssertionError as n:
                            print(f'{n}, {name}项目添加失败')
                        except Exception as e:
                            print(f'{response.text}，请求失败{e}')
                        time.sleep(3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
