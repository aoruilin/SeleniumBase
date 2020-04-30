import unittest
import requests
import time
from base.data import Ips
from interface.uni_lab.common.login_for_others import login_interface
from interface.uni_lab.common.classId_for_others import getClassList
from interface.uni_lab.common.pointId_for_others import get_point_id
from interface.uni_lab.common.resourcePlanId_for_others import get_resourcePlan_id

class TestAddCourse(unittest.TestCase):
    '''添加课程'''
    def setUp(self):
        ip = Ips.ip_for_uniLab
        self.url = ip + '/pc/course/addCoursePlan'
        self.headers = {
            'Content-Type': "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/73.0.3683.86 Safari/537.36"
        }

    def test_01(self):
        '''添加课程'''
        token = login_interface()
        self.headers['token'] = token
        point_id = get_point_id()
        resourcePlan_id = get_resourcePlan_id()
        for r in resourcePlan_id:
            for s in range(1, 3):
                data = {"language": 1}
                classId = getClassList()
                data['classIds'] = classId
                data['pointId'] = point_id[1]
                data['resourcePlanId'] = r
                data['status'] = s

                try:
                    response = requests.post(url=self.url, headers=self.headers, json=data)
                except:
                    n = 1
                    while True:
                        time.sleep(n)
                        try:
                            response = requests.post(url=self.url, headers=self.headers, json=data)
                        except:
                            time.sleep(n+1)
                            if n == 5:
                                print('超时了')
                                break
                            continue

        self.assertIn('操作成功', response.text)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
