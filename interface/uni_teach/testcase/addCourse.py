import unittest
import requests
import time

from interface.uni_teach.common.parameter_for_others import ParameterForOthers


class TestAddCourse(unittest.TestCase):

    def setUp(self):
        self.parameter = ParameterForOthers('teacher')
        ip = self.parameter.ip
        self.url = f'{ip}/pc/course/addCoursePlan'
        self.headers = self.parameter.headers

    def test_01(self):
        point_id = self.parameter.get_point_id()
        resource_plan_id = self.parameter.get_resource_plan_id()
        for r in resource_plan_id:
            for s in range(1, 3):
                data = {"language": 1}
                class_id = self.parameter.get_class_list()
                data['classIds'] = class_id
                data['pointId'] = point_id[1]
                data['resourcePlanId'] = r
                data['status'] = s

                try:
                    response = requests.post(url=self.url, headers=self.headers, json=data)
                    self.assertIn('操作成功', response.text)
                except:
                    n = 1
                    while True:
                        time.sleep(n)
                        try:
                            response = requests.post(url=self.url, headers=self.headers, json=data)
                            self.assertIn('操作成功', response.text)
                        except:
                            time.sleep(n + 1)
                            if n == 10:
                                print('网络可能出问题了')
                                break
                            continue


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
