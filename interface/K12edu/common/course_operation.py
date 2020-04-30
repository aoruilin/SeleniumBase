import time
import requests
from calendar import weekday

from interface.K12edu.common.assert_msg import assert_res


def add_course(parameter, class_id, series_id, course_plan=False):
    """
    发布课程操作
    :param parameter: 参数对象
    :param class_id: 班级id
    :param series_id: 系列id
    :param course_plan: 是否有授课计划
    :return:
    """
    url = f'{parameter.ip}/course/teacher/issue'
    plan_weeks = [__choose_course_plan()] if course_plan else [0]
    data = {
        "classIds": [class_id],
        "planCourse": course_plan,
        "planWeeks": plan_weeks,
        "seriesId": series_id
    }
    res = requests.post(url=url, headers=parameter.headers, json=data)
    assert_res(res.text)


def __choose_course_plan():
    now_time_str = time.strftime('%Y%m%d')
    week_day_index = weekday(int(now_time_str[:4]), int(now_time_str[4:6]), int(now_time_str[6:8]))

    return week_day_index


def edit_course(parameter, course_id, course_plan=False):
    """
    老师编辑课程
    :param parameter: 参数对象
    :param course_id: 课程id
    :param course_plan: 是否开启授课计划
    :return:
    """
    url = f'{parameter.ip}/course/teacher/edit'
    plan_week = [0, 1, 2, 3, 4, 5, 6] if course_plan else [0]
    data = {
        "id": course_id,
        "planCourse": course_plan,
        "planWeeks": plan_week
    }
    res = requests.post(url=url, headers=parameter.headers, json=data)
    assert_res(res.text)


def finish_course(parameter, course_id):
    """
    老师结束课程
    :param parameter:参数对象
    :param course_id:课程id
    :return:
    """
    url = f'{parameter.ip}/course/teacher/finish/{course_id}'
    res = requests.get(url=url, headers=parameter.headers)
    assert_res(res.text)


def del_course(parameter, course_id):
    """
    删除指定课程
    :param parameter: 参数对象
    :param course_id: 课程id
    :return:
    """
    url = f'{parameter.ip}/course/teacher/del/{course_id}'
    res = requests.get(url=url, headers=parameter.headers)
    assert_res(res.text)
