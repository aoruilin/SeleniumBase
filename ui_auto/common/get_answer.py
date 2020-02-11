import base64
from itertools import chain

import requests

from ui_auto.base.data import Data
from ui_auto.base.data import PointIdIndex
from ui_auto.common.mysql import get_code


class ParameterForOthers:
    def __init__(self, identity=''):
        self.ip = Data().api_ip_for_edu()
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.84 Safari/537.36'
        }
        self.identity = identity
        if not self.identity:
            raise Exception('身份不能为空，请输入 identity="manager"、"teacher"或"student"')
        elif 'manager' == self.identity:
            self.username = Data().manager_username_for_edu()
        elif 'teacher' == self.identity:
            self.username = Data().teacher_username_for_edu()
        elif 'student' == self.identity:
            self.username = Data().student_username_for_edu()
        else:
            raise Exception('错误的身份，请输入 identity="manager"、"teacher"或"student"')
        url = f'{self.ip}/pc/login'
        data = {}
        password = Data().password_for_edu
        data['username'] = self.username
        data['password'] = password
        t = requests.session()
        login_ret = t.post(url=url, headers=self.headers, json=data)
        token = login_ret.json()['data']['token']
        self.headers['token'] = token

    def get_class_list(self, get_all=False):
        """
        提供公用的class_id
        :return:
        """
        url = f'{self.ip}/pc/common/getClassList'
        response = requests.get(url=url, headers=self.headers)
        class_list_ret = response.json()
        data_list = class_list_ret['data']
        data = data_list[0]
        class_id_list = [data_dic['id'] for data_dic in data_list] if get_all else [data['id']]

        return class_id_list

    def get_eval_id(self, traditional_teach=False):
        if traditional_teach:
            url = f'{self.ip}/pc/student/homeworkEval?pageNum=1&pageSize=12'
        else:
            class_list = self.get_class_list(get_all=True)
            class_id = class_list[-1]
            url = f'{self.ip}/pc/gate/homework/student/homeworkEval?pageNum=1&pageSize=4&classId={class_id}'
        response = requests.get(url=url, headers=self.headers)
        homework_list_ret = response.json()
        homework_data_list = homework_list_ret['data']['list']
        eval_id_list = [i['id'] for i in homework_data_list]

        return eval_id_list

    def get_choice_problem_id_for_ui(self, eval_id):
        choice_url = f'{self.ip}/pc/choice/getChoiceListByEvalId?pageNum=1&pageSize=120&evalId={eval_id}&sort=0'
        res = requests.get(url=choice_url, headers=self.headers)
        ret = res.json()
        id_list = ret['data']['list']
        problem_id_list = [(c['id'], c['recordId']) for c in id_list]

        return problem_id_list

    def get_problem_id_for_ui(self, eval_id, traditional_teach=False):
        if traditional_teach:
            url = f'{self.ip}/pc/student/homeworkEvalRecord/multi?pageNum=1&pageSize=150&evalId={eval_id}'
        else:
            url = f'{self.ip}/pc/gate/homework/student/homeworkEvalRecord/multi?pageNum=1&pageSize=120&evalId={eval_id}'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        data_list = data_ret['data']
        all_problem_id_list = [p['problemId'] for p in data_list]
        problem_id_list = [r for r in all_problem_id_list if r is not None]
        # problem_id_list = list(filter(lambda x: is_not(x, None), all_problem_id_list))

        return problem_id_list


# print(ParameterForOthers(identity='student').get_eval_id())
