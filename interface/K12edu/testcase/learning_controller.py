import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class LearningController(unittest.TestCase):
    """学情分析"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.series_id_list = self.teacher_parm.get_series_list(2)
        self.teacher_class_id_list = self.teacher_parm.get_class_list(get_all=True)
        self.student_class_id_list = self.student_parm.get_class_list(get_all=True)
        self.student_id, _ = self.student_parm.get_user_school_id()

    def test_01_chart(self):
        """
        折线图（学生和老师）
        :return:
        """
        for i in ['student', 'teacher']:
            url = f'{self.ip}/learning/{i}/chart' \
                if 'student' == i else f'{self.ip}/learning/{i}/chart/{self.student_id}'
            header = self.student_headers if i == 'student' else self.teacher_headers
            class_id_list = self.student_class_id_list if i == 'student' else self.teacher_class_id_list
            for series_id in self.series_id_list:
                for class_id in class_id_list:
                    for flag in ['', 1]:
                        params = f'seriesId={series_id}&classId={class_id}&flag={flag}' \
                            if flag == 1 else f'seriesId={series_id}&classId={class_id}'
                        res = requests.get(url=url, headers=header, params=params)
                        assert_res(res.text)
                        time.sleep(1)
                        data_ret = res.json()
                        try:
                            print([{d['name']: d['grade']} for d in data_ret['data']])
                        except TypeError:
                            msg = '接口正常，没有数据' \
                                if data_ret['msg'] == '操作成功' else \
                                f'接口/learning/{i}/chart报错，返回{data_ret["msg"]}'
                            print(msg)
                        except KeyError:
                            print(f'接口/learning/{i}/chart，返回{data_ret},与预期不符')

    def test_02_detail(self):
        """
        详情（学生和老师）
        :return:
        """
        for i in ['student', 'teacher']:
            url = f'{self.ip}/learning/{i}/detail' \
                if 'student' == i else f'{self.ip}/learning/{i}/detail/{self.student_id}'
            header = self.student_headers if i == 'student' else self.teacher_headers
            class_id_list = self.student_class_id_list if i == 'student' else self.teacher_class_id_list
            for series_id in self.series_id_list:
                for class_id in class_id_list:
                    for flag in ['', 1]:
                        params = f'seriesId={series_id}&classId={class_id}&flag={flag}' \
                            if flag == 1 else f'seriesId={series_id}&classId={class_id}'
                        res = requests.get(url=url, headers=header, params=params)
                        assert_res(res.text)
                        time.sleep(1)
                        data_ret = res.json()
                        try:
                            print([(d['name'], d['grade'], d['avgGrade']) for d in data_ret['data']])
                        except TypeError:
                            msg = '接口正常，没有数据' \
                                if data_ret['msg'] == '操作成功' else \
                                f'接口/learning/{i}/detail报错，返回{data_ret["msg"]}'
                            print(msg)
                        except KeyError:
                            print(f'接口/learning/{i}/detail，返回{data_ret},与预期不符')

    def test_03_detail_page(self):
        """
        学生-自己详情
        老师-学生详情-数据分页
        :return:
        """
        for i in ['student', 'teacher']:
            url = f'{self.ip}/learning/{i}/detail/page' \
                if 'student' == i else f'{self.ip}/learning/{i}/detail/page/{self.student_id}'
            header = self.student_headers if i == 'student' else self.teacher_headers
            class_id_list = self.student_class_id_list if i == 'student' else self.teacher_class_id_list
            for series_id in self.series_id_list:
                for class_id in class_id_list:
                    for flag in ['', 1]:
                        params = f'seriesId={series_id}&classId={class_id}&flag={flag}&pageNum=1&pageSize=30' \
                            if flag == 1 else f'seriesId={series_id}&classId={class_id}&pageNum=1&pageSize=30'
                        res = requests.get(url=url, headers=header, params=params)
                        assert_res(res.text)
                        time.sleep(1)
                        data_ret = res.json()
                        try:
                            data_list = data_ret['data']['list']
                        except TypeError:
                            msg = '接口正常，没有数据' \
                                if data_ret['msg'] == '操作成功' else \
                                f'接口/learning/{i}/detail/page报错，返回{data_ret["msg"]}'
                            print(msg)
                        except KeyError:
                            print(f'接口/learning/{i}/detail/page，返回{data_ret},与预期不符')
                        else:
                            print([(d['name'], d['grade'], d['avgGrade']) for d in data_list])

    def test_04_evaluate(self):
        """
        学生-自己编程能力
        老师-学生详情-编程能力
        :return:
        """
        out_list = []
        for i in ['student', 'teacher']:
            url = f'{self.ip}/learning/{i}/evaluate' \
                if 'student' == i else f'{self.ip}/learning/{i}/evaluate/{self.student_id}'
            header = self.student_headers if i == 'student' else self.teacher_headers
            res = requests.get(url=url, headers=header)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                out_list.append([{i['label']: i['score']} for i in data_ret['data']])
                print(f'{i}:{[{i["label"]: i["score"]} for i in data_ret["data"]]}')
            except TypeError:
                print(f'接口"/learning/{i}/evaluate"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口/learning/{i}/evaluate，返回{data_ret},与预期不符')
        try:
            assert out_list[0] == out_list[1]
        except AssertionError:
            print('教师和学生数据不一致')

    def test_05_weak(self):
        """
        学生-自己薄弱统计
        老师-学生详情-薄弱统计
        :return:
        """
        for i in ['student', 'teacher']:
            url = f'{self.ip}/learning/{i}/weak' \
                if 'student' == i else f'{self.ip}/learning/{i}/weak/{self.student_id}'
            header = self.student_headers if i == 'student' else self.teacher_headers
            for series_id in self.series_id_list:
                params = f'seriesId={series_id}'
                res = requests.get(url=url, headers=header, params=params)
                assert_res(res.text)
                time.sleep(1)
                data_ret = res.json()
                try:
                    print([{i['label']: i['grade']} for i in data_ret['data']])
                except TypeError:
                    msg = '接口正常，没有数据' \
                        if data_ret['msg'] == '操作成功' else \
                        f'接口/learning/{i}/weak报错，返回{data_ret["msg"]}'
                    print(msg)
                except KeyError:
                    print(f'接口/learning/{i}/weak，返回{data_ret},与预期不符')

    def test_06_teacher_analysis(self):
        """
        老师-学情分析
        :return:
        """
        url = f'{self.ip}/learning/teacher/analysis'
        res = requests.get(url=url, headers=self.teacher_headers)
        assert_res(res.text)

    def test_07_teacher_classes(self):
        """
        老师-班级信息
        :return:
        """
        url = f'{self.ip}/learning/teacher/classes'
        res = requests.get(url=url, headers=self.teacher_headers)
        assert_res(res.text)

    def test_08_teacher_course(self):
        """
        老师-课程统计
        老师-作业统计
        :return:
        """
        for i in ['course', 'homework']:
            url = f'{self.ip}/learning/teacher/{i}'
            for series_id in self.series_id_list:
                for class_id in self.teacher_class_id_list:
                    for flag in ['', 1]:
                        data = {
                            "classId": class_id,
                            "flag": flag,
                            "seriesId": series_id
                        } if flag == 1 else {
                            "classId": class_id,
                            "seriesId": series_id
                        }
                        res = requests.post(url=url, headers=self.teacher_headers, json=data)
                        assert_res(res.text)
                        time.sleep(1)
                        data_ret = res.json()
                        try:
                            best = data_ret['data']['best']
                            worst = data_ret['data']['worst']
                            data_list = data_ret['data']['datas']
                        except TypeError:
                            msg = '接口正常，没有数据' \
                                if data_ret['msg'] == '操作成功' else \
                                f'接口/learning/teacher/{i}报错，返回{data_ret["msg"]}'
                            print(msg)
                        except KeyError:
                            print(f'接口/learning/teacher/{i}，返回{data_ret},与预期不符')
                        else:
                            print(f'{i}:{({"best": best["label"]}, {"worst": worst["label"]})}')
                            print(f'{i}:{[{d["label"]: d["rate"]} for d in data_list]}')

    def test_09_teacher_student(self):
        """
        老师-学生学情
        :return:
        """
        url = f'{self.ip}/learning/teacher/student'
        for class_id in self.teacher_class_id_list:
            params = f'classId={class_id}'
            res = requests.get(url=url, headers=self.teacher_headers, params=params)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                print([{i['name']: i['avgGrade']} for i in data_ret['data']])
            except TypeError:
                msg = '接口正常，没有数据' \
                    if data_ret['msg'] == '操作成功' else \
                    f'接口/learning/teacher/student报错，返回{data_ret["msg"]}'
                print(msg)
            except KeyError:
                print(f'接口/learning/teacher/student，返回{data_ret},与预期不符')

    def test_10_student_page(self):
        """
        老师-学生学情-分页
        :return:
        """
        url = f'{self.ip}/learning/teacher/student/page'
        for class_id in self.teacher_class_id_list:
            params = f'classId={class_id}&pageNum=1&pageSize=30'
            res = requests.get(url=url, headers=self.teacher_headers, params=params)
            assert_res(res.text)
            time.sleep(1)
            data_ret = res.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                msg = '接口正常，没有数据' \
                    if data_ret['msg'] == '操作成功' else \
                    f'接口/learning/teacher/student/page报错，返回{data_ret["msg"]}'
                print(msg)
            except KeyError:
                print(f'接口/learning/teacher/student/page，返回{data_ret},与预期不符')
            else:
                print([{i['name']: i['avgGrade']} for i in data_list])

    def test_11_user_homework_series(self):
        """
        用户-作业-系列集
        :return:
        """
        url = f'{self.ip}/learning/user/homework/series'
        for i in ['student', 'teacher']:
            header = self.student_headers if i == 'student' else self.teacher_headers
            class_id_list = self.student_class_id_list if i == 'student' else [1]
            for class_id in class_id_list:
                params = f'classId={class_id}' if i == 'student' else 'classId='
                res = requests.get(url=url, headers=header, params=params)
                assert_res(res.text)
                time.sleep(1)
                data_ret = res.json()
                try:
                    print(f'{i}:{[{i["id"]: i["name"]} for i in data_ret["data"]]}')
                except TypeError:
                    msg = '接口正常，没有数据' \
                        if data_ret['msg'] == '操作成功' else \
                        f'接口/learning/homework/series报错，返回{data_ret["msg"]}'
                    print(msg)
                except KeyError:
                    print(f'接口/learning/homework/series，返回{data_ret},与预期不符')


if __name__ == '__main__':
    unittest.main()
