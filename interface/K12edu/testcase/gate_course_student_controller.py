import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class GateCourseStudentController(unittest.TestCase):
    """闯关授课课程学生相关接口"""

    def setUp(self) -> None:
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.student_parm.ip
        self.student_headers = self.student_parm.headers

    def test_01_get_student_customs_course_list(self):
        """
        获取课件列表
        :return:
        """
        class_id_list = self.student_parm.get_class_list(get_all=True)
        for class_id in class_id_list:  # 班级
            for s in range(3):  # 查看状态和全部
                for o in range(2):  # 排序
                    for k in ['', '自动']:  # 关键字搜索
                        url = f'{self.ip}/pc/gate/course/student/getStudentCustomsCourseList' \
                              f'?pageNum=1&pageSize=6&status={s}&sort={o}&classId={class_id}&keyword={k}'
                        response = requests.get(url=url, headers=self.student_headers)
                        assert_res(response.text)
                        time.sleep(1)
                        data_ret = response.json()
                        try:
                            data_list = data_ret['data']['list']
                        except TypeError:
                            print('接口"/pc/gate/course/student/getStudentCustomsCourseList"报错，'
                                  f'返回{data_ret["msg"]}')
                        else:
                            print([{i['id']: {i['title']: f"状态：{i['status']}"}} for i in data_list])

    def test_02_student_customs_course(self):
        """
        学生获取课件详细信息
        :return:
        """
        class_id = self.student_parm.get_class_list(get_all=True)[-1]
        course_id = self.student_parm.get_student_customs_course_list(class_id)[0]
        url = f'{self.ip}/pc/gate/course/student/studentCustomsCourse/{course_id}/class/{class_id}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_dic = data_ret['data']
            print({data_dic['id']: data_dic['title']})
        except TypeError:
            print(f'接口"/pc/gate/course/student/studentCustomsCourse"报错，返回{data_ret["msg"]}')


if __name__ == '__main__':
    unittest.main()
