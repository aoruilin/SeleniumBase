import requests
from interface.uni_lab.common.login_for_others import login_interface
from interface.uni_lab.common.pointId_for_others import get_point_id
from base.data import Ips

ip = Ips.ip_for_uniLab
pointId = get_point_id()
URL = ip + '/pc/problem?klPoints=%s&pageNum=1&pageSize=12&difficulty=1' % pointId[0]
HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.84 Safari/537.36'
    }


def get_problem_id(url=URL, headers=HEADERS):
    '''提供公用的problemId'''
    token = login_interface()
    headers['token'] = token
    response = requests.get(url=url, headers=headers)
    data_ret = response.json()
    data = data_ret['data']
    problem_list = data['list']
    problemId_list = []
    for d in problem_list:
        problem_id = d['id']
        problemId_list.append(problem_id)

    return problemId_list


# print(get_problem_id())
