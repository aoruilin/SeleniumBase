import requests
from interface.uni_lab.common.login_for_others import login_interface
from base.data import Ips

ip = Ips.ip_for_uniLab
URL = ip + '/pc/common/getPointList?language=2'
HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.84 Safari/537.36'
}

def get_point_id(url=URL, headers=HEADERS):
    '''提供公用的pointId'''
    token = login_interface()
    headers['token'] = token
    response = requests.get(url=url, headers=headers)
    point_list_ret = response.json()
    data_list = point_list_ret['data']
    problem_dic = data_list[3] #知识点二级列表
    problem_list = problem_dic['list']
    id_list = []
    for i in problem_list:
        point_id = i['id']
        id_list.append(point_id)
    pointId_for_homework = id_list[0]
    pointId_for_course = id_list[1]
    return pointId_for_homework, pointId_for_course

# print(get_point_id())

