import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class IndexController(unittest.TestCase):
    """公共数据"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

    def test_01_student_dynamic(self):
        """
        学生同学动态
        :return:
        """
        url = f'{self.ip}/index/student/dynamic'
        data = 'pageNum=1&pageSize=10'
        res = requests.get(url=url, headers=self.student_headers, params=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/index/student/dynamic报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/index/student/dynamic，返回{data_ret},与预期不符')
        else:
            print([i['nickname'] for i in data_list])

    def test_02_student_homework(self):
        """
        学生最近作业
        :return:
        """
        url = f'{self.ip}/index/student/homework'
        data = 'pageNum=1&pageSize=10'
        res = requests.get(url=url, headers=self.student_headers, params=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/index/student/homework，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/index/student/homework，返回{data_ret},与预期不符')
        else:
            print([{i['homeworkName']: i['finishCount']} for i in data_list])

    def test_03_student_statistics(self):
        """
        学生统计
        :return:
        """
        url = f'{self.ip}/index/student/statistics'
        res = requests.get(url=url, headers=self.student_headers)
        assert_res(res.text)
        print(res.text)

    def test_04_teacher_dynamic(self):
        """
        老师拉学生动态
        :return:
        """
        url = f'{self.ip}/index/teacher/dynamic'
        data = 'pageNum=1&pageSize=10'
        res = requests.get(url=url, headers=self.teacher_headers, params=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/index/teacher/dynamic，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/index/teacher/dynamic，返回{data_ret},与预期不符')
        else:
            print([i['nickname'] for i in data_list])

    def test_05_teacher_homework(self):
        """
        老师最近作业
        :return:
        """
        url = f'{self.ip}/index/teacher/homework'
        data = 'pageNum=1&pageSize=10'
        res = requests.get(url=url, headers=self.teacher_headers, params=data)
        assert_res(res.text)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/index/teacher/homework，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/index/teacher/homework，返回{data_ret},与预期不符')
        else:
            print([{i['homeworkName']: i['finishCount']} for i in data_list])

    def test_06_teacher_statistics(self):
        """
        老师统计数据
        :return:
        """
        url = f'{self.ip}/index/teacher/statistics'
        res = requests.get(url=url, headers=self.teacher_headers)
        assert_res(res.text)
        print(res.text)

    def test_07_user_messages(self):
        """
        用户消息
        :return:
        """
        url = f'{self.ip}/index/user/messages'
        for s in range(2):
            data = {
                "pageNum": 1,
                "pageSize": 10,
                "status": s
            }
            res = requests.post(url=url, headers=self.student_headers, json=data)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                print(f'接口/index/user/messages，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口/index/user/messages，返回{data_ret},与预期不符')
            else:
                print([{i['id']: i['content']} for i in data_list])

    def test_08_user_course(self):
        """
        用户最近课程
        :return:
        """
        series_id_list = self.teacher_parm.get_series_list()
        class_id_list = self.teacher_parm.get_class_list()
        url = f'{self.ip}/index/user/courses'
        for class_id in class_id_list:
            for series_id in series_id_list:
                for f in range(2):
                    data = {
                        "classId": class_id,
                        "flag": f,
                        "pageNum": 1,
                        "pageSize": 10,
                        "seriesId": series_id
                    }
                    res = requests.post(url=url, headers=self.teacher_headers, json=data)
                    assert_res(res.text)
                    time.sleep(1)
                    data_ret = res.json()
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口/index/user/courses，返回{data_ret["msg"]}')
                    except KeyError:
                        print(f'接口/index/user/courses，返回{data_ret},与预期不符')
                    else:
                        print([{i['seriesName']: [i['issueName'], i['planWeeks'], i['flag']]} for i in data_list])

    def test_09_messages_opt(self):
        """
        用户消息操作
        :return:
        """
        msg_id_list = self.teacher_parm.get_msg_id_list()
        url = f'{self.ip}/index/user/messages/opt'
        for f in [1, 0, -1]:
            data = {
                "flag": f,
                "messageIds": [
                    msg_id_list[0]
                ]
            }
            res = requests.post(url=url, headers=self.teacher_headers, json=data)
            assert_res(res.text)
            time.sleep(1)
