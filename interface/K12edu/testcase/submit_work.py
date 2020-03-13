import unittest
import requests
import time

from interface.K12edu.common.parameter_for_others import ParameterForOthers
from interface.K12edu.common.picture_list_code import author_picture, work_picture, turtle_code


class SubmitWork(unittest.TestCase):

    def setUp(self):
        self.teacher_parameter = ParameterForOthers('teacher')
        self.student_parameter = ParameterForOthers('student')
        self.ip = self.teacher_parameter.ip
        self.teacher_headers = self.teacher_parameter.headers
        self.student_headers = self.student_parameter.headers

    def test_01(self):
        '''学生端上传作品教师审核发布'''
        # 获取审核教师ID
        teacher_id_url = f'{self.ip}/pc/worksDisplay/getTeacherListByClassId'
        teacher_id_response = requests.get(url=teacher_id_url, headers=self.student_headers)
        data_ret = teacher_id_response.json()
        data_list = data_ret['data']
        teacher_info = data_list[0]
        user_list = teacher_info['userList']
        user = user_list[0]
        teacher_id = user['id']
        time.sleep(1)
        # 获取班级ID
        class_id_url = f'{self.ip}/pc/worksDisplay/studentClassList'
        class_id_response = requests.get(url=class_id_url, headers=self.student_headers)
        data_ret = class_id_response.json()
        data_list = data_ret['data']
        class_info = data_list[0]
        class_id = class_info['id']
        time.sleep(1)
        # 学生上传作品
        for i in range(0, 2):
            student_data = {
                "authorList": [],
                "description": "学生端上传作品接口测试",
                "isCreate": 0,
                "title": "自动作品",
            }
            author_picture_list = author_picture()
            student_data['authorPictureList'] = author_picture_list
            work_picture_list = work_picture()
            student_data['worksPictureList'] = work_picture_list
            code = turtle_code()
            student_data['code'] = code
            student_data['isPublishCode'] = i
            student_data['classId'] = class_id
            student_data['teacherId'] = teacher_id
            post_work_url = f'{self.ip}/pc/worksDisplay/postWorkByStudentWaitReview'
            post_work_response = requests.post(url=post_work_url, headers=self.student_headers, json=student_data)
            self.assertIn('操作成功', post_work_response.text, '学生端作品提交失败')
            time.sleep(1)
        # 获取作品ID
        get_work_id_url = f'{self.ip}/pc/worksDisplay/getMyWorksList?status=2&pageNum=1&pageSize=15&sort=0&keyword='
        work_id_response = requests.get(url=get_work_id_url, headers=self.student_headers)
        data_ret = work_id_response.json()
        data_dic = data_ret['data']
        data_list = data_dic['list']
        first_work = data_list[0]
        first_work_id = first_work['id']
        second_work = data_list[1]
        second_work_id = second_work['id']
        time.sleep(1)
        # 获取学生ID作为authorID
        author_list = []
        get_student_id_url = f'{self.ip}/pc/worksDisplay/getWorkDetailById?worksId={first_work_id}'
        student_id_response = requests.get(url=get_student_id_url, headers=self.student_headers)
        data_ret = student_id_response.json()
        data_dic = data_ret['data']
        author_id = data_dic['worksAuthorId']
        author_list.append(author_id)
        time.sleep(1)
        # 教师审核作品
        audit_work_url = f'{self.ip}/pc/worksDisplay/postWorkByTeacherPublish'
        teacher_data = {
            "description": "教师端审核通过作品接口测试",
            "isCreate": 1,
            "title": "自动发布作品",
            "teacherComment": "教师审核通过",
            "isUpdateWorks": 0
        }
        author_picture_list = author_picture()
        teacher_data['authorPictureList'] = author_picture_list
        teacher_data['authorList'] = author_list
        work_picture_list = work_picture()
        teacher_data['worksPictureList'] = work_picture_list
        code = turtle_code()
        teacher_data['code'] = code
        teacher_data['id'] = first_work_id
        teacher_data['isPublishCode'] = 1
        teacher_data['teacherId'] = teacher_id
        teacher_data['classId'] = class_id
        audit_work_response = requests.post(url=audit_work_url, headers=self.teacher_headers, json=teacher_data)
        self.assertIn('操作成功', audit_work_response.text, '教师端审核作品失败')
        time.sleep(1)
        teacher_data['id'] = second_work_id
        teacher_data['isPublishCode'] = 0
        audit_work_response = requests.post(url=audit_work_url, headers=self.teacher_headers, json=teacher_data)
        self.assertIn('操作成功', audit_work_response.text, '教师端审核作品失败')
        time.sleep(1)

    def test_02(self):
        '''学生端上传作品教师驳回'''
        # 获取审核教师ID
        teacher_id_url = f'{self.ip}/pc/worksDisplay/getTeacherListByClassId'
        teacher_id_response = requests.get(url=teacher_id_url, headers=self.student_headers)
        data_ret = teacher_id_response.json()
        data_list = data_ret['data']
        teacher_info = data_list[0]
        user_list = teacher_info['userList']
        user = user_list[0]
        teacher_id = user['id']
        time.sleep(1)
        # 获取班级ID
        class_id_url = f'{self.ip}/pc/worksDisplay/studentClassList'
        class_id_response = requests.get(url=class_id_url, headers=self.student_headers)
        data_ret = class_id_response.json()
        data_list = data_ret['data']
        class_info = data_list[0]
        class_id = class_info['id']
        time.sleep(1)
        # 学生上传作品
        for i in range(0, 2):
            student_data = {
                "authorList": [],
                "description": "学生端上传作品接口测试",
                "isCreate": 0,
                "title": "自动驳回作品",
            }
            author_picture_list = author_picture()
            student_data['authorPictureList'] = author_picture_list
            work_picture_list = work_picture()
            student_data['worksPictureList'] = work_picture_list
            code = turtle_code()
            student_data['code'] = code
            student_data['isPublishCode'] = i
            student_data['classId'] = class_id
            student_data['teacherId'] = teacher_id
            post_work_url = f'{self.ip}/pc/worksDisplay/postWorkByStudentWaitReview'
            post_work_response = requests.post(url=post_work_url, headers=self.student_headers, json=student_data)
            self.assertIn('操作成功', post_work_response.text, '学生端作品提交失败')
            time.sleep(1)
        # 获取作品ID
        get_work_id_url = f'{self.ip}/pc/worksDisplay/getMyWorksList?status=2&pageNum=1&pageSize=15&sort=0&keyword='
        work_id_response = requests.get(url=get_work_id_url, headers=self.student_headers)
        data_ret = work_id_response.json()
        data_dic = data_ret['data']
        data_list = data_dic['list']
        first_work = data_list[0]
        first_work_id = first_work['id']
        second_work = data_list[1]
        second_work_id = second_work['id']
        time.sleep(1)
        # 获取学生ID作为authorID
        author_list = []
        get_student_id_url = f'{self.ip}/pc/worksDisplay/getWorkDetailById?worksId={first_work_id}'
        student_id_response = requests.get(url=get_student_id_url, headers=self.student_headers)
        data_ret = student_id_response.json()
        data_dic = data_ret['data']
        author_id = data_dic['worksAuthorId']
        author_list.append(author_id)
        time.sleep(1)
        # 教师驳回作品
        audit_work_url = f'{self.ip}/pc/worksDisplay/postWorkByTeacherReject'
        teacher_data = {
            "description": "教师端审核驳回作品接口测试",
            "isCreate": 1,
            "title": "自动驳回作品",
            "teacherComment": "教师审核驳回",
            "isUpdateWorks": 1
        }
        author_picture_list = author_picture()
        teacher_data['authorPictureList'] = author_picture_list
        teacher_data['authorList'] = author_list
        work_picture_list = work_picture()
        teacher_data['worksPictureList'] = work_picture_list
        code = turtle_code()
        teacher_data['code'] = code
        teacher_data['id'] = first_work_id
        teacher_data['isPublishCode'] = 1
        teacher_data['teacherId'] = teacher_id
        teacher_data['classId'] = class_id
        audit_work_response = requests.post(url=audit_work_url, headers=self.teacher_headers, json=teacher_data)
        self.assertIn('操作成功', audit_work_response.text, '教师端驳回作品失败')
        time.sleep(1)
        teacher_data['id'] = second_work_id
        teacher_data['isPublishCode'] = 0
        audit_work_response = requests.post(url=audit_work_url, headers=self.teacher_headers, json=teacher_data)
        self.assertIn('操作成功', audit_work_response.text, '教师端驳回作品失败')
        time.sleep(1)

    def test_03(self):
        """
        学生端上传作品教师不审核
        :return:
        """
        # 获取审核教师ID
        teacher_id_url = f'{self.ip}/pc/worksDisplay/getTeacherListByClassId'
        teacher_id_response = requests.get(url=teacher_id_url, headers=self.student_headers)
        data_ret = teacher_id_response.json()
        data_list = data_ret['data']
        teacher_info = data_list[0]
        user_list = teacher_info['userList']
        user = user_list[0]
        teacher_id = user['id']
        time.sleep(1)
        # 获取班级ID
        class_id_url = f'{self.ip}/pc/worksDisplay/studentClassList'
        class_id_response = requests.get(url=class_id_url, headers=self.student_headers)
        data_ret = class_id_response.json()
        data_list = data_ret['data']
        class_info = data_list[0]
        class_id = class_info['id']
        time.sleep(1)
        # 学生上传作品
        for i in range(0, 2):
            student_data = {
                "authorList": [],
                "description": "学生端上传作品接口测试",
                "isCreate": 0,
                "title": "学生端上传作品不审核",
            }
            author_picture_list = author_picture()
            student_data['authorPictureList'] = author_picture_list
            work_picture_list = work_picture()
            student_data['worksPictureList'] = work_picture_list
            code = turtle_code()
            student_data['code'] = code
            student_data['isPublishCode'] = i
            student_data['classId'] = class_id
            student_data['teacherId'] = teacher_id
            post_work_url = f'{self.ip}/pc/worksDisplay/postWorkByStudentWaitReview'
            post_work_response = requests.post(url=post_work_url, headers=self.student_headers, json=student_data)
            self.assertIn('操作成功', post_work_response.text, '学生端作品提交失败')
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
