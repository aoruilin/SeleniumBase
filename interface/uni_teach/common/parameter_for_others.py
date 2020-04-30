import requests

from base.data import Data
from base.data import PointIdIndex


class ParameterForOthers:
    def __init__(self, identity=''):
        self.ip = Data().api_ip_for_uni_teach()
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.84 Safari/537.36'
        }
        self.identity = identity
        if not self.identity:
            raise Exception('身份不能为空，请输入 identity="manager"、"teacher"或"student"')
        elif 'manager' == self.identity:
            self.username = Data().manager_username_for_uni_teach()
        elif 'teacher' == self.identity:
            self.username = Data().teacher_username_for_uni_teach()
        elif 'student' == self.identity:
            self.username = Data().student_username_for_uni_teach()
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

    def get_class_list(self):
        url = f'{self.ip}/pc/common/getClassList'
        response = requests.get(url=url, headers=self.headers)
        class_list_ret = response.json()
        data_dic = class_list_ret['data']
        data = data_dic[0]
        class_id_list = []
        class_id = data['id']
        class_id_list.append(class_id)
        return class_id_list

    def get_point_id(self):
        url = f'{self.ip}/pc/common/getPointList?seriesId=1'
        response = requests.get(url=url, headers=self.headers)
        point_list_ret = response.json()
        data_list = point_list_ret['data']
        problem_dic = data_list[PointIdIndex.level_two_index]
        problem_list = problem_dic['list']
        id_list = []
        for i in problem_list:
            point_id = i['id']
            id_list.append(point_id)
        point_id_for_homework = id_list[PointIdIndex.level_three_index]
        point_id_for_course = id_list[PointIdIndex.level_three_index]
        return point_id_for_homework, point_id_for_course

    def teach_get_problem_id(self):
        point_id = self.get_point_id()
        url = f'{self.ip}/pc/problem?klPoints={point_id}&pageNum=1&pageSize=12&difficulty=1'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        data = data_ret['data']
        problem_list = data['list']
        problem_id_list = []
        for d in problem_list:
            problem_id = d['id']
            problem_id_list.append(problem_id)
        return problem_id_list

    def get_resource_plan_id(self, standard=True):
        if standard:
            resource_type = 0
        else:
            resource_type = 1
        point_id = self.get_point_id()
        url = f'{self.ip}/pc/course/getResourcePlanList?' \
            f'resourceType={resource_type}&pointId={point_id[0]}&pageNum=1&pageSize=4'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        data = data_ret['data']
        data_list = data['list']
        resource_plan_id_list = []
        for r in data_list:
            resource_plan_id = r['id']
            resource_plan_id_list.append(resource_plan_id)
        return resource_plan_id_list


# print(ParameterForOthers('teacher').get_resource_plan_id())
