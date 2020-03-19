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
        problem_id_list = parameter.get_problem_id(point_id, 2)
        choice_id_list = parameter.get_problem_id(point_id, 1)
        if problem_id_list:
            all_programme_id.append(problem_id_list)
        if choice_id_list:
            all_choice_id.append(choice_id_list)
    all_choice_id_list, all_programme_id_list = list(chain(*all_choice_id)), list(chain(*all_programme_id))
    data = {
        "choiceIds": all_choice_id_list,
        "classIds": parameter.get_class_list(),
        "endTime": time_stamp(end=True),
        "hwName": hw_name,
        "programmeIds": all_programme_id_list,
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
        # assert ('' == success_msg)
    except AssertionError:
        print(f'提示断言失败，发布作业提示“{success_msg}”')
    except TypeError:
        print(f'接口“/homework/tchHwPost”报错，返回{data_ret["msg"]}')
    except KeyError:
        print(f'接口“/homework/tchHwPost”返回{data_ret}')


def oj_data(problem_id, problem_type, homework_id):
    answer = get_choice(problem_id=problem_id, problem_name=None) if problem_type == 1 \
        else base64.b64encode(get_code(problem_id=problem_id, problem_name=None).encode('u8')).decode('u8')
    data = {
        "hwId": homework_id,
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
        problem_id_list = parameter.student_get_problem_id_list()[:cut_num] \
            if cut_num else parameter.student_get_problem_id_list()
        for p, c in problem_id_list:
            data = oj_data(p, c, homework_id)
            response = requests.post(url=url, headers=parameter.headers, json=data)
            ret = response.json()
            __assert_code_result(ret, p, c)
            time.sleep(1)
        # 提交作业
        commit_url = f'{parameter.ip}/homework/stuHwSubmit'
        commit_data = {
            "hwId": homework_id
        }
        commit_res = requests.post(url=commit_url, headers=parameter.headers, json=commit_data)
        assert_res(commit_res.text)
        commit_ret = commit_res.json()
        print(commit_ret['data']['success'])
        time.sleep(1)


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
            print(f'紧急挑战评测接口报错，返回{ret["msg"]}', problem_id)
        except AssertionError as a:
            print(a, f'题号{problem_id}')
        except BaseException as e:
            print(e, f'题号{problem_id}')
