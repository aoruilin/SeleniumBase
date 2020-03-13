import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class GateCourseController(unittest.TestCase):
    """闯关授课课程相关接口"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers

        self.class_id_list = self.teacher_parm.get_class_list(1, get_all=True)
        self.course_id = self.teacher_parm.get_customs_course_list(self.class_id_list[0])[0]

    def test_01_del_course_by_class(self):
        """
        将我发布的课程指定的班级下架（删除）
        :return:
        """
        url = f'{self.ip}/pc/gate/course/delCourseByClass'
        data = {
            'classId': self.class_id_list[0],
            'courseId': self.course_id,
            'status': 2
        }
        response = requests.post(url=url, headers=self.teacher_headers, json=data)
        assert_res(response.text, '操作成功')

    def test_02_get_course_plan_detail(self):
        """
        获取课件详情
        :return:
        """
        url = f'{self.ip}/pc/gate/course/getCoursePlanDetail?' \
              f'courseId={self.course_id}&classId={self.class_id_list[0]}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            print({
                data_ret['data']['pointName']: data_ret['data']['title']
            })
        except TypeError:
            print(f'接口"/pc/gate/course/getCoursePlanDetail"报错，返回{data_ret["msg"]}')

    def test_03_get_customs_course_list(self):
        """
        获取闯关授课课件列表
        :return:
        """
        for class_id in self.class_id_list:
            for s in range(3):
                url = f'{self.ip}/pc/gate/course/getCustomsCourseList?' \
                      f'pageNum=1&pageSize=6&classId={class_id}&status={s}&sort={s}&allFlg=1'
                response = requests.get(url=url, headers=self.teacher_headers)
                assert_res(response.text, '操作成功')
                time.sleep(1)
                data_ret = response.json()
                try:
                    data_list = data_ret['data']['list']
                except TypeError:
                    print(f'接口"/pc/gate/course/getCustomsCourseList"报错，返回{data_ret["msg"]}')
                else:
                    course = [{i['title']: i['id']} for i in data_list]
                    print(course)

    def test_04_get_gate_course_plan_detail_list(self):
        """
        获取关卡课件详情列表
        :return:
        """
        gate_id_list = self.teacher_parm.get_point_id_checkpoint(get_all=True)
        for g in gate_id_list:
            url = f'{self.ip}/pc/gate/course/getGateCoursePlanDetailList' \
                  f'?classId={self.class_id_list[0]}&gateId={g["gate_id"]}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print([{i['id']: i['title']} for i in data_ret['data']])
            except TypeError:
                print(f'接口"/pc/gate/course/getGateCoursePlanDetailList"报错，返回{data_ret["msg"]}')

    def test_05_get_personal_upload_resource_plan_list(self):
        """
        获取学校或个人资源列表
        :return:
        """
        for s in range(1, 3):
            for k in ['', '千年']:
                url = f'{self.ip}/pc/gate/course/getPersonalUploadResourcePlanList' \
                      f'?language=2&category={s}&pageNum=1&pageSize=6&keywords={k}'
                response = requests.get(url=url, headers=self.teacher_headers)
                assert_res(response.text)
                time.sleep(1)
                data_ret = response.json()
                try:
                    data_list = data_ret['data']['list']
                except TypeError:
                    print(f'接口"/pc/gate/course/getPersonalUploadResourcePlanList"报错，返回{data_ret["msg"]}')
                else:
                    print([{i['id']: i['title']} for i in data_list])

    def test_06_resource_plan_detail(self):
        """
        获取资源详情
        :return:
        """
        course_id_list = self.teacher_parm.get_resource_plan_id()
        url = f'{self.ip}/pc/gate/course/getResourcePlanDetail?id={course_id_list[0]}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_dic = data_ret['data']
            print({data_dic['id']: [data_dic['title'], f'状态{data_dic["status"]}']})
        except TypeError:
            print(f'接口"/pc/gate/course/getResourcePlanDetail"报错，返回{data_ret["msg"]}')

    def test_07_get_resource_plan_list(self):
        """
        获取资源列表
        :return:
        """
        point_id_dic_list = self.teacher_parm.get_point_id_checkpoint(get_all=True)
        point_id_list = [p['point_id'] for p in point_id_dic_list]
        for point_id in point_id_list:
            url = f'{self.ip}/pc/gate/course/getResourcePlanList' \
                  f'?resourceType=1&pointId={point_id}&pageNum=1&pageSize=3'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                print(f'接口"/pc/gate/course/getResourcePlanList"报错，返回{data_ret["msg"]}')
            else:
                print([{i['id']: i['title']} for i in data_list])

    def test_08_publish_customs_course(self):
        """
        发布闯关授课课件
        :return:
        """
        url = f'{self.ip}/pc/gate/course/publishCustomsCourse'
        id_dic = self.teacher_parm.get_point_id_checkpoint()
        gate_id = id_dic['gate_id']
        point_id = id_dic['point_id']
        resource_plan_id_list = self.teacher_parm.get_resource_plan_id()
        for r in resource_plan_id_list:
            for i in range(1, 3):
                data = {
                    "classIds": self.teacher_parm.get_class_list(1),
                    "gateId": gate_id,
                    "language": 2,
                    "pointId": point_id,
                    "resourcePlanId": r,
                    "status": i
                }
                response = requests.post(url=url, headers=self.teacher_headers, json=data)
                assert_res(response.text)
                time.sleep(1)

    def test_09_publish_customs_course_check(self):
        """
        发布闯关授课课件检查
        :return:
        """
        url = f'{self.ip}/pc/gate/course/publishCustomsCourseCheck'
        id_dic = self.teacher_parm.get_point_id_checkpoint()
        gate_id = id_dic['gate_id']
        point_id = id_dic['point_id']
        resource_plan_id_list = self.teacher_parm.get_resource_plan_id()
        for r in resource_plan_id_list:
            for i in range(1, 3):
                data = {
                    "classIds": self.teacher_parm.get_class_list(1),
                    "gateId": gate_id,
                    "language": 2,
                    "pointId": point_id,
                    "resourcePlanId": r,
                    "status": i
                }
                response = requests.post(url=url, headers=self.teacher_headers, json=data)
                assert_res(response.text)
                time.sleep(1)
                data_ret = response.json()
                try:
                    print([{i['className']: i['teacherName']} for i in data_ret['data']])
                except TypeError:
                    print(f'接口"/pc/gate/course/publishCustomsCourseCheck"报错，返回{data_ret["msg"]}')

    def test_10_up_course_by_class_status(self):
        """
        将我发布的课程指定的班级发布和撤回发布
        :return:
        """
        url = f'{self.ip}/pc/gate/course/upCourseByClassStatus'
        class_id = self.teacher_parm.get_class_list()[0]
        course_id = self.teacher_parm.get_customs_course_list(class_id)[0]
        for s in range(1, 3):
            data = {
                "classId": class_id,
                "courseId": course_id,
                "status": s
            }
            response = requests.post(url=url, headers=self.teacher_headers, json=data)
            assert_res(response.text)
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
