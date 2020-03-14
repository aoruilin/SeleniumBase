import base64
import time
import requests
from itertools import chain

from interface.common.time_parameter import time_stamp
from interface.K12edu.common.assert_msg import assert_res
from ui_auto.common.mysql import get_choice
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
    timing_post_time = time_stamp(start=True) if timing == 1 else None
    all_choice_id = []
    all_programme_id = []
    for point_id in point_id_list:
        problem_id_list = parameter.get_problem_id(point_id, 1)
        choice_id_list = parameter.get_problem_id(point_id, 2)
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
        "timingPostTime": timing_post_time
    }
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


def do_homework_simple(parameter, cut_num, traditional_teach=False, homework_num=1):
    url = f'{parameter.ip}/pc/homeworkEvalRecordMultiCode' if traditional_teach else \
        f'{parameter.ip}/pc/gate/homework/student/homeworkEvalRecordMultiCode'
    # point_id_list = parameter.get_point_id()
    # point_id = point_id_list[0]
    eval_id_list = parameter.get_eval_id(traditional_teach=traditional_teach)
    for n in range(homework_num):  # 做前几个作业
        eval_id = eval_id_list[n]
        if traditional_teach:
            choice_problem_id_list = parameter.get_choice_problem_id_for_ui(eval_id)[:cut_num] \
                if cut_num else parameter.get_choice_problem_id_for_ui(eval_id)
            for p, c in choice_problem_id_list:
                answer = get_choice(problem_id=p, problem_name=None)
                choice_url = f'{parameter.ip}/pc/choice/judgeChoice?answer={answer}&evalChoiceId={c}'
                choice_response = requests.post(url=choice_url, headers=parameter.headers)
                assert_res(choice_response.text)  # 选择题
                time.sleep(1)

        problem_id_list, send_ojcode_list = parameter.get_ojcode_for_ord(eval_id,
                                                                         traditional_teach=traditional_teach)
        for a, b in zip(send_ojcode_list, problem_id_list):
            data = {
                "isSubmit": 1,
                "pictureContent": "",
                "pictureContentError": "",
                'evalId': eval_id,
                # 'pointId': point_id,
                'ojcode': a,
                'problemId': b
            }
            turtle_img = __base64_img(b)
            if turtle_img:
                data['pictureContent'] = f'data:image/png;base64,{turtle_img}'
            response = requests.put(url=url, headers=parameter.headers, json=data)
            ret = response.json()
            __assert_code_result(ret, b)
            time.sleep(1)

        commit_url = f'{parameter.ip}/pc/student/homeworkEval/{eval_id}' if traditional_teach \
            else f'{parameter.ip}/pc/gate/homework/student/homeworkEval/{eval_id}'  # 提交作业
        commit_data = {"result": 1}
        commit_response = requests.put(url=commit_url, headers=parameter.headers, json=commit_data)
        assert_res(commit_response.text)
        time.sleep(2)

        cha_problem_id_list = []
        for i in range(2):  # 紧急挑战做题
            challenge_problem_url = f'{parameter.ip}/pc/student/challengeProblem/{eval_id}' if traditional_teach \
                else f'{parameter.ip}/pc/gate/homework/student/challengeProblem/{eval_id}'  # 拉紧急挑战题目
            cha_code_url = f'{parameter.ip}/pc/student/homeworkEvalChallengeMultiCode' if traditional_teach \
                else f'{parameter.ip}/pc/gate/homework/student/homeworkEvalChallengeMultiCode'
            cha_data = {
                'isSubmit': 1,
                'pictureContent': '',
                'pictureContentError': '',
                'evalId': eval_id,
                # 'pointId': point_id
            }
            response_cha = requests.get(url=challenge_problem_url, headers=parameter.headers)
            cha_ret = response_cha.json()
            try:
                cha_problem_id = cha_ret['data']['id']
            except TypeError:
                print(f'紧急挑战题目接口报错，返回{cha_ret["msg"]}')
            except BaseException as e:
                print(e)
            else:
                cha_problem_id_list.append(cha_problem_id)
                cha_data['problemId'] = cha_problem_id
                ojcode = parameter.get_ojcode_for_cha(cha_problem_id)
                cha_data['ojcode'] = ojcode
                response_cha_code = requests.put(url=cha_code_url, headers=parameter.headers, json=cha_data)
                cha_code_ret = response_cha_code.json()
                __assert_code_result(cha_code_ret, cha_problem_id)
            time.sleep(1)

        # 紧急挑战完成信息列表
        cha_problem_list_url = f'{parameter.ip}/pc/student/homeworkEvalChallenge/multi' \
                               f'?pageNum=1&pageSize=50&evalId={eval_id}&sort=0' \
            if traditional_teach else f'{parameter.ip}/pc/gate/homework/student/homeworkEvalChallenge/multi' \
                                      f'?pageNum=1&pageSize=12&evalId={eval_id}'
        cha_problem_list_res = requests.get(url=cha_problem_list_url, headers=parameter.headers)
        p_list_ret = cha_problem_list_res.json()
        try:
            problem_info_list = p_list_ret['data']['list']
        except TypeError:
            print(f'紧急挑战完成信息接口报错，返回{p_list_ret["msg"]}')
        except KeyError:
            print(p_list_ret)
        else:
            does_cha_problem_id_list = [int(p['problemId']) for p in problem_info_list]
            assert (does_cha_problem_id_list.sort() == cha_problem_id_list.sort())


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


def __assert_code_result(ret, problem_id):
    try:
        out = ret['data']['outputDataDetailResult']
        assert ('测评通过。' == out)
    except TypeError:
        print(f'紧急挑战评测接口报错，返回{ret["msg"]}', problem_id)
    except AssertionError as a:
        print(a, f'题号{problem_id}')
    except BaseException as e:
        print(e, f'题号{problem_id}')
