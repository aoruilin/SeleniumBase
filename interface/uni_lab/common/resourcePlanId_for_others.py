import requests
from interface.uni_lab.common.login_for_others import login_interface
from interface.uni_lab.common.pointId_for_others import get_point_id
from base.data import Ips

ip = Ips.ip_for_uniLab
pointId = get_point_id()
URL = ip + '/pc/course/getResourcePlanList?pointId=%s&pageNum=1&pageSize=4' % pointId[1]
HEADERS = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.84 Safari/537.36'
    }

def get_resourcePlan_id(url=URL, headers=HEADERS):
    '''提供公用的resourcePlanId'''
    token = login_interface()
    headers['token'] = token
    response = requests.get(url=url, headers=headers)
    data_ret = response.json()
    data = data_ret['data']
    data_list = data['list']
    resourceP_id_list = []
    for r in data_list:
        resourcePlan_id = r['id']
        resourceP_id_list.append(resourcePlan_id)
    return resourceP_id_list

# print(get_resourcePlan_id())


