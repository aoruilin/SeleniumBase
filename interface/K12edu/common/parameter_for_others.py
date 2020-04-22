import time
from operator import is_not

import base64
from itertools import chain

import requests

from ui_auto.base.data import Data
from ui_auto.base.data import PointIdIndex
from ui_auto.common.mysql import get_code


class ParameterForOthers:
    """公共参数"""

    def __init__(self, identity='', username=None):
        d = Data()
        self.ip = d.api_ip_for_edu()
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/68.0.3440.84 Safari/537.36'
        }
        self.identity = identity
        if not self.identity:
            raise Exception('身份不能为空，请输入 identity="manager"、"teacher"或"student"')
        elif 'manager' == self.identity:
            manager_data = d.manager_data()
            self.username = username if username else manager_data['username']
            self.password = manager_data['password']
        elif 'teacher' == self.identity:
            teacher_data = d.teacher_data()
            self.username = username if username else teacher_data['username']
            self.password = teacher_data['password']
        elif 'student' == self.identity:
            student_data = d.student_data()
            self.username = username if username else student_data['username']
            self.password = student_data['password']
        else:
            raise Exception('错误的身份，请输入 identity="manager"、"teacher"或"student"')
        url = f'{self.ip}/user/login'
        data = {
            "password": self.password,
            "username": self.username
        }
        t = requests.Session()
        login_ret = t.post(url=url, headers=self.headers, json=data)
        data_ret = login_ret.json()
        try:
            token = data_ret['data']['token']
        except KeyError:
            print(f'登录失败，返回{data_ret}')
        except TypeError:
            print(f'登录失败，返回{data_ret}')
        else:
            self.headers['token'] = token

    def get_user_school_id(self):
        """
        提供用户id
        :return:
        """
        url = f'{self.ip}/user/userinfo'
        res = requests.get(url=url, headers=self.headers)
        data_ret = res.json()
        try:
            user_id = data_ret['data']['id']
            school_id = data_ret['data']['currentSchool']['id']
            if user_id and school_id:
                return user_id, school_id
            else:
                print(f'{self.username}无法获取user_info')
                return 0, 0
        except TypeError:
            print(f'接口/user/userInfo报错，返回{data_ret["msg"]}')
            return 0, 0
        except KeyError:
            print(data_ret)
            return 0, 0

    def get_school_id_list(self):
        """
        获取用户school_id列表
        :return:
        """
        url = f'{self.ip}/user/userinfo'
        res = requests.get(url=url, headers=self.headers)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['schools']
        except TypeError:
            print(f'接口/user/userInfo报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            school_id_list = [s['id'] for s in data_list]
            return school_id_list

    def get_user_portrait_url_gender(self):
        """
        获取用户头像url
        :return:
        """
        url = f'{self.ip}/user/userinfo'
        res = requests.get(url=url, headers=self.headers)
        data_ret = res.json()
        try:
            return data_ret['data']['portraitUrl'], data_ret['data']['gender']
        except TypeError:
            print(f'接口/user/userInfo报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def get_class_list(self, get_all=False):
        """
        提供公用的class_id
        :return:
        """
        url = f'{self.ip}/common/classes'
        user_id, school_id = self.get_user_school_id()
        params = f'userId={user_id}&schoolId={school_id}'
        response = requests.get(url=url, headers=self.headers, params=params)
        class_list_ret = response.json()
        try:
            data_list = class_list_ret['data']
            data = data_list[-1]
        except TypeError:
            msg = '接口正常，没有数据' \
                if class_list_ret['msg'] == '操作成功' else \
                f'接口/common/classes报错，返回{class_list_ret["msg"]}'
            print(msg)
        except KeyError:
            print(f'接口/common/classes返回{class_list_ret}')
        else:
            class_id_list = [data_dic['id'] for data_dic in data_list] if get_all else [data['id']]
            return class_id_list

    def get_manage_teacher_list(self):
        """
        管理员获取教师管理列表
        :return:
        """
        _, school_id = self.get_user_school_id()
        url = f'{self.ip}/teachcenter/teachermanage/list'
        data = {
            "currPage": 1,
            "keyword": '',
            "pageSize": 50,
            "schoolId": school_id,
            "tchType": 1
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/teachcenter/teachermanage/list报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/teachcenter/teachermanage/list返回{data_ret}')
        else:
            teacher_id_list = [i['tchId'] for i in data_list]
            return teacher_id_list

    def get_manage_class_list(self, school_id):
        """
        管理员获取管理班级列表
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/list'
        data = {
            "classType": 1,
            "currPage": 1,
            "keyword": "",
            "pageSize": 100,
            "schoolId": school_id
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/teachcenter/classmanage/list"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/teachcenter/classmanage/list"返回{data_ret}')
        else:
            return [i['classId'] for i in data_list]

    def get_class_student_id(self, class_id, school_id):
        """
        获取班级管理中一个班的学生的userID
        :return:
        """
        url = f'{self.ip}/teachcenter/classmanage/stuList'
        data = {
            "classId": class_id,
            "currPage": 1,
            "keyword": "",
            "pageSize": 50,
            "schoolId": school_id
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        student_list_ret = res.json()
        try:
            data_list = student_list_ret['data']['list']
        except TypeError:
            print(f'接口/teachcenter/classmanage/stuList报错，返回{student_list_ret["msg"]}')
        except KeyError:
            print(f'接口/teachcenter/classmanage/stuList返回{student_list_ret}')
        else:
            student_id_list = [data_dic['stuId'] for data_dic in data_list]
            return student_id_list

    def get_my_manage_students(self):  # 没改
        """
        获取管理员管理的学生列表
        :return:
        """
        url = f'{self.ip}/pc/class/getMyManageStudList?pageNum=1&pageSize=50&desc=0&allFlg=0'
        res = requests.get(url=url, headers=self.headers)
        ret_dic = res.json()
        try:
            student_list = ret_dic['data']['list']
        except TypeError:
            print(f'接口/pc/class/getMyManageStudList报错，返回{ret_dic["msg"]}')
        except KeyError:
            print(f'接口/pc/class/getMyManageStudList返回{ret_dic}')
        else:
            student_id_list = [data_dic['userId'] for data_dic in student_list]
            return student_id_list

    def get_point_id(self, series=1):
        """
        提供公用的pointId
        :return:
        """
        url = f'{self.ip}/common/points/{series}'
        response = requests.get(url=url, headers=self.headers)
        point_list_ret = response.json()
        try:
            data_list = point_list_ret['data']
        except KeyError:
            print(f'接口/common/points返回{point_list_ret}')
        else:
            try:
                problem_dic = data_list[PointIdIndex.level_two_index]  # S1二级列表
                problem_list = problem_dic['children']
                id_list = [i['id'] for i in problem_list]
                point_id_for_homework = id_list[PointIdIndex.level_three_index]
                point_id_for_course = id_list[PointIdIndex.level_three_index]
                return point_id_for_homework, point_id_for_course
            except IndexError:
                print(f'没有指定的知识点', data_list)
            except TypeError:
                print(f'接口/pc/common/getPointList报错，返回{point_list_ret["msg"]}')

    def get_all_point_resource_id(self, series_id):
        """
        获取一个系列所有的pointID
        :param series_id:
        :return:
        """
        from operator import is_not

        url = f'{self.ip}/common/points/{series_id}'
        response = requests.get(url=url, headers=self.headers)
        point_list_ret = response.json()
        try:
            data_list = point_list_ret['data']
            id_list = [data_dic['children'] for data_dic in data_list]
        except TypeError:
            print(f'接口common/points报错，返回{point_list_ret["msg"]}', series_id)
        except KeyError:
            print(f'接口common/points返回{point_list_ret}')
        else:
            point_id_list = [[{'id': c['id'], 'resource_id': c['resourceId']}
                              for c in child_id_list] for child_id_list in id_list]
            all_id_list = list(chain(*point_id_list))
            return list(filter(lambda x: is_not(x['resource_id'], None), all_id_list))

    def get_point_id_checkpoint(self, get_all=False):  # 没改
        """
        闯关授课pointID
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getGateListBySeriesId?seriesId=1'
        response = requests.get(url=url, headers=self.headers)
        point_list_ret = response.json()
        try:
            data_list = point_list_ret['data']
        except KeyError:
            print(point_list_ret)
        else:
            if get_all:
                try:
                    gate_point_id_list = [{'gate_id': i['id'], 'point_id': i['dimPoint']['id']} for i in data_list]
                    return gate_point_id_list
                except TypeError:
                    print(f'接口"/pc/gate/common/getGateListBySeriesId"报错，返回{point_list_ret["msg"]}')
            else:
                try:
                    gate_dic = data_list[PointIdIndex.checkpoint_level_two_index]
                    gate_point_id_dic = {'gate_id': gate_dic['id'], 'point_id': gate_dic['dimPoint']['id']}
                    return gate_point_id_dic
                except TypeError:
                    print(f'接口"/pc/gate/common/getGateListBySeriesId"报错，返回{point_list_ret["msg"]}')

    def get_all_point_id_checkpoint(self, series_id):  # 没改
        """
        获取闯关授课所有的知识点pointID
        :param series_id: S系列
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getGateListBySeriesId?seriesId={series_id}'
        res = requests.get(url=url, headers=self.headers)
        res_ret = res.json()
        try:
            data_list = res_ret['data']
            dim_list = [data_dic['dimPoint'] for data_dic in data_list]
            gate_point_id_list = [dim_dic['id'] for dim_dic in dim_list]
            return gate_point_id_list
        except TypeError:
            print(f'接口"/pc/gate/common/getGateListBySeriesId"报错，返回{res_ret["msg"]}')
        except KeyError:
            print(res_ret)

    def get_gate_practise_id_list(self, gate_id, class_id):  # 没改
        """
        获取关卡练习题的题目id
        :param gate_id:关卡id
        :param class_id:班级id
        :return:
        """
        url = f'{self.ip}/pc/gate/common/getGatePractiseList' \
              f'?gateId={gate_id}&classId={class_id}'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            practise_id_list = [i['practiseId'] for i in data_ret['data']]
            practise_title_list = [i['title'] for i in data_ret['data']]
            return practise_id_list, practise_title_list
        except TypeError:
            print(f'接口"/pc/gate/common/getGatePractiseList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def get_user_course_list(self, class_id=None, series_id=None):
        """
        获取课程列表
        :param class_id:要获取的班级的id
        :param series_id:系列id
        :return:
        """
        url = f'{self.ip}/course/user/courses'
        data = {
            "classId": class_id,
            # "flag": 0,
            "pageNum": 1,
            "pageSize": 12,
            "seriesId": series_id
        }
        response = requests.post(url=url, headers=self.headers, json=data)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/course/user/courses"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/course/user/courses"返回{data_ret}')
        else:
            course_id_list = [i['id'] for i in data_list]
            return course_id_list

    def get_student_customs_course_list(self, class_id):  # 没改
        """
        学生获取主题授课的课件列表
        :param class_id: 要获取的班级的id
        :return:
        """
        url = f'{self.ip}/pc/gate/course/student/getStudentCustomsCourseList' \
              f'?pageNum=1&pageSize=6&status=1&sort=0&classId={class_id}'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print('接口"/pc/gate/course/student/getStudentCustomsCourseList"报错，'
                  f'返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            course_id_list = [i['id'] for i in data_list]
            return course_id_list

    def teacher_get_homework_problem_id_list(self):
        """
        老师获取单个作业题目列表
        :return:
        """
        url = f'{self.ip}/homework/tchHwAnsProblemList'
        homework_id_list = self.get_homework_id_list(teacher=True)
        if homework_id_list:
            data = {
                "hwId": homework_id_list[0]
            }
            res = requests.post(url=url, headers=self.headers, json=data)
            data_ret = res.json()
            try:
                return [(i['problemId'], i['problemType']) for i in data_ret['data']]
            except TypeError:
                print(f'接口"/homework/tchHwAnsProblemList"报错，返回{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/homework/tchHwAnsProblemList"返回{data_ret}')
        else:
            print('这个账号没有发过作业')

    def get_problem_id(self, point_id, subject_type, p_type=None, difficulty_list=None):
        """
        提供公用的problemId
        :param point_id: 知识点
        :param subject_type: 1-选择题，2-操作题
        :param p_type: 1-课程，2-作业
        :param difficulty_list: 难度 1-简单，2-中等，3-困难 -> 不用带这个，用作预留
        :return:
        """
        url = f'{self.ip}/common/subjects'
        data = {
            "pointId": point_id,
            "types": [
                p_type
            ]
        }
        response = requests.post(url=url, headers=self.headers, json=data)
        data_ret = response.json()
        try:
            data_list = data_ret['data']
            if subject_type == 1:  # 选择题
                return [i['id'] for i in data_list if i['subjectType'] == 1]
            else:  # 操作题
                return [i['id'] for i in data_list if i['subjectType'] == 2]
        except TypeError:
            print(f'接口"/common/subjects"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/common/subjects"返回{data_ret}')

    def get_all_problem_id(self, point_id, check_point=False):  # 没改
        """
        获得一个知识点所有题目的problemID
        :param point_id:
        :param check_point: 是否是主题授课
        :return:
        """
        all_list = []
        for d in range(1, 4):
            url = f'{self.ip}/pc/problem?klPoints={point_id}&pageNum=1&pageSize=50&difficulty={d}' \
                if check_point else f'{self.ip}/pc/problem?klPoints={point_id}&pageNum=1&pageSize=50&difficulty={d}'
            res = requests.get(url=url, headers=self.headers)
            data_ret = res.json()
            try:
                data_list = data_ret['data']['list']
            except TypeError:
                print(f'接口"/pc/problem"报错，返回{data_ret["msg"]}', f'pointId:{point_id}')
            except KeyError:
                print(data_ret)
            else:
                problem_id_list = [d['id'] for d in data_list]
                all_list.append(problem_id_list)
        all_problem_id_list = list(chain(*all_list))

        return all_problem_id_list

    def get_choice_problem_id(self):  # 没改
        """
        选择题的problem id
        :return:
        """
        point_id = self.get_point_id()
        url = f'{self.ip}/pc/choice/list?klPoints={point_id}&pageNum=1&pageSize=12&difficulty=1'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            problem_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/choice/list"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            problem_id_list = [d['id'] for d in problem_list]
            return problem_id_list

    def get_all_choice_problem_id(self, point_id):  # 没改
        """
        获取一个知识点全部选择题problemID
        :param point_id:
        :return:
        """
        url = f'{self.ip}/pc/choice/list?klPoints={point_id}&pageNum=1&pageSize=12'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            problem_list = data_ret['data']['list']
        except TypeError:
            print(f'接口“/pc/choice/list”报错：{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            problem_id_list = [d['id'] for d in problem_list]
            return problem_id_list

    def get_eval_id(self, traditional_teach=False):  # 没改
        if traditional_teach:
            url = f'{self.ip}/pc/student/homeworkEval?pageNum=1&pageSize=12'
        else:
            class_list = self.get_class_list(get_all=True)
            class_id = class_list[-1]
            url = f'{self.ip}/pc/gate/homework/student/homeworkEval?pageNum=1&pageSize=4&classId={class_id}'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            homework_data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口“homeworkEval”报错：{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            eval_id_list = [i['id'] for i in homework_data_list]
            return eval_id_list

    def get_resource_plan_id(self, standard=False):  # 没改
        """
        提供公用的resourcePlanId
        :param standard: True-标准授课，False-主题授课
        :return:
        """
        if standard:
            resource_type = 0
        else:
            resource_type = 1
        point_id_tup = self.get_point_id()
        point_id = point_id_tup[1]
        url = f'{self.ip}/pc/course/getResourcePlanList?' \
              f'resourceType={resource_type}&pointId={point_id}&pageNum=1&pageSize=4'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/course/getResourcePlanList"报错：{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            resource_id_list = [r['id'] for r in data_list]
            return resource_id_list

    def get_series_list(self, module_type=1):
        """
        获取所有系列seriesID
        :param module_type: 1-课程，2-作业，默认获取课程
        :return:
        """
        url = f'{self.ip}/common/series'
        _, school_id = self.get_user_school_id()
        data = {
            "schoolId": school_id,
            "seriesType": 0,
            "moduleType": module_type
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']
            series_list = [i['id'] for i in data_list]
        except TypeError:
            print(f'接口"/common/series：{data_ret["msg"]}')
        except KeyError:
            print(f'接口/common/series，返回{data_ret},与预期不符')
        else:
            return series_list

    def get_series_resource_plan_id(self, series):  # 没改
        """
        获取一个系列下所有的resourcePlanId
        :return:
        """
        url = f'{self.ip}/pc/resource/getResourcePlanList?' \
              f'pageNum=1&pageSize=150&resourceType=0&seriesId={series}&keyword='
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/resource/getResourcePlanList"报错：{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            resource_id_list = [r['resourceId'] for r in data_list]
            return resource_id_list

    def teacher_get_hw_student_num(self):
        """
        教师获取作业的学生学号
        :return:
        """
        url = f'{self.ip}/homework/tchHwStuList'
        data = {
            "currPage": 1,
            "hwId": self.get_homework_id_list(teacher=True)[0],
            "pageSize": 30
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/homework/tchHwStuList"报错：{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwStuList"返回{data_ret}')
        else:
            return [i['studentNo'] for i in data_list]

    def student_get_problem_id_list(self):
        """
        学生获取作业题目id
        :return:
        """
        url = f'{self.ip}/homework/stuHwProblemList'
        homework_id_list = self.get_homework_id_list()
        if homework_id_list:
            data = {
                "hwId": self.get_homework_id_list()[0]  # 第一个作业
            }
            res = requests.post(url=url, headers=self.headers, json=data)
            data_ret = res.json()
            try:
                # problem_type = 1 if choice else 2
                return [(i['problemId'], i['problemType'])
                        for i in data_ret['data']]  # if i['problemType'] == problem_type]
            except TypeError:
                print(f'接口"/homework/stuHwProblemList"报错：{data_ret["msg"]}')
            except KeyError:
                print(f'接口"/homework/stuHwProblemList"返回{data_ret}')
        else:
            print('这个学生没有收到过作业')

    def teacher_get_student_eval_id_list(self):
        """
        获取学生evalId
        :return:
        """
        url = f'{self.ip}/homework/tchHwStuList'
        data = {
            "currPage": 1,
            "hwId": self.get_homework_id_list(teacher=True)[0],
            "pageSize": 30
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/homework/tchHwStuList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口"/homework/tchHwStuList"返回{data_ret}')
        else:
            return [i['studentEvalId'] for i in data_list]

    def get_choice_problem_id_for_ui(self, eval_id):  # 没改
        choice_url = f'{self.ip}/pc/choice/getChoiceListByEvalId?pageNum=1&pageSize=120&evalId={eval_id}&sort=0'
        res = requests.get(url=choice_url, headers=self.headers)
        data_ret = res.json()
        try:
            id_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/choice/getChoiceListByEvalId"报错：{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            problem_id_list = [(c['id'], c['recordId']) for c in id_list]
            return problem_id_list

    def get_problem_id_for_ui(self, eval_id, traditional_teach=False):  # 没改
        if traditional_teach:
            url = f'{self.ip}/pc/student/homeworkEvalRecord/multi?pageNum=1&pageSize=150&evalId={eval_id}'
        else:
            url = f'{self.ip}/pc/gate/homework/student/homeworkEvalRecord/multi?pageNum=1&pageSize=120&evalId={eval_id}'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']
            all_problem_id_list = [p['problemId'] for p in data_list]
            problem_id_list = [r for r in all_problem_id_list if r is not None]
            # problem_id_list = list(filter(lambda x: is_not(x, None), all_problem_id_list))
            return problem_id_list
        except TypeError:
            print(f'接口"homeworkEvalRecord"报错：{data_ret["msg"]}')
        except KeyError:
            print(data_ret)

    def get_ojcode_for_ord(self, eval_id, traditional_teach=False):  # 没改
        problem_id_list = self.get_problem_id_for_ui(eval_id, traditional_teach=traditional_teach)
        ojcode_list = []

        for problem_id in problem_id_list:
            ojcode = []
            file_dic = {"fileName": "main.py", "fileType": 1, "rwType": 1, "sort": 0}
            code = get_code(problem_id=problem_id, problem_name=None)
            b_code = base64.b64encode(code.encode('utf-8'))
            s_code = str(b_code)[2:-1]
            file_dic['fileContent'] = s_code
            ojcode.append(file_dic)
            ojcode_list.append(ojcode)
        return problem_id_list, ojcode_list

    @staticmethod
    def get_ojcode_for_cha(problem_id):  # 没改
        ojcode = []
        file_dic = {"fileName": "main.py", "fileType": 1, "rwType": 1, "sort": 0}
        code = get_code(problem_id=problem_id, problem_name=None)
        b_code = base64.b64encode(code.encode('utf-8'))
        s_code = str(b_code)[2:-1]
        file_dic['fileContent'] = s_code
        ojcode.append(file_dic)

        return ojcode

    def get_gate_teacher_homework_id(self):  # 没改
        """获得老师发布的主题授课homeworkID"""
        url = f'{self.ip}/pc/gate/homework/tchHomeworkList'
        data = f'pageNum=1&pageSize=50&status=0&classId={self.get_class_list()[0]}&allFlg=1'
        res = requests.get(url=url, headers=self.headers, params=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/pc/gate/homework/tchHomeworkList报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            return [i['id'] for i in data_list]

    def get_gate_student_homework_id(self):  # 没改
        """获取学生主题授课homeworkID"""
        url = f'{self.ip}/pc/gate/homework/student/homeworkEval'
        data = f'pageNum=1&pageSize=50&classId={self.get_class_list()[0]}'
        res = requests.get(url=url, headers=self.headers, params=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/pc/gate/homework/student/homeworkEval报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            return [i['id'] for i in data_list]

    def get_homework_id_list(self, teacher=False):
        url = f'{self.ip}/homework/tchHwList' if teacher else f'{self.ip}/homework/stuHwList'
        class_id_index = -1 if teacher else 0
        _, school_id = self.get_user_school_id()
        data = {
            "classId": '',
            "currPage": 1,
            "homeworkName": "",
            "pageSize": 30,
            "schoolId": school_id,
            "status": ''
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/homework/stuHwList报错，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/homework/stuHwList返回{data_ret}')
        else:
            return [i['homeworkId'] for i in data_list]

    def get_record_id_list(self, traditional_teach=False):  # 没改
        """
        获取单个作业的recorId列表
        :param traditional_teach: 是否为标准授课
        :return:
        """
        url = f'{self.ip}/pc/student/homeworkEvalRecord' \
            if traditional_teach else \
            f'{self.ip}/pc/gate/homework/student/homeworkEvalRecord'
        eval_id_list = self.get_eval_id(traditional_teach=True) \
            if traditional_teach else self.get_eval_id()
        data = f'pageNum=1&pageSize=50&evalId={eval_id_list[0]}'
        response = requests.get(url=url, headers=self.headers,
                                params=data)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口homeworkEvalRecord报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            return [i['recordId'] for i in data_list]

    def get_challenge_record_id(self, traditional_teach=False):  # 没改
        """
        获取紧急挑战题目recordID
        :return:
        """
        url = f'{self.ip}/pc/student/homeworkEvalChallenge' \
            if traditional_teach else \
            f'{self.ip}/pc/gate/homework/student/homeworkEvalChallenge'
        eval_id_list = self.get_eval_id(traditional_teach=True) \
            if traditional_teach else self.get_eval_id()
        data = f'pageNum=1&pageSize=50&evalId={eval_id_list[0]}'
        response = requests.get(url=url, headers=self.headers,
                                params=data)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['recordList']['list']
        except TypeError:
            print(f'接口homeworkEvalRecord报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            return [i['recordId'] for i in data_list]

    def get_challenge_record_id_list(self, traditional_teach=False):  # 没改
        """
        获取单个作业的紧急挑战recordId列表
        :param traditional_teach: 是否为标准授课
        :return:
        """
        url = f'{self.ip}/pc/student/homeworkEvalChallenge' \
            if traditional_teach else \
            f'{self.ip}/pc/gate/homework/student/homeworkEvalChallenge'
        eval_id_list = self.get_eval_id(traditional_teach=True) \
            if traditional_teach else self.get_eval_id()
        data = f'pageNum=1&pageSize=50&evalId={eval_id_list[0]}'
        response = requests.get(url=url, headers=self.headers,
                                params=data)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['recordList']['list']
        except TypeError:
            print(f'接口homeworkEvalRecord报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            return [i['recordId'] for i in data_list]

    def get_teacher_id(self):  # 没改
        """
        获取学生提交作品选择老师的teacherID
        :return:
        """
        url = f'{self.ip}/pc/worksDisplay/getTeacherListByClassId'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']
            teacher_info = data_list[0]
            user_list = teacher_info['userList']
            user = user_list[0]
            teacher_id = user['id']
            return teacher_id
        except TypeError:
            print(f'接口/pc/worksDisplay/getTeacherListByClassId报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        except IndexError:
            print(data_ret)

    def get_draft_id_list(self):  # 没改
        """
        用户获取草稿列表
        :return:
        """
        url = f'{self.ip[:-8]}/ddc-port/play/getDraftList'
        params = 'pageNum=1&pageSize=6'
        response = requests.get(url=url, headers=self.headers, params=params)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/play/getDraftList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            draft_id_list = [i['id'] for i in data_list]
            return draft_id_list

    def get_work_id(self):  # 没改
        """
        提供待教师审核的作品ID
        :return:
        """
        url = f'{self.ip}/pc/worksDisplay/getMyWorksList?status=2&pageNum=1&pageSize=15&sort=0&keyword='
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
            work_id_list = []
            first_work = data_list[0]
            first_work_id = first_work['id']
            second_work = data_list[1]
            second_work_id = second_work['id']
        except TypeError:
            print(f'接口"/pc/worksDisplay/getMyWorksList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        except IndexError:
            print('没有数据', data_ret)
        else:
            work_id_list.append(first_work_id)
            work_id_list.append(second_work_id)
            return work_id_list

    def get_work_id_list(self):
        """
        提供学生作品id列表
        :return:
        """
        url = f'{self.ip}/play/getMyWorksList?pageNum=1&pageSize=30'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/pc/play/getMyWorksList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            work_id_list = [i['id'] for i in data_list]
            return work_id_list

    def get_category_list(self):  # 没改
        """
        提供试炼场素材库分类id列表
        :return:
        """
        url = f'{self.ip[:-8]}/ddc-port/play/getSucaiCategoryList'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['个人素材']
        except TypeError:
            print(f'接口"/play/getSucaiCategoryList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            id_list = [i['id'] for i in data_list]
            return id_list

    def get_sucai_url(self):  # 没改
        """
        获取上传的密钥，返回资源链接的路径
        :return:
        """
        url = f'{self.ip[:-8]}/ddc-port/common/getGipher'
        data = {
            'key': 'zsyl@oss888',
            'type': 'sucai'
        }
        response = requests.post(url=url, headers=self.headers, json=data)
        data_ret = response.json()
        try:
            bucket_name = data_ret['data']['bucketName']
            role_path = data_ret['data']['rolePath']
        except TypeError:
            print(f'接口"/pc/common/getGipher"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            image_url = f'https://{bucket_name}.file.myqcloud.com/' \
                        f'{role_path}{time.strftime("%Y%m%d")}/'
            return image_url

    def get_image_id_list(self, category_id):  # 没改
        """
        提供素材库图片id列表
        :param category_id: 素材分类id
        :return:
        """
        url = f'{self.ip[:-8]}/ddc-port/play/getImageFileList?categoryId={category_id}&pageSize=50&pageNum=1'
        response = requests.get(url=url, headers=self.headers)
        data_ret = response.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口"/play/getImageFileList"报错，返回{data_ret["msg"]}')
        except KeyError:
            print(data_ret)
        else:
            id_list = [i['id'] for i in data_list]
            return id_list

    def get_msg_id_list(self):
        """
        提供用户msg_id列表
        :return:
        """
        url = f'{self.ip}/index/user/messages'
        data = {
            "pageNum": 1,
            "pageSize": 10
        }
        res = requests.post(url=url, headers=self.headers, json=data)
        data_ret = res.json()
        try:
            data_list = data_ret['data']['list']
        except TypeError:
            print(f'接口/index/user/messages，返回{data_ret["msg"]}')
        except KeyError:
            print(f'接口/index/user/messages，返回{data_ret},与预期不符')
        else:
            return [i['id'] for i in data_list]

# print(ParameterForOthers(identity='teacher').get_all_point_resource_id(1))
# print(ParameterForOthers(identity='student').student_get_problem_id_list())
# p = ParameterForOthers(identity='teacher')
# print(p.__dict__)
# print(p.__doc__)
# print(p.__module__)
# import pprint
#
# pprint.pprint(p.__class__.__dict__)
