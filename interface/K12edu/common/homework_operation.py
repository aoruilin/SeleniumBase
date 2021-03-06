import base64
import time
import requests
from itertools import chain

from interface.common.time_parameter import time_stamp
from interface.K12edu.common.assert_msg import assert_res
from ui_auto.common.mysql import get_choice, get_code
from ui_auto.common.get_cwd import get_absolute_path


def add_homework(parameter, hw_name, series_id, point_id_list,
                 show_answer, show_difficulty, timing, difficulty_list=None):
    """
    老师发布作业
    :param parameter: 参数对象
    :param hw_name: 作业名称
    :param series_id: 系列id
    :param point_id_list: 知识点列表
    :param show_answer: 显示答案 0-不公布 1-公布
    :param show_difficulty: 显示难度 0-不显示 1-显示
    :param timing: 定时发布 0-立即发布 1-不定时
    :param difficulty_list: 题目难度 1-简单，2-中等，3-困难 -> 不用带这个，用作预留
    :return:
    """
    url = f'{parameter.ip}/homework/tchHwPost'
    all_choice_id = []
    all_programme_id = []
    for point_id in point_id_list:
        problem_id_list = parameter.get_problem_id(point_id, 2, 2)
        problem_id_dic = [
            {
                'pointId': point_id,
                'subjectId': problem_id
            } for problem_id in problem_id_list
        ]
        choice_id_list = parameter.get_problem_id(point_id, 1, 2)
        choice_id_dic = [
            {
                'pointId': point_id,
                'subjectId': choice_id
            } for choice_id in choice_id_list
        ]
        if problem_id_list:
            all_programme_id.append(problem_id_dic)
        if choice_id_list:
            all_choice_id.append(choice_id_dic)
    all_choice_id_list, all_programme_id_list = list(chain(*all_choice_id)), list(chain(*all_programme_id))
    data = {
        "choices": all_choice_id_list[:25],
        "classIds": parameter.get_class_list(),
        "endTime": time_stamp(end=True),
        "hwName": hw_name,
        "programmes": all_programme_id_list[:25],
        "seriesId": series_id,
        "showAnswer": show_answer,
        "showDifficulty": show_difficulty,
        "timingPost": timing,
    }
    if timing == 1:
        data['timingPostTime'] = time_stamp(start=True)
    res = requests.post(url=url, headers=parameter.headers, json=data)
    assert_res(res.text)
    data_ret = res.json()
    success_msg = None
    try:
        success_msg = data_ret['data']['msg']
        print(data_ret['data']['success'])
        return data_ret['data']['success']
    except AssertionError:
        print(f'提示断言失败，发布作业提示“{success_msg}”')
        return False
    except TypeError:
        print(f'接口“/homework/tchHwPost”报错，返回{data_ret["msg"]}')
        return False
    except KeyError:
        print(f'接口“/homework/tchHwPost”返回{data_ret}')
        return False


def oj_data(problem_id, problem_type, homework_id=None, class_id=None, course_id=None, point_id=None, practice=False):
    answer = get_choice(problem_id=problem_id, problem_name=None) if problem_type == 1 \
        else base64.b64encode(get_code(problem_id=problem_id, problem_name=None).encode('u8')).decode('u8')
    data = {
        "classId": class_id,
        "courseId": course_id,
        "picContentError": "",
        "picEncryptContent": "",
        "pointId": point_id,
        "subjectId": problem_id,
        "subjectType": problem_type,
        "userAnswer": answer
    } if practice else {
        "hwId": homework_id.__str__(),
        "picContentError": "",
        "picEncryptContent": "",
        "subjectId": problem_id,
        "subjectType": problem_type,
        "userAnswer": answer
    }
    turtle_img = __base64_img(problem_id)
    if turtle_img:
        data['picEncryptContent'] = f'data:image/png;base64,{turtle_img}'
    return data


def do_homework_simple(parameter, cut_num=None, homework_num=1):
    url = f'{parameter.ip}/homework/stuHwProblemOj'
    homework_id_list = parameter.get_homework_id_list()
    for n in range(homework_num):  # 做前几个作业
        homework_id = homework_id_list[n]
        __add_homework_eval(parameter, homework_id)
        problem_id_list = parameter.student_get_problem_id_list()[:cut_num] \
            if cut_num else parameter.student_get_problem_id_list()
        for p, c in problem_id_list:
            data = oj_data(p, c, homework_id)
            response = requests.post(url=url, headers=parameter.headers, json=data)
            ret = response.json()
            __assert_code_result(ret, p, c)
            time.sleep(1.5)
        # 提交作业
        commit_url = f'{parameter.ip}/homework/stuHwSubmit'
        commit_data = {
            "hwId": homework_id.__str__()
        }
        commit_res = requests.post(url=commit_url, headers=parameter.headers, json=commit_data)
        assert_res(commit_res.text)
        time.sleep(1)


def student_do_practice(parameter, class_id, course_id, point_id, subject_id_list) -> list:
    url = f'{parameter.ip}/course/student/evalAndSave/record'
    result_list = []
    for p_id, p_type in subject_id_list:
        data = oj_data(p_id, p_type, class_id=class_id, course_id=course_id, point_id=point_id, practice=True)
        res = requests.post(url=url, headers=parameter.headers, json=data)
        data_ret = res.json()
        result = data_ret['data']['result']
        out_put = '正确' if result == 1 else '错误'
        result_list.append((p_id, out_put))
    return result_list


def __base64_img(problem_id):
    try:
        project_cwd = get_absolute_path('interface')
        with open(f'{project_cwd}\\base\\turtle_problem_code\\{problem_id}.png', 'rb') as f:
            base64_data = base64.b64encode(f.read())
    except FileNotFoundError:
        return False
    else:
        s = base64.b64encode(base64_data)
        b_string = base64.b64decode(s).decode('u8')
        return b_string


def __add_homework_eval(parameter, hw_id):
    """
    学生激活作业
    :param parameter: 参数对象
    :param hw_id: 作业id
    :return:
    """
    url = f'{parameter.ip}/homework/stuHwAddEval'
    data = {
        "hwId": hw_id
    }
    res = requests.post(url=url, headers=parameter.headers, json=data)
    assert_res(res.text)


def __assert_code_result(ret, problem_id, problem_type):
    if 1 == problem_type:
        try:
            assert ('操作成功' == ret['msg'])
        except AssertionError as a:
            print(a, ret['msg'], f'题号{problem_id}')
        except KeyError:
            print(f'评测接口报错,返回{ret}')
    else:  # 待定
        try:
            out = ret['data']['problemStatus']
            assert (1 == out)
        except TypeError:
            print(f'操作题评测接口报错，返回{ret["msg"]}', problem_id)
        except AssertionError as a:
            print(a, f'题号{problem_id}')
        except BaseException as e:
            print(e, f'题号{problem_id}')
