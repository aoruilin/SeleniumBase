import time
import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class GateHomeworkController(unittest.TestCase):
    """闯关授课作业模块"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.class_id = self.teacher_parm.get_class_list()[0]
        self.homework_id = self.teacher_parm.get_gate_teacher_homework_id()[0]
        self.eval_id_list = self.student_parm.get_eval_id()
        self.student_id, _ = self.student_parm.get_user_school_id()

    def test_01_comprehensive_statistics(self):
        """
        获取作业的综合统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/comprehensiveStatistics'
        gate_id_list = [g['gate_id'] for g in self.student_parm.get_point_id_checkpoint(get_all=True)]
        for gate_id in gate_id_list:
            for s in range(6):
                for t in range(2):
                    data = f'pageNum=1&pageSize=12&gateId={gate_id}&' \
                           f'homeworkId={self.homework_id}&classId={self.class_id}&' \
                           f'sort={s}&sortType={t}'
                    response = requests.get(url=url, headers=self.teacher_headers,
                                            params=data)
                    assert_res(response.text)
                    time.sleep(1)
                    data_ret = response.json()
                    try:
                        data_list = data_ret['data']['list']
                    except TypeError:
                        print(f'接口"/pc/gate/homework/comprehensiveStatistics"报错，返回{data_ret["msg"]}')
                    else:
                        print(
                            [
                                {
                                    i['nickname']: f'正确率{i["correctNumber"]}/{i["totalNums"]},level{i["level"]}'
                                } for i in data_list
                            ]
                        )

    def test_02_for_the_most_statistics(self):
        """
        对得最多统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/forTheMostStatistics/{self.homework_id}/class/{self.class_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['statistics']
        except TypeError:
            print(f'接口"/pc/gate/homework/forTheMostStatistics"报错，返回{data_ret["msg"]}')
        else:
            print([{i['title']: i['correctNums']} for i in data_list])

    def test_03_get_best_answer_statistics(self):
        """
        答得最好统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/getBastAnswerStatistics/{self.homework_id}/class/{self.class_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([{i['title']: i['avgCorrect']} for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/gate/homework/getBastAnswerStatistics"报错，返回{data_ret["msg"]}')

    def test_04_get_fastest_answer_statistics(self):
        """
        做得最快统计数据
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/getFastestAnswerStatistics/{self.homework_id}/class/{self.class_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print(
                [
                    {
                        i['title']: f'{i["fastestInfo"]["nickname"]}做的最快，用时{i["fastestInfo"]["doTime"]}'
                    } for i in data_ret['data']
                ]
            )
        except TypeError:
            print(f'接口"/pc/gate/homework/getFastestAnswerStatistics"报错，返回{data_ret["msg"]}')

    def test_05_homework(self):
        """
        获得作业详情
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homework/{self.homework_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text)
        data_ret = response.json()
        try:
            homework_name = data_ret['data']['name']
            data_list = data_ret['data']['problemList']
        except TypeError:
            print(f'接口"/pc/gate/homework/homework"报错，返回{data_ret["msg"]}')
        else:
            print([{homework_name: i['name']} for i in data_list])

    def test_06_homework_item(self):
        """
        获得作业题目列表
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homework/{self.homework_id}/item'
        data = 'pageNum=1&pageSize=12'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/homework/homework/item"报错，返回{data_ret["msg"]}')
        else:
            print([{i['id']: i['title']} for i in data_list])

    def test_07_homework_eval(self):
        """
        获取作业完成信息
        :return:
        """
        for eval_id in self.eval_id_list:
            url = f'{self.ip}/pc/gate/homework/homeworkEval/{eval_id}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                data_dic = data_ret['data']
                print(
                    {data_dic['studentName']: f'完成{data_dic["completeCount"]},'
                                              f'正确{data_dic["correctCount"]},'
                                              f'level{data_dic["level"]}'}
                )
            except TypeError:
                print(f'接口"/pc/gate/homework/homeworkEval"报错，返回{data_ret["msg"]}')

    def test_08_homework_eval_challenge(self):
        """
        获取紧急挑战作业完成信息
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homeworkEvalChallenge'
        data = f'pageNum=1&pageSize=12&evalId={self.eval_id_list[0]}&studentId={self.student_id}'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['recordList']['list']
        except TypeError:
            print(f'接口"/pc/gate/homework/homeworkEvalChallenge"报错，返回{data_ret["msg"]}')
        else:
            print([{i['title']: f'结果{i["result"]}'} for i in data_list])

    def test_09_homework_eval_challenge_multi(self):
        """
        获得紧急挑战作业详细完成信息列表,多文本编辑器中
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homeworkEvalChallenge/multi'
        data = f'pageNum=1&pageSize=12&evalId={self.eval_id_list[0]}&userId={self.student_id}'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/homework/homeworkEvalChallenge/multi"报错，返回{data_ret["msg"]}')
        else:
            print([i['title'] for i in data_list])

    def test_10_homework_eval_challenge_multi_record(self):
        """
        获取紧急挑战指定作业详细完成信息,多文本编辑器中
        :return:
        """
        record_id_list = self.student_parm.get_challenge_record_id()
        for record_id in record_id_list:
            url = f'{self.ip}/pc/gate/homework/homeworkEvalChallenge/multi/{record_id}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                data_dic = data_ret['data']
                print({data_dic['problem']['title']: data_dic['result']})
            except TypeError:
                print(f'接口"/pc/gate/homework/homeworkEvalChallenge/multi/record"报错，返回{data_ret["msg"]}')

    def test_11_homework_eval_record(self):
        """
        获得作业详细完成信息列表
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homeworkEvalRecord'
        data = f'pageNum=1&pageSize=12&evalId={self.eval_id_list[0]}' \
               f'&homeworkId={self.homework_id}&studentId={self.student_id}'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/gate/homework/homeworkEvalRecord"报错，返回{data_ret["msg"]}')
        else:
            print([i['title'] for i in data_list])

    def test_12_homework_record_multi(self):
        """
        获得作业详细完成信息列表,多文本编辑器中
        :return:
        """
        url = f'{self.ip}/pc/gate/homework/homeworkEvalRecord/multi'
        data = f'pageNum=1&pageSize=12&evalId={self.eval_id_list[0]}' \
               f'&homeworkId={self.homework_id}&studentId={self.student_id}'
        response = requests.get(url=url, headers=self.teacher_headers,
                                params=data)
        assert_res(response.text)
        data_ret = response.json()
        try:
            print([i['title'] for i in data_ret['data']])
        except TypeError:
            print(f'接口"/pc/gate/homeworkEvalRecord/multi"报错，返回{data_ret["msg"]}')

    def test_13_homework_eval_record(self):
        """
        获取指定作业详细完成信息,多文本编辑器中
        :return:
        """
        record_id_list = self.student_parm.get_record_id_list()
        for record_id in record_id_list:
            url = f'{self.ip}/pc/gate/homework/homeworkEvalRecord/multi/{record_id}'
            response = requests.get(url=url, headers=self.teacher_headers)
            assert_res(response.text)
            time.sleep(1)
            data_ret = response.json()
            try:
                print(data_ret['data']['problem']['title'])
            except TypeError:
                print(f'接口"/pc/gate/homework/homeworkEvalRecord/multi/"报错，返回{data_ret["msg"]}')


if __name__ == "__main__":
    unittest.main()
