import requests
from interface.uni_lab.common.classId_for_others import getClassList
from base.data import Ips

ip = Ips.ip_for_uniLab
URL = ip + '/pc/project'
HEADERS = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.84 Safari/537.36'
}
def get_project_id(url=URL, headers=HEADERS):
    token = getClassList()[0]
    headers['token'] = token
    response = requests.get(url=url, headers=headers)
    res_data = response.json()
    data_list = res_data['data']
    data_dic = data_list[0]
    project_id = data_dic['projectId']

    return project_id

# print(get_project_id())

