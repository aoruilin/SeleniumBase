import unittest

import requests

from interface.K12edu.common.assert_msg import assert_res
from interface.K12edu.common.parameter_for_others import ParameterForOthers


class GrowManageController(unittest.TestCase):
    """成长管理模块"""

    def setUp(self) -> None:
        self.manager_parm = ParameterForOthers(identity='manager')
        self.teacher_parm = ParameterForOthers(identity='teacher')
        self.student_parm = ParameterForOthers(identity='student')
        self.ip = self.teacher_parm.ip
        self.manager_headers = self.manager_parm.headers
        self.teacher_headers = self.teacher_parm.headers
        self.student_headers = self.student_parm.headers

        self.student_id = self.teacher_parm.get_class_student_id()[0]

    def test_01_get_class_average_score(self):
        """
        获取班级信息平均分
        :return:
        """
        url = f'{self.ip}/pc/growManage/getClassAverageScore?' \
              'pageNum=1&pageSize=100&sort=1&sortType=0'
        response = requests.get(url=url, headers=self.manager_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/growManage/getClassAverageScore"报错，返回{data_ret["msg"]}')
        else:
            score_dic = {i['className']: i['studentScore'] for i in data_list}
            print(score_dic)

    def test_02_get_class_detail_score(self):
        """
        获取班级学生详细得分
        :return:
        """
        url = f'{self.ip}/pc/growManage/getClassDetailScore?' \
              'pageNum=1&pageSize=100&sort=1&sortType=0&' \
              f'classId={self.teacher_parm.get_class_list(1)[0]}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/growManage/getClassDetailScore"报错，返回{data_ret["msg"]}')
        else:
            score_dic = {i['nickname']: i['avgScore'] for i in data_list}
            print(score_dic)

    def test_03_get_grow_manage_statistic(self):
        """
        获取成长管理统计
        :return:
        """
        url = f'{self.ip}/pc/growManage/getGrowManageStatistic'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            print([data_ret['data']['knowledgeReserveScore'],
                   data_ret['data']['learnAttitudeScore'],
                   data_ret['data']['learnEffectScore'],
                   data_ret['data']['problemSolvingSkillsScore']])
        except TypeError:
            print(f'接口"/pc/growManage/getGrowManageStatistic"报错，返回{data_ret["msg"]}')

    def test_04_get_person_point_score(self):
        """
        获取知识点得分列表
        :return:
        """
        series_id_list = self.student_parm.get_series_list()
        for series_id in series_id_list:
            url = f'{self.ip}/pc/growManage/getPersonPointScore?seriesId={series_id}'
            response = requests.get(url=url, headers=self.student_headers)
            assert_res(response.text, '操作成功')
            data_ret = response.json()
            try:
                data_list = data_ret['data']
            except TypeError:
                print(f'接口"/pc/growManage/getPersonPointScore"报错，返回{data_ret["msg"]}')
            else:
                data_dic = {
                    i['pointName']: [{
                        s['pointName']: s['personScore'] for s in i['personPointScores']
                    }] for i in data_list
                }
                print(data_dic)

    def test_05_get_person_series_rate(self):
        """
        学生获取比赛能力成长条进度系列
        :return:
        """
        url = f'{self.ip}/pc/growManage/getPersonSeriesRate'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')

    def test_06_get_student_grow_manage_statistic(self):
        """
        老师通过学生Id获取学生成长管理统计
        :return:
        """
        student_id = self.teacher_parm.get_class_student_id()[0]
        url = f'{self.ip}/pc/growManage/getStudentGrowManageStatistic?studentId={student_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            print([data_ret['data']['knowledgeReserveScore'],
                   data_ret['data']['learnAttitudeScore'],
                   data_ret['data']['learnEffectScore'],
                   data_ret['data']['problemSolvingSkillsScore']])
        except TypeError:
            print(f'接口"/pc/growManage/getStudentGrowManageStatistic"报错，返回{data_ret["msg"]}')

    def test_07_get_student_leave_rate(self):
        """
        获取学生的等级比率及吉祥物名称
        :return:
        """
        series_id_list = self.student_parm.get_series_list()
        for series_id in series_id_list:
            url = f'{self.ip}/pc/growManage/getStudentLeaveRate?seriesId={series_id}'
            response = requests.get(url=url, headers=self.student_headers)
            assert_res(response.text, '操作成功')
            data_ret = response.json()
            try:
                print(data_ret['data'])
            except TypeError:
                print(f'接口"/pc/growManage/getStudentLeaveRate"报错，返回{data_ret["msg"]}')

    def test_08_get_student_rank_radio(self):
        """
        获取学生的排名排名比率
        :return:
        """
        url = f'{self.ip}/pc/growManage/getStudentRankRatio'
        response = requests.get(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            print(data_ret['data'])
        except TypeError:
            print(f'接口"/pc/growManage/getStudentRankRatio"报错，返回{data_ret["msg"]}')

    def test_09_get_student_series_rate(self):
        """
        老师通过学生ID获取该学生比赛能力成长条进度系列
        :return:
        """
        url = f'{self.ip}/pc/growManage/getStudentSeriesRate?userId={self.student_id}'
        response = requests.get(url=url, headers=self.teacher_headers)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        print(data_ret['data'])

    def test_10_update_user_mascot_name(self):
        """
        修改用户的吉祥物名称
        :return:
        """
        url = f'{self.ip}/pc/growManage/updateUserMascotName?mascotName=接口修改名称'
        response = requests.post(url=url, headers=self.student_headers)
        assert_res(response.text, '操作成功')

    def test_11_get_student_point_score(self):
        """
        老师通过学生Id获取知识点得分列表
        :return:
        """
        url = f'{self.ip}/pc/growManage/getStudentPointScore'
        params = f'seriesId=1&studentId={self.student_id}'
        response = requests.get(url=url, headers=self.teacher_headers, params=params)
        assert_res(response.text, '操作成功')
        data_ret = response.json()
        try:
            print([{i['pointName']: i['personScore']} for i in data_ret['data']])
        except TypeError:
            print(f'接口/pc/growManage/getStudentPointScore报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)


if __name__ == '__main__':
    unittest.main()
