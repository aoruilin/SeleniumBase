import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class GateHomeworkStudentController(unittest.TestCase):
    """闯关授课学生作业模块"""

    def setUp(self) -> None:
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.student_parm.ip
        self.student_headers = self.student_parm.headers
        self.eval_id_list = self.student_parm.get_eval_id()

    def test_01_challenge_problem(self):
        """
        换一道题/随机一道题
        :return:
        """
        for i in range(3):
            url = f'{self.ip}/pc/gate/homework/student/challengeProblem/{self.eval_id_list[i]}'
            response = requests.get(url=url, headers=self.student_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print({data_ret['data']['id']: data_ret['data']['title']})
            except TypeError:
                print(f'接口"/pc/gate/homework/student/challengeProblem"报错，返回{data_ret["msg"]}')

    def test_02_do_the_most_statistics(self):
        """
        获取对得最多统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/doTheMostStatistics/{self.eval_id_list[0]}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([{i['title']: i['correctNums']} for i in data_ret['data']['statistics']])
        except TypeError:
            print(f'接口"/pc/gate/homework/student/doTheMostStatistics"报错，返回{data_ret["msg"]}')

    def test_03_get_fastest_answer_statistics(self):
        """
        获取做得最快统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/getFastestAnswerStatistics/{self.eval_id_list[0]}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print(
                [
                    {
                        i['title']: {
                            f'最快{i["fastestInfo"]["nickname"]}': f'{i["fastestInfo"]["doTime"]}秒',
                            f'自己{i["myinfo"]["nickname"]}': f'{i["myinfo"]["doTime"]}秒'
                        }
                    } for i in data_ret['data']
                ]
            )
        except TypeError:
            print(f'接口"/pc/gate/homework/student/getFastestAnswerStatistics"报错，返回{data_ret["msg"]}')

    def test_04_get_student_best_answer_statistics(self):
        """
        获取做得最好统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/getStuBastAnswerStatistics/{self.eval_id_list[0]}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print(
                [
                    {
                        i['title']: f'班级平均代码长度{i["avgLength"]},班级平均做题时间{i["avgDoTime"]}'
                    } for i in data_ret['data']
                ]
            )
        except TypeError:
            print(f'接口"/pc/gate/homework/student/getStuBastAnswerStatistics"报错，返回{data_ret["msg"]}')

    def test_05_homework_eval(self):
        """
        获得作业完成信息列表
        :return:
        """
        gate_id_list = [g['gate_id'] for g in self.student_parm.get_point_id_checkpoint(get_all=True)]
        class_id_list = self.student_parm.get_class_list(get_all=True)
        url = f'{self.ip}/pc/gate/homework/student/homeworkEval'
        for c in class_id_list:
            for a in gate_id_list:
                for s in range(3):
                    data = f'pageNum=1&pageSize=12&classId={c}&gateId={a}&evalStatus={s}'
                    response = requests.get(url=url, headers=self.student_headers,
                                            params=data)
                    assert_res(response.text)
                    time.sleep(1)
                    data_ret = response.json()
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口"/pc/gate/homework/student/homeworkEval"报错，返回{data_ret["msg"]}')
                    else:
                        print([{i['homeworkId']: i['homeworkName']} for i in data_list])

    def test_06_homework_eval(self):
        """
        获取作业完成信息
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/homeworkEval/{self.eval_id_list[0]}'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print({data_ret['data']['homeworkId']: data_ret['data']['homeworkName']})
        except TypeError:
            print(f'接口"/pc/gate/homework/student/homeworkEval"报错，返回{data_ret["msg"]}')

    def test_07_homework_eval_challenge(self):
        """
        获取紧急挑战作业完成信息
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/homeworkEvalChallenge'
        data = f'pageNum=1&pageSize=12&evalId={self.eval_id_list[0]}&' \
               f'studentId={self.student_parm.get_user_school_id()[0]}'
        response = requests.get(url=url, headers=self.student_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['recordList']['list']
        except TypeError:
            print(f'接口"/pc/gate/homework/student/homeworkEvalChallenge"报错，返回{data_ret["msg"]}')
        else:
            print([{i['title']: i['result']} for i in data_list])

    def test_08_multi(self):
        """
        获得作业紧急挑战详细完成信息列表,多文本编辑器中
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/homeworkEvalChallenge/multi'
        for s in range(2):
            data = f'pageNum=1&pageSize=12&evalId={self.eval_id_list[0]}&sort={s}'
            response = requests.get(url=url, headers=self.student_headers,
                                    params=data)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                print(f'接口"/pc/gate/homework/student/homeworkEvalChallenge/multi"报错，返回{data_ret["msg"]}')
            else:
                print([{i['title']: i['result']} for i in data_list])

    def test_09_multi_record_id(self):
        """
        获取指定紧急挑战作业详细完成信息,多文本编辑器中
        :return:
        """
        record_id_list = self.student_parm.get_challenge_record_id_list()
        for record_id in record_id_list:
            url = f'{self.ip}/pc/gate/homework/student/homeworkEvalChallenge/multi/{record_id}'
            response = requests.get(url=url, headers=self.student_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print({data_ret['data']['problem']['title']: data_ret['data']['result']})
            except TypeError:
                print(f'接口"/pc/gate/homework/student/homeworkEvalChallenge/multi"报错，返回{data_ret["msg"]}')

    def test_10_homework_eval_record(self):
        """
        获得作业详细完成信息列表
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/homeworkEvalRecord'
        data = f'pageNum=1&pageSize=12&evalId={self.student_parm.get_eval_id()[0]}'
        response = requests.get(url=url, headers=self.student_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/homework/student/homeworkEvalChallenge/multi"报错，返回{data_ret["msg"]}')
        else:
            print([{i['title']: i['result']} for i in data_list])

    def test_11_multi(self):
        """
        获得作业详细完成信息列表,多文本编辑器中
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/student/homeworkEvalRecord/multi'
        data = f'pageNum=1&pageSize=12&evalId={self.student_parm.get_eval_id()[0]}'
        response = requests.get(url=url, headers=self.student_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([{i['title']: i['result']} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/gate/homework/student/homeworkEvalChallenge/multi"报错，返回{data_ret["msg"]}')

    def test_12_record_multi(self):
        """
        获取指定作业详细完成信息,多文本编辑器中
        :return:
        """
        record_id_list = self.student_parm.get_record_id_list()
        for record_id in record_id_list:
            url = f'{self.ip}/pc/gate/homework/student/homeworkEvalRecord/multi/{record_id}'
            response = requests.get(url=url, headers=self.student_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print({data_ret['data']['problem']['title']: data_ret['data']['result']})
            except TypeError:
                print(f'接口"/pc/gate/homework/student/homeworkEvalRecord/multi"报错，返回{data_ret["msg"]}')


if __name__ == "__main__":
    unittest.main()
