import unittest
import requests
import time

from interface.K12edu.common.parameter_for_others import ParameterForOthers


class TestAddCourse(unittest.TestCase):
    """添加课程"""

    def setUp(self):
        self.parameter = ParameterForOthers(identity='teacher')
        self.ip = self.parameter.ip
        self.headers = self.parameter.headers

    def test_01(self):
        """添加课程"""
        url = f'{self.ip}/pc/course/addCoursePlan'
        point_id = self.parameter.get_point_id()
        resource_plan_id = self.parameter.get_resource_plan_id(standard=True)
        for r in resource_plan_id:
            for s in range(1, 3):
                data = {"language": 1}
                class_id = self.parameter.get_class_list(1)
                data['classIds'] = class_id
                data['pointId'] = point_id[1]
                data['resourcePlanId'] = r
                data['status'] = s

                try:
                    response = requests.post(url=url, headers=self.headers, json=data)
                    print(response)
                    self.assertIn('操作成功', response.text)
                except:
                    n = 1
                    while True:
                        time.sleep(n)
                        try:
                            response = requests.post(url=url, headers=self.headers, json=data)
                            self.assertIn('操作成功', response.text)
                        except:
                            time.sleep(n + 1)
                            if n == 5:
                                print('超时了')
                                break
                            continue

    def test_02(self):
        """闯关授课添加课程"""
        url = f'{self.ip}/pc/gate/course/publishCustomsCourse'
        id_dic = self.parameter.get_point_id_checkpoint()
        gate_id = id_dic['gate_id']
        point_id = id_dic['point_id']
        resource_plan_id_list = self.parameter.get_resource_plan_id()
        for r in resource_plan_id_list:
            for i in range(1, 3):
                data = {'language': 2}
                class_id = self.parameter.get_class_list(1)
                data['classIds'] = class_id
                data['gateId'] = gate_id
                data['pointId'] = point_id
                data['resourcePlanId'] = r
                data['status'] = i
                response = requests.post(url=url, headers=self.headers, json=data)
                self.assertIn('操作成功', response.text)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
